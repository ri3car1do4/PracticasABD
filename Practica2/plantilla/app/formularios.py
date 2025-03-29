"""
Modulo en el que definimos los formularios de nuestra aplicacion
"""
from typing import List
import datetime
from dateutil import relativedelta
from wtforms import StringField, PasswordField, SelectField, DateField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL, ValidationError, NumberRange
from flask_wtf import FlaskForm

class SignupForm(FlaskForm):
    """Formulario para el registro de usuarios"""
    email = StringField(
        'Email',
        [
            Email(message='No es un email válido.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Contraseña',
        [
            DataRequired(message="Introduzca una contraseña."),
            Length(8, message="Contraseña mínimo de 8")
        ]
    )
    confirmPassword = PasswordField(
        'Repite Contraseña',
        [
            DataRequired(message="Please enter a password."),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    cumple = DateField('Tu cumpleaños', validators=[DataRequired("Introduce un cumpleaños")])
    submit = SubmitField('Submit')

    def validate_birthday(self, field):
        """
        Solo permitimos fechas de cumpleaños de más de 18 años y no futuras
        """
        if field.data >= datetime.date.today():
            raise ValidationError("¡La fecha no puede estar en el futuro!")

        # Usamos relativedelta.relativedelta(end_date, start_date) para obtener la diferencia
        # de tiempos
        if relativedelta.relativedelta(datetime.date.today(), field.data).years < 14:
            raise ValidationError("Solo está permitido el registro de mayores de edad.")

class SignInForm(FlaskForm):
    """Formulario para hacer login"""
    email = StringField(
        'Email',
        [
            Email(message='No es un email válido.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Contraseña',
        [
            DataRequired(message="Introduzca una contraseña."),
        ]
    )

    submit = SubmitField('Submit')

class NuevaLiga(FlaskForm):
    """Formulario para crear un nueva Liga"""
    # render_kw nos permite poner texto dentro de la caja de texto
    nombre = StringField('Nombre', validators=[DataRequired("La liga debe tener nombre.")],
                           render_kw={"placeholder": "Nombre..."})
    numero_participantes_maximo = StringField('Número máximo de participantes',
                           validators=[DataRequired("La liga debe tener un número máximo de participantes.")],
                           render_kw={"placeholder": "0"})
    password = StringField('Contraseña', render_kw={"placeholder": "Contraseña..."})

    submit = SubmitField('Aceptar')

class PasswordForm(FlaskForm):
    """Formulario para la contraseña de una liga"""
    password = PasswordField(
        'Contraseña',
        [
            DataRequired(message="Introduzca una contraseña."),
        ]
    )

    submit = SubmitField('Submit')