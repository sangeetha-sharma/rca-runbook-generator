import pytest
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres_url() -> str:
    # Start one PostgreSQL container for the whole test session.
    with PostgresContainer("postgres:16") as container:
        # Build the sync URL testcontainers gives us, then swap the driver
        # to asyncpg so it matches the async SQLAlchemy engine used by the app.
        sync_url = container.get_connection_url()
        async_url = sync_url.replace("psycopg2", "asyncpg")

        # Yield the URL to tests; no tables are created here.
        yield async_url

        # Container is stopped automatically when the `with` block exits,
        # i.e. after the test session finishes using this fixture.
