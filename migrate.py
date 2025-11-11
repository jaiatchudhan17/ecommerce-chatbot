"""
Database migration script to create all tables.
"""

from genesis_ecommerce.db.core import init_db
from genesis_ecommerce.logger import logger


if __name__ == "__main__":
    logger.info("Running database migration...")
    logger.info("Creating all tables...")
    init_db()
    logger.info("✓ Database tables created successfully!")
