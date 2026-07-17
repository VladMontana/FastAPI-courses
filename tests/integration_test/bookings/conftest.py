import pytest_asyncio


@pytest_asyncio.fixture(autouse=True)
async def clear_bookings(db):
    await db.bookings.delete_constructor()
    await db.commit()
    yield
    await db.bookings.delete_constructor()
    await db.commit()
