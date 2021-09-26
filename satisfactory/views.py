from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .serializers import *
from .models import *
#from ..permissions import IsOwner

class RecipeViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer 
    filterset_fields = ('version', 'displayname')
    ordering_fields = ['displayname']
    search_fields = ['displayname']

    @method_decorator(cache_page(60*60))
    def dispatch(self, request, *args, **kwargs):
        cache.set('test123', 'value123')
        print(cache.getKeys())
        return super().dispatch(request, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ('version', 'displayname')

class BuildableViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Buildable.objects.all()
    serializer_class = BuildableSerializer
    filterset_fields = ('version', 'displayname')
