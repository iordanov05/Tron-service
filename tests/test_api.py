import pytest
from httpx import AsyncClient
from httpx import ASGITransport  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.main import app
from app.db.session import AsyncSessionLocal

@pytest.mark.asyncio
async def test_post_tron_info() -> None:
    test_address: str = "TNuoKL1ni8aoshfFL1ASca1Gou9RXwAzfn"

    transport = ASGITransport(app=app)

    async with AsyncClient(base_url="http://test", transport=transport) as ac:
        response = await ac.post("/tron", json={"address": test_address})
    try:
        print("RESPONSE:", response.json())
    except Exception:
        print("RAW:", response.text)

    assert response.status_code == 200
    data: dict = response.json()

    assert data["address"] == test_address
    assert isinstance(data["balance"], float)
    assert isinstance(data["bandwidth"], int)
    assert isinstance(data["energy"], int)

    async with AsyncSessionLocal() as db: 
        await db.execute(
            text("DELETE FROM tron_requests WHERE address = :address"),
            {"address": test_address}
        )
        await db.commit()




