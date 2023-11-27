from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
                  path("me/", views.me_view, name="me"),
                  path("login/", views.login_view, name="login"),
                  path("logout/", views.logout_view, name="logout"),
                  path("signup/", views.register_view, name="register"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
