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
    default_recipe = serializers.ReadOnlyField(source='recipe.default_recipe')

    class Meta:
        model = RecipeInput
        fields = ('recipe_id','recipe_name', 'default_recipe', 'amount_min', 'amount', )

class ProductOutputSerializer(serializers.HyperlinkedModelSerializer):
    recipe_id = serializers.ReadOnlyField(source='recipe.id')
    recipe_name = serializers.ReadOnlyField(source='recipe.displayname')
    default_recipe = serializers.ReadOnlyField(source='recipe.default_recipe')

    class Meta:
        model = RecipeOutput
        fields = ('product_id',"product_name", 'amount', 'amount_min', 'mj', 'default_recipe', )

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeInputSerializer(source='recipeinput_set', many=True)
    products = RecipeOutputSerializer(source='recipeoutput_set', many=True)

    class Meta:
        model = Recipe
        fields = "__all__"
        depth = 1

class ProductBuildableSerializer(serializers.HyperlinkedModelSerializer):
    buildable_id = serializers.ReadOnlyField(source='buildable.id')
    buildable_name = serializers.ReadOnlyField(source='buildable.displayname')

    class Meta:
        model = RecipeOutput
        fields = ('buildable_id',"buildable_name", 'amount',  )

class ProductSerializer(serializers.ModelSerializer):
    needed_for = ProductInputSerializer(source='recipeinput_set', many=True)
    made_with = ProductInputSerializer(source='recipeoutput_set', many=True)
    needed_for_buildable = ProductBuildableSerializer(source='buildableingredient_set', many=True)

    class Meta:
        model = Product
        fields = "__all__"
        depth = 1

class BuildableIngredientSerializer(serializers.HyperlinkedModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    product_name = serializers.ReadOnlyField(source='product.displayname')

    class Meta:
        model = RecipeOutput
        fields = ('product_id',"product_name", 'amount', )

class BuildableSerializer(serializers.ModelSerializer):
    ingredients = BuildableIngredientSerializer(source='buildableingredient_set', many=True)

    class Meta:
        model = Buildable
        fields = "__all__"
        depth = 1
