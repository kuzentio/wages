from django.contrib import admin

from vegetable.models import Vegetable


@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    readonly_fields = ['slug', ]
