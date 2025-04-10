from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.db.models import TronRequest
from sqlalchemy import select
from typing import List

async def create_tron_request(
    db: AsyncSession,
    address: str,
    balance: float,
    bandwidth: int,
    energy: int
) -> None:
    """
    Сохраняет информацию по Tron-кошельку в базу данных.

    :param db: Асинхронная сессия SQLAlchemy
    :param address: Адрес Tron-кошелька
    :param balance: Баланс в TRX
    :param bandwidth: Использованный bandwidth
    :param energy: Лимит энергии
    """
    stmt = insert(TronRequest).values(
        address=address,
        balance=balance,
        bandwidth=bandwidth,
        energy=energy
    )
    await db.execute(stmt)
    await db.commit()

async def get_tron_requests(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10
) -> List[TronRequest]:
    """
    Получить список запросов из базы данных с пагинацией.
    
    :param db: Сессия базы данных
    :param skip: Сколько записей пропустить (offset)
    :param limit: Сколько записей вернуть (limit)
    :return: Список объектов TronRequest
    """
    stmt = select(TronRequest).offset(skip).limit(limit).order_by(TronRequest.timestamp.desc())
    result = await db.execute(stmt)
    return result.scalars().all()