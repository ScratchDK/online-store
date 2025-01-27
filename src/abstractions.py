from abc import ABC, abstractmethod
from typing import Any


class BaseProduct(ABC):
    @classmethod
    @abstractmethod
    def new_product(cls, **kwargs: dict) -> Any:
        pass

    @abstractmethod
    def price(self) -> float | int:
        pass

    @abstractmethod
    def __add__(self, other: Any) -> Any:
        pass

    @abstractmethod
    def __str__(self):
        pass


class BaseEntity(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def get_products(self) -> list:
        pass
