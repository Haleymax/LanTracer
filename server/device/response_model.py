from typing import Union, List, Dict, Any

from pydantic import BaseModel

class DeviceResponse(BaseModel):
    status: bool
    message: Union[List[Dict[str, str]], str]

class BaseResponse(BaseModel):
    status: bool
    message: str

class MemoryInfoResponse(BaseModel):
    status: bool
    data: list[Any]
    message: str