from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead


def lead_list(request):
    Leads = Lead.objects.all()
    context = {
        "leads": Leads
    }
    return render(request, "lead_list.html", context)


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "lead_detail.html", context)

