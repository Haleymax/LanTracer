from typing import Union, List, Dict

from pydantic import BaseModel

class DeviceResponse(BaseModel):
    status: bool
    message: Union[List[Dict[str, str]], str]