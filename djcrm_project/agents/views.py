from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
import random

from leads.models import Agent

from .forms import AgentModelForm
from .mixins import OrganiserMixin


class AgentListView(OrganiserMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    context_object_name = "agents"

    def get_queryset(self):
        organisation = self.request.user.organisation
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganiserMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    success_url = reverse_lazy("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.organisation
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on DJCRM. Please login to start working.",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )

        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganiserMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.organisation
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganiserMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    context_object_name = "agent"
    success_url = reverse_lazy("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.organisation
        return Agent.objects.filter(organisation=organisation)


class AgentDeleteView(OrganiserMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"
    success_url = reverse_lazy("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.organisation
        return Agent.objects.filter(organisation=organisation)

