from django.db import models
from django.core import exceptions

class BitBooleanField(models.BooleanField):
    def get_prep_value(self, value):
        # Convierte True/False a 1/0 para guardar en la base de datos como BIT(1)
        if value is None:
            return None
        return 1 if value else 0

    def to_python(self, value):
        # Convierte b'1'/b'0' (valores binarios) a True/False
        if value is None:
            return None
        if isinstance(value, bytes):
            # Convierte bytes a entero y luego a booleano
            return bool(int.from_bytes(value, 'big'))
        # Maneja otros casos (como True/False o 1/0)
        return bool(value)

    def from_db_value(self, value, expression, connection):
        # Convierte el valor leído desde la base de datos a un booleano
        return self.to_python(value)