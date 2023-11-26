from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("accounts.urls")),
    re_path(r'^.*/$', lambda request: redirect("home", permanent=True)),
]
