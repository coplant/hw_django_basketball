from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import FileInput

User = get_user_model()


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(
        attrs={"class": "form-input form-control", "placeholder": "Логин"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(
        attrs={"class": "form-input form-control", "placeholder": "Пароль"}))

    class Meta:
        model = User
        fields = ("username", "password")

    def is_valid(self):
        result = super().is_valid()
        for x in (self.fields if "__all__" in self.errors else self.errors):
            attrs = self.fields[x].widget.attrs
            attrs.update({"class": attrs.get("class", "") + " is-invalid"})
        return result


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ("username", "email", "phone_number",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "phone_number",)


class UserProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(
        widget=FileInput(attrs={"class": "btn nav-pills overlay fs-6 nav-pills mt-2 text-center"}), label="")

    class Meta:
        model = User
        fields = ("profile_image",)
