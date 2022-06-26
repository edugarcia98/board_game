from dataclasses import dataclass
from typing import Optional


@dataclass()
class Property:
    name: str
    cost: int
    rent_cost: int
    owner: object
