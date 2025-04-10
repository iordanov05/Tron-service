import pytest
from sqlalchemy import text
from app.db.session import AsyncSessionLocal
from app.db.crud import create_tron_request

@pytest.mark.asyncio
async def test_create_tron_request() -> None:
    async with AsyncSessionLocal() as db:
        address = "TestUnitAddress1"
        balance = 99.99
        bandwidth = 123
        energy = 456

        await create_tron_request(
            db=db,
            address=address,
            balance=balance,
            bandwidth=bandwidth,
            energy=energy
        )

        # Прямой SQL-запрос
        result = await db.execute(
            text("SELECT address, balance, bandwidth, energy FROM tron_requests WHERE address = :address"),
            {"address": address}
        )
        row = result.fetchone()

        assert row is not None
        assert row[0] == address
        assert row[1] == balance
        assert row[2] == bandwidth
        assert row[3] == energy
        
        # Удаляем тестовые данные
        await db.execute(
            text("DELETE FROM tron_requests WHERE address = :address"),
            {"address": address}
        )
        await db.commit()
