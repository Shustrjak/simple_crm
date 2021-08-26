import random

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .mixins import OrganisorAndRequiredMixin
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView)

from clients.models import SalesManager
from .forms import SalesManagerModelForm


class SalesManagerListView(OrganisorAndRequiredMixin, ListView):
    template_name = 'salesmanagers/salesmanager_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return SalesManager.objects.filter(organisation=organisation)


class SalesManagerCreateView(OrganisorAndRequiredMixin, CreateView):
    template_name = 'salesmanagers/salesmanager_create.html'
    form_class = SalesManagerModelForm

    def get_success_url(self):
        return reverse("salesmanagers:salesmanager-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_salesmanager = True
        user.is_organisor = False
        user.set_password(f'{random.randint(0, 1000000)}')
        user.save()
        SalesManager.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject='Invite you',
            message=('You added as an agent on SimpleCRM. Password ' + str(
                user.set_password(f"{random.randint(0, 1000000)}"))),
            from_email='admin@admin.admin',
            recipient_list=[user.email],

        )

        return super(SalesManagerCreateView, self).form_valid(form)


class SalesManagerDetailView(OrganisorAndRequiredMixin, DetailView):
    template_name = 'salesmanagers/salesmanager_detail.html'

    def get_queryset(self):
        return SalesManager.objects.all()

    context_object_name = "salesmanager"


class SalesManagerUpdateView(OrganisorAndRequiredMixin, UpdateView):
    template_name = 'salesmanagers/salesmanager_update.html'
    form_class = SalesManagerModelForm

    # TODO get_queryset?
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return SalesManager.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse("salesmanagers:salesmanager-list")


class SalesManagerDeleteView(OrganisorAndRequiredMixin, DeleteView):
    template_name = 'salesmanagers/salesmanager_delete.html'

    def get_queryset(self):
        return SalesManager.objects.all()

    def get_success_url(self):
        return reverse("salesmanagers:salesmanagers")
