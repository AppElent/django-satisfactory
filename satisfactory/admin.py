from django.contrib import admin
from .models import *

class RecipeInputInline(admin.TabularInline):
    model = RecipeInput
    extra = 1

class RecipeOutputInline(admin.TabularInline):
    model = RecipeOutput
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeInputInline, RecipeOutputInline)
    exclude = ('key',)

class ProductAdmin(admin.ModelAdmin):
    exclude = ('key',)

class BuildableAdmin(admin.ModelAdmin):
    exclude = ('key',)

class NodeTypeAdmin(admin.ModelAdmin):
    exclude = ('key',)


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Buildable, BuildableAdmin)
#admin.site.register(RecipeInput)
#admin.site.register(RecipeOutput)
admin.site.register(NodeType, NodeTypeAdmin)