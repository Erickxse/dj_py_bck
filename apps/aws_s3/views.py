from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import CexStand, CexServiceProduct
import json

def get_image(request, stand_id):
    # Obtener el objeto CexStand con el ID proporcionado
    stand = get_object_or_404(CexStand, id=stand_id)
    return JsonResponse({'image_url': stand.get_image_url()})

def delete_image(request, stand_id):
    # Obtener el objeto CexStand con el ID proporcionado
    stand = get_object_or_404(CexStand, id=stand_id)
    stand.img = None  # Elimina el nombre de la imagen
    stand.save()  # Guarda los cambios
    return JsonResponse({'message': 'Image deleted successfully'})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_image(request, stand_id):
    """
    Endpoint para subir una imagen a un stand específico.
    Requiere autenticación por token.
    """
    try:
        # Obtener el stand
        stand = get_object_or_404(CexStand, id=stand_id)
        
        # Verificar que el usuario tiene permiso para modificar este stand
        # Aquí puedes añadir tu lógica de permisos según tu modelo de datos
        
        # Obtener la imagen del request
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No se ha proporcionado ninguna imagen'}, status=400)
            
        image_file = request.FILES['image']
        
        try:
            # Guardar la imagen en S3
            image_name = stand.save_image_to_s3(image_file)
            
            # Actualizar el campo img en el modelo
            stand.img = image_name
            stand.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Imagen subida correctamente',
                'image_name': image_name,
                'image_url': stand.get_image_url()
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    except Exception as e:
        return JsonResponse({'error': f'Error al procesar la solicitud: {str(e)}'}, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_product_image(request, stand_id, product_id):
    """
    Endpoint para subir una imagen a un producto específico.
    """
    try:
        stand_id = int(stand_id)  # Asegurar que sean números
        product_id = int(product_id)

        product = get_object_or_404(CexServiceProduct, stand_id=stand_id, id=product_id)

        # Validar si se ha enviado un archivo
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No se ha proporcionado ninguna imagen'}, status=400)

        image_file = request.FILES['image']

        try:
            # Guardar la imagen en S3 y obtener el nombre del archivo
            image_name = product.save_image_to_s3(image_file)

            # Actualizar el campo `image` con la nueva imagen (principal)
            product.image = image_name

            # 🟢 Actualizar el campo `images`, agregando la nueva imagen separada por comas
            if product.images:
                product.images = f"{product.images},{image_name}"  # Agrega la nueva imagen
            else:
                product.images = image_name  # Primera imagen

            product.save()

            return JsonResponse({
                'success': True,
                'image_url': product.get_image_url(),
                'all_images': product.images  # Devolver la lista completa de imágenes
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    except ValueError:
        return JsonResponse({'error': 'stand_id o product_id no son números válidos'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error al procesar la solicitud: {str(e)}'}, status=500)
