from django.shortcuts import render
from django.shortcuts import redirect
from django.forms import modelform_factory
from json import dumps

from current.models import Russa, Aussie, TENS, FES, ITP, IBP, Microcorrente, Polarizada, CPAV
from current import textos

# Create your views here.

def welcome(request):
    return render(request, 'website/welcome.html')

RussaForm = modelform_factory(Russa, exclude=[], labels={'intensity': 'Intensidade (0-140mA)', 'carrier': 'Frequência (2500Hz)', 'timer': 'Tempo (s)', 'burst_hz': 'Frequência de burst (1-100Hz)', 'rise':'Tempo de subida (1-20s)', 'decay':'Tempo de descida (1-20s)', 'duty':'Trabalho (%)', 'on':'ON (1-60s)', 'off': 'OFF (1-60s)'})
AussieForm = modelform_factory(Aussie, exclude=[], labels={'intensity': 'Intensidade (0-140mA)', 'carrier': 'Frequência (1000 ou 4000Hz)', 'timer': 'Tempo (s)', 'burst_ms': 'Duração do burst (2 ou 4 ms)', 'burst_hz': 'Frequência de burst (1-100Hz)', 'rise':'Tempo de subida (1-20s)', 'decay':'Tempo de descida (1-20s)', 'on':'ON (1-60s)', 'off': 'OFF (1-60s)'})
TENSForm = modelform_factory(TENS, exclude=[], labels={'intensity': 'Intensidade (0-140mA)', 'carrier': 'Frequência (1-250Hz)', 'timer': 'Tempo (s)', 'mode': 'Modo', 'fase': 'Fase (50-500 micros)'})
FESForm = modelform_factory(FES, exclude=[], labels={'intensity': 'Intensidade (0-140mA)', 'carrier': 'Frequência (0.5-250Hz)', 'timer': 'Tempo (s)', 'rise': 'Tempo de subida (1-20s)', 'decay': 'Tempo de descida (1-20s)','fase': 'Fase (0.00005-0.0005s)', 'on':'ON (1-60s)', 'off': 'OFF (1-60s)'})
ITPForm = modelform_factory(ITP, exclude=[], labels={'intensity': 'Intensidade (0-140mA)', 'carrier': 'Frequência (1, 2, 3, 8 ou 10Hz)', 'timer': 'Tempo (s)', 'AMF': 'AMF (1-200Hz)', 'sweep_hz': 'Frequência de sweep (1-200Hz)', 'sweep_s': 'Modo do sweep'})
IBPForm = modelform_factory(IBP, exclude=[], labels={'intensity': 'Intensidade (0-140mA)', 'carrier': 'Frequência (1, 2, 3, 8 ou 10Hz)', 'timer': 'Tempo (s)', 'AMF': 'AMF (1-200Hz)', 'sweep_hz': 'Frequência de sweep (1-200Hz)', 'sweep_s': 'Modo do sweep','rise': 'Tempo de subida (1-20s)', 'decay': 'Tempo de descida (1-20s)', 'on':'ON (1-60s)', 'off': 'OFF (1-60s)'})
MicrocorrenteForm = modelform_factory(Microcorrente,exclude=[], labels={'intensity': 'Intensidade (0-0.99mA)', 'carrier': 'Frequência (15000Hz)', 'timer': 'Tempo (s)', 'freq': 'Frequência de burst (0.1-500Hz)'})
PolarizadaForm = modelform_factory(Polarizada,exclude=[], labels={'intensity': 'Intensidade (0-30mA)', 'carrier': 'Frequência (15000Hz)', 'timer': 'Tempo (s)'})
CPAVForm = modelform_factory(CPAV,exclude=[], labels={'intensity': 'Intensidade (1-400mA)', 'carrier': 'Frequência (15000Hz)', 'timer': 'Tempo (s)', 'rise':'Tempo de subida (1-20s)', 'decay':'Tempo de descida (1-20s)', 'on':'ON (1-60s)', 'off': 'OFF (1-60s)'})

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
            values = []
            for i in range(len(t)):
                data = {'t': t[i],
                        'wave': wave[i]}
                values.append(data)
            
            dataJSON = dumps(values)
            return render(request, 'website/current.html', {"form": form, "nome": nome,
                                                            "description": current_description.get(nome),
                                                            "data": dataJSON,
                                                            "wave": wave})
    else:
        return render(request, 'website/current.html', {"form": form, "nome": nome,
                                                            "description": current_description.get(nome)})

def login(request, nome):

    return render(request, 'website/current.html')