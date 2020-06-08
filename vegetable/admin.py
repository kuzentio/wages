from django.contrib import admin

from vegetable.models import Vegetable, VegetableImage


@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    readonly_fields = ['slug', ]


@admin.register(VegetableImage)
class VegetableImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']
    # readonly_fields = ['slug', ]
