from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from django.views import generic
from .models import Lead, Agent
from .forms import LeadModelForm


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = {
            "User": self.request.user
        }
        return context


class LeadListView(generic.ListView):
    template_name = "lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"


class LeadDetailView(generic.DetailView):
    template_name = "lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


class LeadCreateView(generic.CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm
    success_url = reverse_lazy("leads:lead-list")


class LeadUpdateView(generic.UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm
    queryset = Lead.objects.all()
    success_url = reverse_lazy("leads:lead-list")


class LeadDeleteView(generic.DeleteView):
    template_name = "lead_delete.html"
    queryset = Lead.objects.all()
    success_url = reverse_lazy("leads:lead-list")
