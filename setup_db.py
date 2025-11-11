#!/usr/bin/env python3
"""
Setup script to initialize the database and seed sample data.
Run this script after configuring your .env file.
"""

import sys
from genesis_ecommerce.logger import logger


def main():
    """Run database migration and seeding."""

    print("=" * 60)
    print("Genesis E-commerce - Database Setup")
    print("=" * 60)
    print()

    # Step 1: Run migrations
    logger.info("Step 1: Running database migrations...")
    try:
        from genesis_ecommerce.db.core import init_db

        init_db()
        logger.info("✓ Database tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Migration failed: {str(e)}")
        sys.exit(1)

    print()

    # Step 2: Ask about seeding
    logger.info("Step 2: Seed sample data?")
    response = input(
        "Would you like to populate the database with sample data? (y/n): "
    ).lower()

    if response in ["y", "yes"]:
        try:
            from seed_data import create_sample_data

            create_sample_data()
        except Exception as e:
            logger.error(f"❌ Seeding failed: {str(e)}")
            sys.exit(1)
    else:
        logger.info("Skipping sample data creation.")

    print()
    print("=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Start the server: python run.py")
    print("2. Visit API docs: http://localhost:8000/docs")
    print("3. Test chatbot: python test_chatbot.py")
    print()


if __name__ == "__main__":
    main()
