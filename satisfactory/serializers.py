from rest_framework import serializers
from .models import *

class RecipeInputSerializer(serializers.HyperlinkedModelSerializer):
    product_key = serializers.ReadOnlyField(source='product.key')
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = RecipeInput
        fields = ('product_key',"product_name", 'amount',  )
        #fields = "__all__"

class RecipeOutputSerializer(serializers.HyperlinkedModelSerializer):
    product_key = serializers.ReadOnlyField(source='product.key')
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = RecipeOutput
        fields = ('product_key',"product_name", 'amount', )

class RecipeSerializer(serializers.ModelSerializer):
    products_in = RecipeInputSerializer(source='recipeinput_set', many=True)
    products_out = RecipeOutputSerializer(source='recipeoutput_set', many=True)

    class Meta:
        model = Recipe
        #fields = ['id', 'title', 'author']
        fields = "__all__"
        #exclude = ['user']

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        #fields = ['id', 'title', 'author']
        fields = "__all__"
        #exclude = ['user']

class MachineTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MachineType
        #fields = ['id', 'title', 'author']
        fields = "__all__"
        #exclude = ['user']
        depth = 3
