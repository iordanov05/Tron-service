from pydantic import BaseModel, ConfigDict
from datetime import datetime

# получаем от клиента в POST-запросе
class TronAddressRequest(BaseModel):
    address: str

# отдадим клиенту в ответ на POST-запрос
class TronAddressResponse(BaseModel):
    address: str
    balance: float
    bandwidth: int
    energy: int

# отдадим клиенту в GET-запросе
class TronRequestRecord(BaseModel):
    id: int
    address: str
    balance: float
    bandwidth: int
    energy: int
    timestamp: datetime

    # Новый способ настройки
    model_config = ConfigDict(from_attributes=True)
