from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher
import django
from django.conf import settings

# Configuración mínima de Django
if not settings.configured:
    settings.configure(
        PASSWORD_HASHERS=[
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        ]
    )

def hash_password_django(password):
    """
    Genera un hash PBKDF2-SHA256 usando Django
    """
    hashed = make_password(password)
    return hashed

# Ejemplo de uso
password = "sshelf0607"
hashed_password = hash_password_django(password)
print(f"Hash: {hashed_password}")