"""
Customer Support Chatbot using Google Gemini with RAG capabilities.

This module provides a RAG-based chatbot that can answer questions about:
- Order status and tracking
- Support tickets
- Terms and conditions
- General support queries
"""

from pathlib import Path
from typing import List, Optional

import google.generativeai as genai
from sqlmodel import Session, select

from genesis_ecommerce.config import settings
from genesis_ecommerce.db.schema import Orders, Tickets
from genesis_ecommerce.logger import logger


class CustomerSupportBot:
    """
    RAG-based customer support chatbot using Google Gemini.
    """

    def __init__(self):
        """Initialize the chatbot with Gemini API and load documents."""
        # Configure Gemini
        genai.configure(api_key=settings.gemini_api_key)

        # Use Gemini 1.5 Flash for fast responses
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        # Load support documents
        self.documents = self._load_documents()

        # System prompt for the chatbot
        self.system_prompt = """You are a helpful customer support assistant for Genesis E-commerce.

Your responsibilities:
1. Answer questions about orders, shipping, returns, and refunds
2. Provide information from our Terms and Conditions and Support Guide
3. Help customers understand our policies and procedures
4. Be polite, professional, and concise
5. If you cannot find specific information in the provided context, be honest about it

Context Information:
{context}

Important Guidelines:
- Always be courteous and empathetic
- Provide accurate information based on the context
- If discussing specific orders or tickets, use the provided database information
- Cite relevant policy sections when applicable
- Keep responses concise but complete
- If you don't know something, suggest contacting human support
"""

    def _load_documents(self) -> str:
        """
        Load support documents for RAG.

        Returns:
            Combined text content of all support documents
        """
        documents_dir = Path(__file__).parent / "documents"
        combined_text = ""

        try:
            # Load Terms and Conditions
            terms_file = documents_dir / "terms_and_conditions.txt"
            if terms_file.exists():
                with open(terms_file, "r", encoding="utf-8") as f:
                    combined_text += f"=== TERMS AND CONDITIONS ===\n{f.read()}\n\n"
                logger.info("Loaded terms and conditions document")

            # Load Support Guide
            support_file = documents_dir / "support_guide.txt"
            if support_file.exists():
                with open(support_file, "r", encoding="utf-8") as f:
                    combined_text += f"=== SUPPORT GUIDE ===\n{f.read()}\n\n"
                logger.info("Loaded support guide document")

            if not combined_text:
                logger.warning("No support documents found")
                combined_text = "No additional documentation available."

        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            combined_text = "Error loading support documents."

        return combined_text

    def _get_order_context(self, order_id: int, session: Session) -> str:
        """
        Retrieve order information from database.

        Args:
            order_id: Order ID to fetch
            session: Database session

        Returns:
            Formatted order information
        """
        try:
            order = session.get(Orders, order_id)
            if not order:
                return f"Order #{order_id} not found in system."

            order_info = f"""
Order Information:
- Order ID: {order.id}
- User ID: {order.user_id}
- Items: {", ".join(order.items)}
- Status: {order.status}
- Created: {order.created_at}
- Last Updated: {order.updated_at}
"""
            return order_info
        except Exception as e:
            logger.error(f"Error fetching order {order_id}: {str(e)}")
            return f"Error retrieving order #{order_id} information."

    def _get_ticket_context(self, ticket_id: int, session: Session) -> str:
        """
        Retrieve support ticket information from database.

        Args:
            ticket_id: Ticket ID to fetch
            session: Database session

        Returns:
            Formatted ticket information
        """
        try:
            ticket = session.get(Tickets, ticket_id)
            if not ticket:
                return f"Ticket #{ticket_id} not found in system."

            # Also get associated order info
            order = session.get(Orders, ticket.order_id)
            order_status = order.status if order else "Unknown"

            ticket_info = f"""
Support Ticket Information:
- Ticket ID: {ticket.id}
- Order ID: {ticket.order_id}
- Order Status: {order_status}
- Issue: {ticket.issue_description}
- Ticket Status: {ticket.status}
- Created: {ticket.created_at}
- Last Updated: {ticket.updated_at}
"""
            return ticket_info
        except Exception as e:
            logger.error(f"Error fetching ticket {ticket_id}: {str(e)}")
            return f"Error retrieving ticket #{ticket_id} information."

    def _get_user_orders_context(self, user_id: int, session: Session) -> str:
        """
        Retrieve all orders for a user.

        Args:
            user_id: User ID to fetch orders for
            session: Database session

        Returns:
            Formatted orders information
        """
        try:
            statement = select(Orders).where(Orders.user_id == user_id)
            orders = session.exec(statement).all()

            if not orders:
                return f"No orders found for user #{user_id}."

            orders_info = f"User #{user_id} has {len(orders)} order(s):\n"
            for order in orders:
                orders_info += f"\n- Order #{order.id}: {order.status} - {len(order.items)} item(s) - Created: {order.created_at}"

            return orders_info
        except Exception as e:
            logger.error(f"Error fetching orders for user {user_id}: {str(e)}")
            return f"Error retrieving orders for user #{user_id}."

    async def chat(
        self,
        message: str,
        session: Session,
        order_id: Optional[int] = None,
        ticket_id: Optional[int] = None,
        user_id: Optional[int] = None,
        conversation_history: Optional[List[dict]] = None,
    ) -> str:
        """
        Process a chat message and generate a response.

        Args:
            message: User's message
            session: Database session for fetching order/ticket data
            order_id: Optional order ID for context
            ticket_id: Optional ticket ID for context
            user_id: Optional user ID to fetch their orders
            conversation_history: Optional list of previous messages

        Returns:
            Bot's response
        """
        try:
            # Build context
            context_parts = [self.documents]

            # Add specific order/ticket context if provided
            if order_id:
                context_parts.append(self._get_order_context(order_id, session))

            if ticket_id:
                context_parts.append(self._get_ticket_context(ticket_id, session))

            if user_id:
                context_parts.append(self._get_user_orders_context(user_id, session))

            context = "\n\n".join(context_parts)

            # Build the full prompt
            full_prompt = self.system_prompt.format(context=context)

            # Add conversation history if provided
            if conversation_history:
                full_prompt += "\n\nConversation History:\n"
                for msg in conversation_history[-5:]:  # Last 5 messages for context
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    full_prompt += f"{role.capitalize()}: {content}\n"

            # Add current user message
            full_prompt += f"\n\nUser: {message}\n\nAssistant:"

            # Generate response using Gemini
            logger.info(f"Generating response for message: {message[:50]}...")
            response = self.model.generate_content(full_prompt)

            bot_response = response.text
            logger.info("Successfully generated response")

            return bot_response

        except Exception as e:
            logger.error(f"Error generating chat response: {str(e)}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again or contact our support team directly at support@genesis-ecommerce.com"


# Global chatbot instance
_bot_instance = None


def get_chatbot() -> CustomerSupportBot:
    """
    Get or create the global chatbot instance.

    Returns:
        CustomerSupportBot instance
    """
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = CustomerSupportBot()
        logger.info("Initialized customer support chatbot")
    return _bot_instance
