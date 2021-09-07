from django.urls import path

from .views import lead_list, lead_detail, lead_create, lead_update

app_name = "leads"

urlpatterns = [
    path('', lead_list),
    path('<int:pk>/', lead_detail),  # int нужно для того, чтобы create не воспринималось, как pk
    path('<int:pk>/update/', lead_update),
    path('create/', lead_create),
]