"""
Modulo en el que definimos los modelos relacionales de nuestra aplicacion
"""

from typing import List
import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
