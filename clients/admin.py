from django.contrib import admin

# Register your models here.
from .models import Client, SalesManager, User, UserProfile, Category


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = "id", "full_name", "sales_manager", "organisation", "email"
    list_display_links = "id", "full_name"
    # date_hierarchy = 'date'
    # """ Добавить свойство-фильтр( date=models.DateField(auto_now=True) ) по дате добавления"""


@admin.register(SalesManager)
class SalesManagerAdmin(admin.ModelAdmin):
    list_display = "id", "user"
    list_display_links = "id", "user"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = "id", "username"
    list_display_links = "id", "username"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "id", "name"
    list_display_links = list_display


# @admin.register(UserProfile)
# class UserAdmin(admin.ModelAdmin):
#     list_display = "id", "user.username"
#     list_display_links = "id", "user.username"

admin.site.register(UserProfile)
# admin.site.register(Category)
admin.site.site_header = "CRM Admin"
admin.site.site_title = "CRM Admin Portal"
admin.site.index_title = "Welcome to CRM Portal"
