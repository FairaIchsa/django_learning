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
    print(pk)
    lead = Lead.objects.get(id=pk)
    print(lead)
    return HttpResponse("Detail view")

