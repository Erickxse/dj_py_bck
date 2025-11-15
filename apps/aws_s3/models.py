from django.db import models
from django.conf import settings
import os
import uuid, time, requests
from io import BytesIO
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.exceptions import ValidationError


class CexStand(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    stand_type_id = models.IntegerField()
    seo_id = models.IntegerField()
    stand_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    ruc = models.CharField(max_length=13, blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)  # Guarda solo el nombre de la imagen
    hits = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=255)

    # Instancia de S3Boto3Storage como variable de clase
    s3_storage = S3Boto3Storage()

    def get_image_url(self):
        """Genera la URL pública de CloudFront para la imagen almacenada en S3"""
        if self.img:
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/images/upload/{self.id}/sml/{self.img}"
        return None

    def save_image_to_s3(self, image_file):
        """Sube la imagen a S3 y devuelve el nombre del archivo"""
        
        # Definir las extensiones válidas
        valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        # Validar tamaño máximo (5 MB) en el modelo
        max_size = 5 * 1024 * 1024
        if image_file.size > max_size:
            raise ValidationError("La imagen no debe superar los 5 MB")
        
        try:
            # Obtener la extensión del archivo de la imagen
            file_extension = os.path.splitext(image_file.name)[1].lower()
            
            # Validar si la extensión es una de las permitidas
            if file_extension not in valid_image_extensions:
                raise ValidationError(
                    f"El archivo debe ser una imagen con una de las siguientes extensiones: {', '.join(valid_image_extensions)}"
                )
            
             # Asegurarse de que el stand tiene un id antes de continuar
            if not self.id:
                raise ValidationError("El Stand debe estar guardado previamente para asignarle una imagen.")
            

            # Generar un nombre único para la imagen
            file_name = f"{uuid.uuid4().hex}{file_extension}"  # Usa UUID para evitar conflictos de nombres
            # file_path = f"cex_stands/{self.id}/{file_name}"
            file_path = f"images/upload/{self.id}/sml/{file_name}"

            try:
                # Si ya hay una imagen, eliminarla primero
                if self.img:
                    old_file_path = f"images/upload/{self.id}/sml/{self.img}"
                    if self.s3_storage.exists(old_file_path):
                        self.s3_storage.delete(old_file_path)

                # Guardar la imagen en S3
                self.s3_storage.save(file_path, image_file)

            except Exception as e:
                raise Exception(f"Error al guardar la imagen en S3: {str(e)}")

            return file_name  # Devuelve el nombre del archivo que se almacena en la base de datos

        except ValidationError as e:
            raise ValidationError(f"Validación fallida: {str(e)}")
        except Exception as e:
            raise Exception(f"Ocurrió un error al procesar la imagen: {str(e)}")

    class Meta:
        managed = False  # Esto asegura que Django no alterará la tabla de la base de datos
        db_table = 'cex_stand'

class CexServiceProduct(models.Model):
    stand_id = models.IntegerField()
    category_id = models.IntegerField()
    seo_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.CharField(max_length=255, blank=True, null=True)  # Nombre del archivo
    images = models.TextField(blank=True, null=True)  # Lista de nombres de imágenes
    s3_storage = S3Boto3Storage()

    def save_image_to_s3(self, image_file):
        """Sube la imagen a S3 y devuelve el nombre del archivo."""
        valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        max_size = 5 * 1024 * 1024  # 5MB

        # Validar tamaño máximo
        if image_file.size > max_size:
            raise ValidationError("La imagen no debe superar los 5 MB")

        # Validar extensión
        file_extension = os.path.splitext(image_file.name)[1].lower()
        if file_extension not in valid_image_extensions:
            raise ValidationError(f"Extensión no permitida: {file_extension}")

        # 💡 Asegurar que el producto tiene un ID antes de subir la imagen
        if not self.id:
            self.save()  # Guardar el producto para generar el ID

        # Generar nombre único
        file_name = f"{uuid.uuid4().hex}{file_extension}"
        file_path = f"images/upload/{self.stand_id}/card/{file_name}"

        # 🛑 Borrar imagen anterior antes de subir una nueva
        if self.image:
            old_file_path = f"images/upload/{self.stand_id}/card/{self.image}"
            if self.s3_storage.exists(old_file_path):
                self.s3_storage.delete(old_file_path)

        # 📤 Subir nueva imagen a S3
        self.s3_storage.save(file_path, image_file)

        # Guardar solo el nombre del archivo en la base de datos
        self.image = file_name
        return file_name  

    def get_image_url(self):
        """Devuelve la URL pública de la imagen almacenada en S3."""
        if self.image:
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/images/upload/{self.stand_id}/card/{self.image}"
        return None

    class Meta:
        db_table = 'cex_service_product'
