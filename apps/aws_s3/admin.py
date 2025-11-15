from django.contrib import admin
from django import forms
from .models import CexStand, CexServiceProduct
from django.core.exceptions import ValidationError
import os

class CexStandAdminForm(forms.ModelForm):
    image = forms.ImageField(required=False)  # Campo para seleccionar una imagen

    class Meta:
        model = CexStand
        fields = ['stand_name', 'description', 'img', 'image']

    def clean_image(self):
        image_file = self.cleaned_data.get('image')
        if image_file:
            # Validar tamaño máximo (5 MB)
            max_size = 5 * 1024 * 1024
            if image_file.size > max_size:
                raise ValidationError("La imagen no debe superar los 5 MB")

            # Validar extensiones permitidas
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            file_extension = os.path.splitext(image_file.name)[1].lower()
            if file_extension not in valid_extensions:
                raise ValidationError("El archivo debe ser una imagen con una de las siguientes extensiones: .jpg, .jpeg, .png, .gif, .bmp")
        return image_file

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'image' in self.cleaned_data and self.cleaned_data['image']:
            image_file = self.cleaned_data['image']
            try:
                image_name = instance.save_image_to_s3(image_file)  # Subir la imagen a S3 y obtener el nombre del archivo
                instance.img = image_name  # Guardamos solo el nombre del archivo en la base de datos
            except Exception as e:
                raise ValidationError(f"Error al guardar la imagen: {str(e)}")

        if commit:
            instance.save()

        return instance

class CexStandAdmin(admin.ModelAdmin):
    form = CexStandAdminForm
    list_display = ('id', 'stand_name', 'description', 'img')  # Mostramos la lista de stands con sus datos
    search_fields = ['stand_name', 'description']  # Permitir búsqueda de stands por nombre o descripción

    fields = ['stand_name', 'description', 'img', 'image']  # Aquí se definen los campos que puedes editar

    def get_readonly_fields(self, request, obj=None):
        """Solo permitir editar el campo de imagen"""
        if obj:  # Si el objeto existe (es decir, estamos editando un stand existente)
            return ['stand_name', 'description', 'img']  # Hacer estos campos solo lectura
        return []  # Si estamos creando un nuevo stand, todos los campos serán editables


admin.site.register(CexStand, CexStandAdmin)


class CexServiceProductAdminForm(forms.ModelForm):
    image = forms.ImageField(required=False)  # Campo para seleccionar una imagen

    class Meta:
        model = CexServiceProduct
        fields = ['name', 'description', 'price', 'image']  # Incluimos el campo para la imagen

    def clean_image(self):
        image_file = self.cleaned_data.get('image')
        if image_file:
            # Validar tamaño máximo (5 MB)
            max_size = 5 * 1024 * 1024
            if image_file.size > max_size:
                raise ValidationError("La imagen no debe superar los 5 MB")

            # Validar extensiones permitidas
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            file_extension = os.path.splitext(image_file.name)[1].lower()
            if file_extension not in valid_extensions:
                raise ValidationError("El archivo debe ser una imagen con una de las siguientes extensiones: .jpg, .jpeg, .png, .gif, .bmp")
        return image_file

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'image' in self.cleaned_data and self.cleaned_data['image']:
            image_file = self.cleaned_data['image']
            try:
                image_name = instance.save_image_to_s3(image_file)  # Subir la imagen a S3 y obtener el nombre del archivo
                instance.image = image_name  # Guardamos solo el nombre del archivo en la base de datos
            except Exception as e:
                raise ValidationError(f"Error al guardar la imagen: {str(e)}")

        if commit:
            instance.save()

        return instance

class CexServiceProductAdmin(admin.ModelAdmin):
    form = CexServiceProductAdminForm
    list_display = ('id', 'name', 'description', 'price', 'image', 'images')  # Mostramos la lista de productos con sus datos
    search_fields = ['name', 'description']  # Permitir búsqueda de productos por nombre o descripción

    fields = ['image']  # Aquí se definen los campos que puedes editar

admin.site.register(CexServiceProduct, CexServiceProductAdmin)