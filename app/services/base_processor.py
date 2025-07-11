from abc import ABC, abstractmethod
from fastapi import UploadFile
from typing import Any
 
class BaseProcessor(ABC):
    @abstractmethod
    async def process(self, file: UploadFile) -> str:
        pass 