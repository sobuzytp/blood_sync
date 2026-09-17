from django.urls import path

from . import views

app_name = 'donors'

urlpatterns = [
    path('', views.donor_list_view, name='list'),
    path('become/', views.donor_create_view, name='create'),
    path('<int:pk>/', views.donor_detail_view, name='detail'),
    path('<int:pk>/edit/', views.donor_edit_view, name='edit'),
    path('<int:pk>/delete/', views.donor_delete_view, name='delete'),
]
