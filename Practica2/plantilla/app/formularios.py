"""
Modulo en el que definimos los formularios de nuestra aplicacion
"""
from typing import List
import datetime
from dateutil import relativedelta
from wtforms import StringField, PasswordField, SelectField, DateField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL, ValidationError, NumberRange
from flask_wtf import FlaskForm
