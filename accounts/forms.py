from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import FileInput

from players.models import Player, Team

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
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(
        attrs={"class": "form-input form-control", "placeholder": "Имя", "autocomplete": "new-password"}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(
        attrs={"class": "form-input form-control", "placeholder": "Фамилия", "autocomplete": "new-password"}))
    username = forms.CharField(label="Логин", required=False, widget=forms.TextInput(
        attrs={"class": "form-input form-control", "placeholder": "Логин", "autocomplete": "new-password"}))
    email = forms.CharField(label="Email", widget=forms.TextInput(
        attrs={"class": "form-input form-control", "placeholder": "Email", "autocomplete": "new-password"}))
    team = forms.ModelChoiceField(label="Команда", queryset=Team.objects.all(), widget=forms.Select(
        attrs={"class": "form-input form-control", "placeholder": "Команда"}))
    phone_number = forms.CharField(label="Номер телефона", required=False, widget=forms.TextInput(
        attrs={"class": "form-input form-control", "placeholder": "Номер телефона", "autocomplete": "new-password"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(
        attrs={"class": "form-input form-control", "placeholder": "Пароль", "autocomplete": "new-password"}))
    password2 = forms.CharField(label="Пароль (подтверждение)", widget=forms.PasswordInput(
        attrs={"class": "form-input form-control", "placeholder": "Пароль (подтверждение)",
               "autocomplete": "new-password"}))

    def clean_username(self):
        return self.cleaned_data["username"] or None

    def clean_email(self):
        return self.cleaned_data["email"] or None

    def clean_phone_number(self):
        return self.cleaned_data["phone_number"] or None

    class Meta(UserCreationForm):
        model = User
        fields = ("first_name", "last_name", "email", "team", "username", "phone_number",)


class CustomUserChangeForm(forms.ModelForm):
    birth_date = forms.DateField(
        label="Дата рождения", widget=forms.widgets.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    height = forms.IntegerField(
        label="Рост", min_value=100, max_value=300, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    weight = forms.IntegerField(
        label="Вес", min_value=30, max_value=120, widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Player
        fields = ("birth_date", "height", "weight",)

    labels = {
        "birth_date": "Дата рождения",
        "height": "Рост",
        "weight": "Вес",
    }


class UserProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(
        widget=FileInput(attrs={"class": "btn nav-pills overlay fs-6 nav-pills mt-2 text-center"}), label="")

    class Meta:
        model = User
        fields = ("profile_image",)
