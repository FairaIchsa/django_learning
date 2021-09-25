from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from agents.mixins import OrganiserMixin

from .models import Lead, Category
from .forms import LeadModelForm, AssignAgentForm, CustomUserCreationForm, LeadCategoryUpdateForm


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
            queryset = Lead.objects.filter(
                organisation__user=user,
                agent__isnull=False
            )
        elif user.is_agent:
            queryset = Lead.objects.filter(
                agent__user=user,
                agent__isnull=False
            )   # а не agent=Agent.objects.get(user=user)
        return queryset
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.organisation,
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset,
            })
        return context


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


class AssignAgentView(generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm
    success_url = reverse_lazy("leads:lead-list")

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_organiser:
            leads = Lead.objects.filter(organisation=user.organisation)
        else:
            leads = Lead.objects.filter(organisation=user.agent.organisation)

        context.update({
            "unassigned_lead_count": leads.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.organisation)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #
    #     leads = self.get_object().leads.all()   # leads взято из related_name поля category модели Lead
    #
    #     context.update({
    #         "leads": leads,
    #     })
    #     return context
    #     Можно заменить выражением category.leads.all в шаблоне category_detail.html

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.organisation)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation__user=user)
        elif user.is_agent:
            queryset = Lead.objects.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse_lazy("leads:lead-detail", kwargs={"pk": self.get_object().pk})
