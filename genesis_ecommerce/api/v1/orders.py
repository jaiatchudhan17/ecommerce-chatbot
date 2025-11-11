from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from genesis_ecommerce.db.core import get_session
from genesis_ecommerce.db.schema import Orders
from genesis_ecommerce.logger import logger

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/user/{user_id}")
async def fetch_user_orders(user_id: int, session: Session = Depends(get_session)):
    """
    Fetch all orders for a specific user.

    Args:
        user_id: The ID of the user
        session: Database session (injected)

    Returns:
        List of orders for the user
    """
    logger.info(f"Fetching orders for user_id: {user_id}")

    try:
        statement = select(Orders).where(Orders.user_id == user_id)
        orders = session.exec(statement).all()

        logger.info(f"Found {len(orders)} orders for user_id: {user_id}")

        return {"user_id": user_id, "order_count": len(orders), "orders": orders}
    except Exception as e:
        logger.error(f"Error fetching orders for user_id {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch orders")
