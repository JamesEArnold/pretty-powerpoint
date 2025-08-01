"""Repository interface definitions."""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")


class Repository(Generic[T], ABC):
    """Base repository interface."""

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """Get entity by ID."""
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save entity."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        pass

    @abstractmethod
    async def list(self, **filters: str) -> List[T]:
        """List entities with optional filters."""
        pass
