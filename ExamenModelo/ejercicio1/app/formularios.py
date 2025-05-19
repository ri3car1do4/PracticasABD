"""
Modulo en el que definimos los formularios de nuestra aplicacion
"""
from typing import List
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from flask_wtf import FlaskForm


class NuevoMazo(FlaskForm):
    """Formulario para crear un nuevo mazo"""
    # render_kw nos permite poner texto dentro de la caja de texto
    nombre = StringField('Nombre del mazo', validators=[DataRequired()],
                           render_kw={"placeholder": "Nombre..."})

    submit = SubmitField('Aceptar')


# Vamos a incluir un validador a partir de una funcion externa.
def restringir_carta_no_incluida(form, field):
    """
    Restringir que una carta con el mismo nombre no se ha incluido previamente
    """
    # Comprobamos que la informacion del campo no esta en el atributo "nombre_carta
    if field.data in form.cartas_ya_incluidas:
        raise ValidationError("Ya se ha incluido una carta con ese nombre")


class AnyadirCarta(FlaskForm):
    """ Formulario para añadir cartas. Se tiene en cuenta el nombre de la carta """
    nombre_carta = StringField('Nombre de la carta', validators=[DataRequired(), restringir_carta_no_incluida])
    banquillo = BooleanField('Banquillo')
    numero_copias = IntegerField('Número de copias', validators=[DataRequired(),
                                                                 NumberRange(min=0, message="Se debe incluir "
                                                                                            "al menos una copia")])
    submit = SubmitField('Añadir')

    def __init__(self, cartas_ya_incluidas: List[str], *args, **kwargs):
        # Llamamos al constructor de super()
        super().__init__(*args, **kwargs)

        # Nombre de las cartas ya incluidas
        self.cartas_ya_incluidas = cartas_ya_incluidas
