from django.shortcuts import render, redirect, get_object_or_404

from visitantes.forms import (
    VisitanteForm, AutorizaVisitanteForm
)

from porteiros.models import Porteiro
from visitantes.models import Visitante
from django.contrib import messages

from django.utils import timezone

def registrar_visitante(request):
    form = VisitanteForm()

    if request.method == "POST":
        form = VisitanteForm(request.POST)

        if form.is_valid():
            visitante = form.save(commit = False)
            visitante.registrado_por = Porteiro.objects.get(id=1)

            visitante.save()

            messages.success(
                request,
                "O Visitante foi registrado com sucesso!"
            )
            
            return redirect("index")

    context = {
        "nome_pagina": "Registrar visitante",
        "form": form,
    }

    return render(request, "registrar_visitante.html", context)

def informacoes_visitante(request, id):
    visitante = get_object_or_404(
        Visitante,
        id=id
    )

    form = AutorizaVisitanteForm()

    if request.method == "POST":
        form = AutorizaVisitanteForm(
            request.POST,
            instance=visitante
        )

        if form.is_valid():
            visitante = form.save(commit=False)

            visitante.status = "EM_VISITA"
            visitante.horario_autorizacao = timezone.now()
            visitante.save()

            messages.success(
                request,
                "Visitante autorizado com sucesso"
            )

            return redirect("index")

    context = {
        "nome_pagina": "Informações do Visitante",
        "visitante": visitante,
        "form": form,
    }

    return render(request, "informacoes_visitante.html", context)

def finalizar_visita(request, id):
    if request.method=="POST":
        visitante = get_object_or_404(
        Visitante,
        id=id
    )

    visitante.status = "FINALIZADO" 
    visitante.horario_saida = timezone.now()

    visitante.save()

    messages.success(
        request,
        "Visita finalizada com sucesso" 
    )

    return redirect("index")