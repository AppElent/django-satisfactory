from rest_framework import serializers
from .models import *

class RecipeInputSerializer(serializers.HyperlinkedModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    product_name = serializers.ReadOnlyField(source='product.displayname')

    class Meta:
        model = RecipeInput
        fields = ('product_id',"product_name", 'amount', 'amount_min', )
        #fields = "__all__"

class RecipeOutputSerializer(serializers.HyperlinkedModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    product_name = serializers.ReadOnlyField(source='product.displayname')

    class Meta:
        model = RecipeOutput
        fields = ('product_id',"product_name", 'amount', 'amount_min', 'mj', )

class ProductInputSerializer(serializers.HyperlinkedModelSerializer):
    recipe_id = serializers.ReadOnlyField(source='recipe.id')
    recipe_name = serializers.ReadOnlyField(source='recipe.displayname')

    class Meta:
        model = RecipeInput
        fields = ('recipe_id','recipe_name', 'amount_min', 'amount', )

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeInputSerializer(source='recipeinput_set', many=True)
    products = RecipeOutputSerializer(source='recipeoutput_set', many=True)

    class Meta:
        model = Recipe
        #fields = ['id', 'title', 'author']
        fields = "__all__"
        #exclude = ['user']
        depth = 1

class ProductSerializer(serializers.ModelSerializer):
    products_in = ProductInputSerializer(source='recipe_input', many=True)

    class Meta:
        model = Product
        #fields = ['id', 'title', 'author']
        fields = "__all__"
        #exclude = ['user']
        depth = 1

class BuildableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Buildable
        #fields = ['id', 'title', 'author']
        fields = "__all__"
        #exclude = ['user']
        depth = 1
