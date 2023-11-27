from django.contrib import admin

from .models import Bandeco, Item, Nota, Comentario

admin.site.register(Bandeco)
admin.site.register(Item)
admin.site.register(Nota)
admin.site.register(Comentario)