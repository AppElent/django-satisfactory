from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from .models import *
#from ..permissions import IsOwner

class RecipeViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer 
    #filterset_fields = ('category', 'application', 'severity')
    #ordering_fields = ['category', 'severity']

class ProductViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 

class MachineTypeViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = MachineType.objects.all()
    serializer_class = MachineTypeSerializer 
