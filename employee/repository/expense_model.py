"""
Expense Model
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Expense:
    user_id: int
    amount: float
    description: str
    category: str
    date: str
    id: Optional[int] = None
