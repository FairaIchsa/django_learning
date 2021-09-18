from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Lead, Agent
from .forms import LeadModelForm, CustomUserCreationForm


class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "lead_create.html"
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


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm
    queryset = Lead.objects.all()
    success_url = reverse_lazy("leads:lead-list")


class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "lead_delete.html"
    queryset = Lead.objects.all()
    success_url = reverse_lazy("leads:lead-list")
