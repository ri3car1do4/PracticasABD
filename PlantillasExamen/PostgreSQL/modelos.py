from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, ForeignKey
from datetime import date
from typing import List

"""
AYUDA
"""

class Base(DeclarativeBase):
    pass