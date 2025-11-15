from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import CexInboxSerializer

class CexInboxCreateView(APIView):
    permission_classes = [AllowAny]  # Esto desactiva la autenticación para esta vista

    def post(self, request, format=None):
        serializer = CexInboxSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            # Volvemos a serializar el objeto guardado para obtener todos sus campos (ya con country_id y mailed_it)
            response_serializer = CexInboxSerializer(instance)
            return Response(response_serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
