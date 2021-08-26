from django.urls import path

from .views import (SalesManagerListView,
                    SalesManagerCreateView,
                    SalesManagerDetailView,
                    SalesManagerUpdateView,
                    SalesManagerDeleteView)

app_name = 'salesmanagers'

urlpatterns = [
    path('', SalesManagerListView.as_view(), name='salesmanager-list'),
    path('create/', SalesManagerCreateView.as_view(), name='salesmanager-create'),
    path('<int:pk>/detail/', SalesManagerDetailView.as_view(), name='salesmanager-detail'),
    path('<int:pk>/update/', SalesManagerUpdateView.as_view(), name='salesmanager-update'),
    path('<int:pk>/delete/', SalesManagerDeleteView.as_view(), name='salesmanager-delete'),

]
