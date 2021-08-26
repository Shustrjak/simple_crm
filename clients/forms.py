from django import forms
from django.contrib.auth import get_user_model
from .models import Client, SalesManager
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()


class ClientModelForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'email',
            'organisation',
            'sales_manager',
            'description',
            'phoned',
            'spec_files',

        )


class ClientForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()



class CustomUserUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class AssignSalesManagerForm(forms.Form):
    sales_manager = forms.ModelChoiceField(queryset=SalesManager.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        sales_managers = SalesManager.objects.filter(organisation=request.user.userprofile)
        super(AssignSalesManagerForm, self).__init__(*args, **kwargs)
        self.fields["sales_manager"].queryset = sales_managers


class ClientCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = 'category',
