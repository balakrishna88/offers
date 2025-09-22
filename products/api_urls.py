# products/urls.py
from django.urls import path

from products.api_views import trending_api
from . import views


urlpatterns = [
    path("trending/", trending_api, name="trending_api"),
]
