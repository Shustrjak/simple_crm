from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    DetailView, FormView
)

from clients.models import Client, Category
from salesmanagers.mixins import OrganisorAndRequiredMixin
from .forms import ClientModelForm, CustomUserUserCreationForm, AssignSalesManagerForm, \
    ClientCategoryUpdateForm


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = "landing.html"


class ClientListView(LoginRequiredMixin, ListView):
    template_name = "clients/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        user = self.request.user

        # init queryset
        if user.is_organisor:
            queryset = Client.objects.filter(
                organisation=user.userprofile,
                sales_manager__isnull=False)
        else:
            queryset = Client.objects.filter(
                organisation=user.salesmanager.organisation,
                sales_manager__isnull=False)
            # filtering
            queryset = queryset.filter(sales_manager__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Client.objects.filter(organisation=user.userprofile,
                                             sales_manager__isnull=True)
            context.update({
                "unassigned_clients": queryset,
            })
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = "clients/client_detail.html"
    context_object_name = "client"

    def get_queryset(self):
        user = self.request.user

        # init queryset
        if user.is_organisor:
            queryset = Client.objects.filter(organisation=user.userprofile)
        else:
            queryset = Client.objects.filter(organisation=user.salesmanager.organisation)
            # filtering
            queryset = queryset.filter(sales_manager__user=user)
        return queryset


class ClientCreateView(OrganisorAndRequiredMixin, CreateView):
    template_name = "clients/client_create.html"
    form_class = ClientModelForm

    def get_success_url(self):
        return reverse("clients:client-list")

    def form_valid(self, form):
        client = form.save(commit=False)
        client.organisation = self.request.user.userprofile
        client.save()
        send_mail(
            subject='one',
            message='two',
            from_email='sale@lubimie-aromati.ru',
            recipient_list=[
                'sale@lubimie-aromati.ru'
            ],

        )
        return super(ClientCreateView, self).form_valid(form)


class ClientUpdateView(OrganisorAndRequiredMixin, UpdateView):
    template_name = "clients/client_update.html"
    form_class = ClientModelForm

    def get_queryset(self):
        user = self.request.user
        # init queryset
        return Client.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("clients:client-list")


class ClientDeleteView(OrganisorAndRequiredMixin, DeleteView):
    template_name = "clients/client_delete.html"

    def get_queryset(self):
        user = self.request.user
        # init queryset
        return Client.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("clients:client-list")


class AssignSalesManagerView(OrganisorAndRequiredMixin, FormView):
    template_name = "clients/assign_sales.html"
    form_class = AssignSalesManagerForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignSalesManagerView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("clients:client-list")

    def form_valid(self, form):
        sales_manager = form.cleaned_data["sales_manager"]
        client = Client.objects.get(id=self.kwargs["pk"])
        client.sales_manager = sales_manager
        client.save()
        return super(AssignSalesManagerView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "categories/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Client.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Client.objects.filter(
                organisation=user.salesmanager.organisation)

        context.update({
            "unassigned_client_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user

        # init queryset
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(
                organisation=user.salesmanager.organisation)
        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "categories/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user

        # init queryset
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(
                organisation=user.salesmanager.organisation)
        return queryset


class ClientCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "categories/category_update.html"

    form_class = ClientCategoryUpdateForm


    def get_queryset(self):
        user = self.request.user

        # init queryset
        if user.is_organisor:
            queryset = Client.objects.filter(organisation=user.userprofile)
        else:
            queryset = Client.objects.filter(organisation=user.salesmanager.organisation)
            # filtering
            queryset = queryset.filter(sales_manager__user=user)
        return queryset

    def get_success_url(self):
        return reverse("clients:client-detail", kwargs={'pk': self.get_object().id})

class ClientFileView(TemplateView):
    pass

