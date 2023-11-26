from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class AuthBackend(ModelBackend):
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username) |
                Q(phone_number__iexact=username)
            )
        except User.DoesNotExist:
            return None
        return user if user.check_password(password) else None
