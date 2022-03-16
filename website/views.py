from django.shortcuts import render
from django.shortcuts import redirect
from django.forms import modelform_factory
from matplotlib.figure import Figure

from current.models import Russa, Aussie, TENS, FES, ITP, IBP, Microcorrente, Polarizada, CPAV
from current import textos
import matplotlib.pyplot as plt

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

current_description = {"TENS": textos.TENS,
         "ITP": textos.ITP,
         "IBP": textos.IBP,
        "FES": textos.FES,
         "russa": textos.russa, "aussie": textos.aussie,
         "microcorrente": textos.microcorrente,
         "polarizada": textos.polarizada,
        "CPAV": textos.CPAV
         }

def current(request, nome):

    figure = Figure(figsize=[10, 1], facecolor="white", tight_layout=True)
    if nome == 'russa':
        form = RussaForm
    elif nome == 'aussie':
        form = AussieForm

    elif nome == 'TENS':
        form = TENSForm

    elif nome == 'FES':
        form = FESForm

    elif nome == 'ITP':
        form = ITPForm

    elif nome == 'IBP':
        form = IBPForm

    elif nome == 'microcorrente':
        form = MicrocorrenteForm

    elif nome == 'polarizada':
        form = PolarizadaForm

    else:
        form = CPAVForm

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            corrente = form.save()
            t = corrente.get_t()
            wave = corrente.wave()
            subplot = figure.add_subplot(111)
            subplot.grid()
            subplot.plot(t, wave)

            #return redirect("welcome")

    return render(request, 'website/current.html', {"form": form, "nome": nome,
                                                    "description": current_description.get(nome),
                                                    "figure": 'aa'})

def login(request, nome):

    return render(request, 'website/current.html')