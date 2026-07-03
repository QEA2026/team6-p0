"""
User Model
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    username: str
    password: str
    role: str
    id: Optional[int] = None

    def __post_init__(self):
        if self.role != 'Employee':
            raise ValueError("Role must be 'Employee'")