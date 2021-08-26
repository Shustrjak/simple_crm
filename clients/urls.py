
from django.urls import path
from .views import (ClientListView,
                    ClientDetailView,
                    ClientCreateView,
                    ClientUpdateView,
                    ClientDeleteView,
                    AssignSalesManagerView,
                    CategoryListView,
                    CategoryDetailView,
                    ClientCategoryUpdateView
                    )

app_name = "clients"

urlpatterns = [
    path('', ClientListView.as_view(), name='client-list'),
    path('create/', ClientCreateView.as_view(), name='client-create'),
    path('<int:pk>/detail/', ClientDetailView.as_view(), name='client-detail'),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
    path('<int:pk>/assign-sales/', AssignSalesManagerView.as_view(), name='assign-sales'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/detail/', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:pk>/category/', ClientCategoryUpdateView.as_view(), name='category-update'),
]


