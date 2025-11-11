"""
Script to populate the database with sample data.
"""

from datetime import datetime, timedelta
import random

from genesis_ecommerce.db.core import engine
from genesis_ecommerce.db.schema import Users, Orders
from genesis_ecommerce.logger import logger
from sqlmodel import Session


def create_sample_data():
    """Create sample users and orders."""

    # Sample data
    sample_users = [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "hashed_password": "hashed_pass_123",
        },
        {
            "username": "jane_smith",
            "email": "jane@example.com",
            "hashed_password": "hashed_pass_456",
        },
        {
            "username": "bob_wilson",
            "email": "bob@example.com",
            "hashed_password": "hashed_pass_789",
        },
        {
            "username": "alice_brown",
            "email": "alice@example.com",
            "hashed_password": "hashed_pass_012",
        },
        {
            "username": "charlie_davis",
            "email": "charlie@example.com",
            "hashed_password": "hashed_pass_345",
        },
    ]

    sample_items = [
        ["Laptop", "Mouse", "Keyboard"],
        ["Phone", "Case", "Screen Protector"],
        ["Headphones", "USB Cable"],
        ["Monitor", "HDMI Cable", "Desk Mount"],
        ["Tablet", "Stylus"],
        ["Webcam", "Microphone"],
        ["External SSD", "USB Hub"],
        ["Gaming Chair"],
        ["Desk Lamp", "Cable Organizer"],
        ["Backpack", "Water Bottle"],
    ]

    order_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]

    with Session(engine) as session:
        logger.info("Creating sample users...")
        created_users = []

        for user_data in sample_users:
            now = datetime.now()
            user = Users(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=user_data["hashed_password"],
                is_active=True,
                created_at=now - timedelta(days=random.randint(30, 365)),
                updated_at=now,
            )
            session.add(user)
            created_users.append(user)

        session.commit()
        logger.info(f"✓ Created {len(created_users)} users")

        # Refresh to get IDs
        for user in created_users:
            session.refresh(user)

        logger.info("Creating sample orders...")
        total_orders = 0

        for user in created_users:
            # Each user gets 2-5 orders
            num_orders = random.randint(2, 5)

            for i in range(num_orders):
                days_ago = random.randint(1, 90)
                created_at = datetime.now() - timedelta(days=days_ago)

                order = Orders(
                    user_id=user.id,
                    items=random.choice(sample_items),
                    status=random.choice(order_statuses),
                    created_at=created_at,
                    updated_at=created_at + timedelta(days=random.randint(0, 5)),
                )
                session.add(order)
                total_orders += 1

        session.commit()
        logger.info(f"✓ Created {total_orders} orders")

        logger.info("")
        logger.info("✅ Sample data created successfully!")
        logger.info(f"   - Users: {len(created_users)}")
        logger.info(f"   - Orders: {total_orders}")


if __name__ == "__main__":
    logger.info("Populating database with sample data...")
    logger.info("")
    create_sample_data()
