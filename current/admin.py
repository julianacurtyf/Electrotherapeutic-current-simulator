from django.contrib import admin

# Register your models here.

from .models import Russa, Aussie, TENS, FES, ITP, IBP, Microcorrente, Polarizada, CPAV

admin.site.register(Russa)
admin.site.register(Aussie)
admin.site.register(TENS)
admin.site.register(FES)
admin.site.register(ITP)
admin.site.register(IBP)
admin.site.register(Microcorrente)
admin.site.register(Polarizada)
admin.site.register(CPAV)