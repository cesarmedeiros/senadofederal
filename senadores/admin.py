from django.contrib import admin

from .models import Parlamentar, Partido, Mandato, Exercicio
# Register your models here.

admin.site.register(Parlamentar)
admin.site.register(Partido)
admin.site.register(Mandato)
admin.site.register(Exercicio)