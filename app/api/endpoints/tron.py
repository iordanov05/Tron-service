from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from typing import List

from app.services.tron_client import client
from app.schemas.tron import TronAddressRequest, TronAddressResponse
from app.db.session import AsyncSessionLocal
from app.db.crud import create_tron_request
from app.schemas.tron import TronRequestRecord
from app.db.crud import get_tron_requests

router = APIRouter()

# Зависимость для передачи сессии БД
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/tron", response_model=TronAddressResponse)
async def get_wallet_info(
    data: TronAddressRequest,
    db: AsyncSession = Depends(get_db)
) -> TronAddressResponse:
    """
    Получает информацию по Tron-кошельку, сохраняет в базу и возвращает пользователю.
    """
    try:
        # Получаем баланс и ресурсы из сети Tron
        acc = client.get_account(data.address)
        res = client.get_account_resource(data.address)

        balance: float = int(acc.get("balance", 0)) / 1_000_000
        bandwidth: int = res.get("free_net_used", 0)
        energy: int = res.get("EnergyLimit", 0)

        # Сохраняем в базу
        await create_tron_request(
            db=db,
            address=data.address,
            balance=balance,
            bandwidth=bandwidth,
            energy=energy
        )

        # Возвращаем результат пользователю
        return TronAddressResponse(
            address=data.address,
            balance=balance,
            bandwidth=bandwidth,
            energy=energy
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/tron", response_model=List[TronRequestRecord])
async def read_tron_requests(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
) -> List[TronRequestRecord]:
    """
    Возвращает список последних запросов из базы.
    
    Параметры:
    - skip: сколько пропустить (для пагинации)
    - limit: сколько вернуть записей
    """
    return await get_tron_requests(db=db, skip=skip, limit=limit)    