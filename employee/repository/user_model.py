"""
User Model
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int] # optional because database can set this for you after you save
    username: str
    password: str
    role: str

    def __post_init__(self):
        if self.role != 'Employee':
            raise ValueError("Role must be 'Employee'")