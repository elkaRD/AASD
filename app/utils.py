from abc import ABC
from abc import ABC
from typing import Set, TypeVar

from pydantic import BaseModel as PydanticModel

T = TypeVar('T')


class Typable(ABC):
    @classmethod
    def all_subclasses(cls: T) -> Set[T]:
        subclasses = set(cls.__subclasses__())
        subsubclasses = set()
        for subclass in subclasses:
            subsubclasses |= set(subclass.__subclasses__())
        return subclasses | subsubclasses

    @classmethod
    def for_type(cls: T, type: str) -> T:
        subclass_mapping = {
            subclass.type: subclass
            for subclass in cls.all_subclasses()
        }
        return subclass_mapping[type]


class BaseModel(PydanticModel):
    def pretty_print(
            self,
            indent: int = 4,
            sort_keys: bool = True,
            **kwargs
    ) -> str:
        return self.json(indent=indent, sort_keys=sort_keys, **kwargs)
