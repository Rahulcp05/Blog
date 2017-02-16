from django.contrib import admin

from .models import Item,Comment
class ItemAdmin(admin.ModelAdmin):
    list_display=['title','updated','created',]
    list_filter=['updated','created',]
    search_fields = ['title',]
admin.site.register(Item,ItemAdmin)
