from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from genesis_ecommerce.customer_support_bot.bot import get_chatbot
from genesis_ecommerce.db.core import get_session
from genesis_ecommerce.db.schema import Orders, Tickets
from genesis_ecommerce.logger import logger

router = APIRouter(prefix="/support", tags=["support"])


class CreateTicketRequest(BaseModel):
    """Request model for creating a support ticket."""

    order_id: int
    issue_description: str


class UpdateTicketStatusRequest(BaseModel):
    """Request model for updating ticket status."""

    status: str


@router.post("/tickets")
async def create_ticket(
    ticket_request: CreateTicketRequest, session: Session = Depends(get_session)
):
    """
    Create a new support ticket for an order.

    Args:
        ticket_request: Ticket creation request with order_id and issue_description
        session: Database session (injected)

    Returns:
        Created ticket details
    """
    logger.info(f"Creating ticket for order_id: {ticket_request.order_id}")

    try:
        # Verify order exists
        order = session.get(Orders, ticket_request.order_id)
        if not order:
            logger.warning(f"Order not found: {ticket_request.order_id}")
            raise HTTPException(status_code=404, detail="Order not found")

        # Create new ticket
        new_ticket = Tickets(
            order_id=ticket_request.order_id,
            issue_description=ticket_request.issue_description,
            status="open",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        session.add(new_ticket)
        session.commit()
        session.refresh(new_ticket)

        logger.info(
            f"Created ticket {new_ticket.id} for order {ticket_request.order_id}"
        )

        return {
            "message": "Ticket created successfully",
            "ticket": new_ticket,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating ticket: {str(e)}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create ticket")


@router.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int, session: Session = Depends(get_session)):
    """
    Get details of a specific support ticket.

    Args:
        ticket_id: The ID of the ticket
        session: Database session (injected)

    Returns:
        Ticket details
    """
    logger.info(f"Fetching ticket: {ticket_id}")

    try:
        ticket = session.get(Tickets, ticket_id)
        if not ticket:
            logger.warning(f"Ticket not found: {ticket_id}")
            raise HTTPException(status_code=404, detail="Ticket not found")

        logger.info(f"Retrieved ticket {ticket_id} with status: {ticket.status}")
        return ticket
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching ticket {ticket_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch ticket")


@router.get("/tickets/order/{order_id}")
async def get_tickets_by_order(order_id: int, session: Session = Depends(get_session)):
    """
    Get all support tickets for a specific order.

    Args:
        order_id: The ID of the order
        session: Database session (injected)

    Returns:
        List of tickets for the order
    """
    logger.info(f"Fetching tickets for order_id: {order_id}")

    try:
        # Verify order exists
        order = session.get(Orders, order_id)
        if not order:
            logger.warning(f"Order not found: {order_id}")
            raise HTTPException(status_code=404, detail="Order not found")

        statement = select(Tickets).where(Tickets.order_id == order_id)
        tickets = session.exec(statement).all()

        logger.info(f"Found {len(tickets)} tickets for order_id: {order_id}")

        return {
            "order_id": order_id,
            "ticket_count": len(tickets),
            "tickets": tickets,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching tickets for order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch tickets")


@router.get("/tickets/user/{user_id}")
async def get_tickets_by_user(user_id: int, session: Session = Depends(get_session)):
    """
    Get all support tickets for all orders of a specific user.

    Args:
        user_id: The ID of the user
        session: Database session (injected)

    Returns:
        List of all tickets for the user's orders
    """
    logger.info(f"Fetching all tickets for user_id: {user_id}")

    try:
        # Get all orders for the user
        orders_statement = select(Orders).where(Orders.user_id == user_id)
        orders = session.exec(orders_statement).all()

        if not orders:
            logger.info(f"No orders found for user_id: {user_id}")
            return {
                "user_id": user_id,
                "ticket_count": 0,
                "tickets": [],
            }

        # Get all tickets for those orders
        order_ids = [order.id for order in orders]
        tickets_statement = select(Tickets).where(Tickets.order_id.in_(order_ids))
        tickets = session.exec(tickets_statement).all()

        logger.info(f"Found {len(tickets)} tickets for user_id: {user_id}")

        return {
            "user_id": user_id,
            "ticket_count": len(tickets),
            "tickets": tickets,
        }
    except Exception as e:
        logger.error(f"Error fetching tickets for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch user tickets")


@router.patch("/tickets/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: int,
    status_request: UpdateTicketStatusRequest,
    session: Session = Depends(get_session),
):
    """
    Update the status of a support ticket.

    Args:
        ticket_id: The ID of the ticket
        status_request: New status for the ticket
        session: Database session (injected)

    Returns:
        Updated ticket details
    """
    logger.info(f"Updating ticket {ticket_id} status to: {status_request.status}")

    try:
        ticket = session.get(Tickets, ticket_id)
        if not ticket:
            logger.warning(f"Ticket not found: {ticket_id}")
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Validate status
        valid_statuses = ["open", "in_progress", "resolved", "closed"]
        if status_request.status not in valid_statuses:
            logger.warning(f"Invalid status: {status_request.status}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
            )

        old_status = ticket.status
        ticket.status = status_request.status
        ticket.updated_at = datetime.now()

        session.add(ticket)
        session.commit()
        session.refresh(ticket)

        logger.info(
            f"Updated ticket {ticket_id} status from {old_status} to {ticket.status}"
        )

        return {
            "message": "Ticket status updated successfully",
            "ticket": ticket,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating ticket {ticket_id}: {str(e)}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update ticket status")


@router.get("/tickets")
async def get_all_tickets(
    status: str | None = None, session: Session = Depends(get_session)
):
    """
    Get all support tickets, optionally filtered by status.

    Args:
        status: Optional filter by ticket status
        session: Database session (injected)

    Returns:
        List of tickets
    """
    logger.info(f"Fetching all tickets{f' with status: {status}' if status else ''}")

    try:
        statement = select(Tickets)
        if status:
            statement = statement.where(Tickets.status == status)

        tickets = session.exec(statement).all()

        logger.info(f"Found {len(tickets)} tickets")

        return {
            "ticket_count": len(tickets),
            "tickets": tickets,
            "filter": {"status": status} if status else None,
        }
    except Exception as e:
        logger.error(f"Error fetching tickets: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch tickets")


# ============================================================================
# CHATBOT ENDPOINTS
# ============================================================================


class ChatMessage(BaseModel):
    """Model for a chat message in conversation history."""

    role: str  # 'user' or 'assistant'
    content: str


class ChatRequest(BaseModel):
    """Request model for chatbot interaction."""

    message: str
    order_id: Optional[int] = None
    ticket_id: Optional[int] = None
    user_id: Optional[int] = None
    conversation_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """Response model for chatbot interaction."""

    response: str
    conversation_id: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    chat_request: ChatRequest, session: Session = Depends(get_session)
):
    """
    Chat with the customer support bot.

    The bot can answer questions about:
    - Orders (provide order_id for specific order context)
    - Support tickets (provide ticket_id for specific ticket context)
    - User's orders (provide user_id to see all orders)
    - General policies, terms, and support information

    Args:
        chat_request: Chat request with message and optional context
        session: Database session (injected)

    Returns:
        Bot's response
    """
    logger.info(
        f"Chat request: {chat_request.message[:50]}... "
        f"(order_id={chat_request.order_id}, "
        f"ticket_id={chat_request.ticket_id}, "
        f"user_id={chat_request.user_id})"
    )

    try:
        # Get the chatbot instance
        bot = get_chatbot()

        # Convert conversation history to dict format if provided
        history = None
        if chat_request.conversation_history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in chat_request.conversation_history
            ]

        # Generate response
        response = await bot.chat(
            message=chat_request.message,
            session=session,
            order_id=chat_request.order_id,
            ticket_id=chat_request.ticket_id,
            user_id=chat_request.user_id,
            conversation_history=history,
        )

        logger.info("Successfully generated chat response")

        return ChatResponse(response=response)

    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process chat request. Please try again or contact support.",
        )


@router.post("/chat/order/{order_id}", response_model=ChatResponse)
async def chat_about_order(
    order_id: int,
    message: str,
    session: Session = Depends(get_session),
):
    """
    Chat with the bot about a specific order.

    This is a convenience endpoint that automatically includes order context.

    Args:
        order_id: The order ID to discuss
        message: Your question about the order
        session: Database session (injected)

    Returns:
        Bot's response with order context
    """
    logger.info(f"Order-specific chat: order_id={order_id}, message={message[:50]}...")

    try:
        # Verify order exists
        order = session.get(Orders, order_id)
        if not order:
            logger.warning(f"Order not found: {order_id}")
            raise HTTPException(status_code=404, detail="Order not found")

        # Get the chatbot instance
        bot = get_chatbot()

        # Generate response with order context
        response = await bot.chat(
            message=message,
            session=session,
            order_id=order_id,
        )

        logger.info(f"Successfully generated response for order {order_id}")

        return ChatResponse(response=response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing order chat request: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat request.")


@router.post("/chat/ticket/{ticket_id}", response_model=ChatResponse)
async def chat_about_ticket(
    ticket_id: int,
    message: str,
    session: Session = Depends(get_session),
):
    """
    Chat with the bot about a specific support ticket.

    This is a convenience endpoint that automatically includes ticket context.

    Args:
        ticket_id: The ticket ID to discuss
        message: Your question about the ticket
        session: Database session (injected)

    Returns:
        Bot's response with ticket context
    """
    logger.info(
        f"Ticket-specific chat: ticket_id={ticket_id}, message={message[:50]}..."
    )

    try:
        # Verify ticket exists
        ticket = session.get(Tickets, ticket_id)
        if not ticket:
            logger.warning(f"Ticket not found: {ticket_id}")
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Get the chatbot instance
        bot = get_chatbot()

        # Generate response with ticket context
        response = await bot.chat(
            message=message,
            session=session,
            ticket_id=ticket_id,
        )

        logger.info(f"Successfully generated response for ticket {ticket_id}")

        return ChatResponse(response=response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing ticket chat request: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat request.")
