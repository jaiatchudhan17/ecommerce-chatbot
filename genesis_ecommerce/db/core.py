from sqlmodel import Session, create_engine

from genesis_ecommerce.config import settings

# Create engine with connection pooling
engine = create_engine(
    settings.database_url,
    echo=True,  # Set to False in production
    pool_pre_ping=True,  # Verify connections before using them
)


def get_session():
    """
    Dependency function to get a database session.
    Use with FastAPI's Depends or in a context manager.
    """
    with Session(engine) as session:
        yield session


def init_db():
    """
    Initialize the database by creating all tables.
    Call this function at application startup.
    """
    from sqlmodel import SQLModel

    # Import models to register them with SQLModel metadata
    import genesis_ecommerce.db.schema  # noqa: F401

    SQLModel.metadata.create_all(engine)
