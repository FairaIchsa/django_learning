from django.contrib import admin
from django.urls import path, include
from leads.function_based_views import landing_page
from leads.class_based_views import LandingPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('leads/', include('leads.urls', namespace="leads"))
]
