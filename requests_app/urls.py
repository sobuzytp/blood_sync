from django.urls import path

from . import views

app_name = 'requests_app'

urlpatterns = [
    path('', views.request_list_view, name='list'),
    path('create/', views.request_create_view, name='create'),
    path('my-requests/', views.my_requests_view, name='my_requests'),
    path('<int:pk>/', views.request_detail_view, name='detail'),
    path('<int:pk>/edit/', views.request_edit_view, name='edit'),
    path('<int:pk>/delete/', views.request_delete_view, name='delete'),
    path('<int:pk>/status/', views.request_status_update_view, name='status_update'),
]
