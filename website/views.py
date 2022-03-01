from django.shortcuts import render
from django.forms import modelform_factory
from current.models import Russa, Aussie, TENS, FES, ITP, IBP, Microcorrente, Polarizada, CPAV
# Create your views here.

def welcome(request):
    return render(request, 'website/welcome.html')

RussaForm = modelform_factory(Russa, exclude=[])
AussieForm = modelform_factory(Aussie, exclude=[])
TENSForm = modelform_factory(TENS, exclude=[])
FESForm = modelform_factory(FES, exclude=[])
ITPForm = modelform_factory(ITP, exclude=[])
IBPForm = modelform_factory(IBP, exclude=[])
MicrocorrenteForm = modelform_factory(Microcorrente,exclude=[])
PolarizadaForm = modelform_factory(Polarizada,exclude=[])
CPAVForm = modelform_factory(CPAV,exclude=[])

def current(request, nome):

    return render(request, 'website/current.html')

def login(request, nome):

    return render(request, 'website/current.html')