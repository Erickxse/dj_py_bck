from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Añade esta importación
from .serializers import CexQuotesSerializer
from .models import CexQuotes
from apps.stand.models import CexStand
from apps.service_product.models import CexServiceProduct
from django.shortcuts import get_object_or_404
from apps.authentication.utils import enviarCorreoNotificacionCotizacion



class CreateQuoteView(generics.CreateAPIView):
    serializer_class = CexQuotesSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        stand_id = kwargs.get('stand_id')
        service_product_id = kwargs.get('service_product_id')
        
        # Verificar que existan el stand y el producto/servicio
        stand = get_object_or_404(CexStand, pk=stand_id)
        service_product = get_object_or_404(CexServiceProduct, pk=service_product_id)
        
        # Agregar los IDs al request data
        request.data['stand_id'] = stand_id
        request.data['service_product_id'] = service_product_id
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quote = serializer.save()

        from apps.authentication.models import User
        user = User.objects.filter(stand_id=quote.stand_id).first()
    
        if user:
            dest_email = user.email
            print(f"[INFO] Email del dueño del stand: {dest_email}")

            datos_quote = {
                "quoted_by": quote.quoted_by,
                "quote_email": quote.quote_email,
                "quote_phone": quote.quote_phone,
                "service_product_no_of_items": quote.service_product_no_of_items,
                "quote_notes": quote.quote_notes,
            }

            # ✅ Enviar email envuelto en try/except
            try:
                enviarCorreoNotificacionCotizacion(dest_email, datos_quote)
            except Exception as e:
                print(f"[ERROR] Falló el envío del email de notificación: {e}")
        else:
            print(f"[WARN] No se encontró ningún User con stand_id={quote.stand_id}")

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'status': 'success',
                'message': 'Cotización creada exitosamente',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )