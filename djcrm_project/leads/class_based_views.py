from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from agents.mixins import OrganiserMixin

from .models import Lead
from .forms import LeadModelForm, CustomUserCreationForm


class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation__user=user)
        elif user.is_agent:
            queryset = Lead.objects.filter(agent__user=user)      # а не agent=Agent.objects.get(user=user)
        return queryset


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation__user=user)
        elif user.is_agent:
            queryset = Lead.objects.filter(agent__user=user)
        return queryset


class LeadCreateView(OrganiserMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    success_url = reverse_lazy("leads:lead-list")

    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]   # обязательно список или кортеж
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganiserMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    context_object_name = "lead"
    success_url = reverse_lazy("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organisation__user=user)
        return queryset


class LeadDeleteView(OrganiserMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    context_object_name = "lead"
    success_url = reverse_lazy("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organisation__user=user)
        return queryset
