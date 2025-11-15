from django.shortcuts import render
from .models import CexCategory
from apps.service_product.models import CexServiceProduct
from apps.stand.models import CexStand
from .serializers import CategorySerializer, CategoryTreeSerializer, CategoryCarouselSerializer, CategorySubSerializerProd
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from rest_framework.views import APIView

# Create your views here.

class CategoryView(viewsets.ModelViewSet):
    queryset = CexCategory.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer


from rest_framework.response import Response

class CategoryCarouselView(viewsets.ModelViewSet):
    queryset = CexCategory.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoryCarouselSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        if slug:
            try:
                # Buscar la categoría de nivel 1 usando el slug
                category_level_1 = CexCategory.objects.filter(slug=slug, level=1).first()
                if category_level_1:
                    return self.queryset.filter(parent_id=category_level_1.id, level=2)
                
                # Buscar la categoría de nivel 2 usando el slug
                category_level_2 = CexCategory.objects.filter(slug=slug, level=2).first()
                if category_level_2:
                    return self.queryset.filter(parent_id=category_level_2.id, level=3)
                
                return CexCategory.objects.none()
            except CexCategory.DoesNotExist:
                return CexCategory.objects.none()
        else:
            return CexCategory.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No existen categorías relacionadas."}, status=200)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)





class CategoryTreeView(viewsets.ModelViewSet):
    print("STARTED CATEGORY TREE VIEW")
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoryTreeSerializer

    def list(self, request):
        categories = CexCategory.objects.all().order_by('level', 'parent_id', 'name')

        def build_tree(parent_id, categories, level):
            tree = []
            children = [cat for cat in categories if cat.parent_id == parent_id]
            for child in children:
                node = {
                    'id': child.id,
                    'name': child.name,
                    'description': child.description,
                    'short_description': child.short_description,
                    'img': child.img,
                    'level': child.level,
                    'slug': child.slug,
                    'parent_id': child.parent_id,
                    # Cambiar el nombre de la clave según el nivel
                    f'children_{level + 1}': build_tree(child.id, categories, child.level + 1)
                }
                tree.append(node)
            return tree

        # Construir el árbol empezando por las categorías principales
        category_tree = build_tree(0, categories, 1)

        # Serializar el árbol
        serializer = self.get_serializer(category_tree, many=True)
        print("finished serializing")
        return Response(serializer.data)


    

class CategorySubView(viewsets.ModelViewSet):
    queryset = CexServiceProduct.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySubSerializerProd

    def get_queryset(self):
        print("estoy entrando aqui")
        # Recuperar el slug desde los argumentos de la URL
        slug = self.kwargs.get('slug')
        print(f"Slug recibido: {slug}")  # Para depuración

        # Buscar la categoría correspondiente en CexCategory con el slug
        try:
            category = CexCategory.objects.get(slug=slug)
            print(f"Categoría encontrada: {category.name} con ID: {category.id}")  # Depuración
        except CexCategory.DoesNotExist:
            print(f"No se encontró ninguna categoría con el slug: {slug}")
            return CexServiceProduct.objects.none()  # Retorna un queryset vacío si no existe la categoría

        # Filtrar productos por category_id
        queryset = self.queryset.filter(category_id=category.id)
        print(f"Productos encontrados: {queryset.count()}")  # Para depuración

        return queryset

        