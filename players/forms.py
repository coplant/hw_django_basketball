from django import forms

from players.models import Match


class PlayerStatForm(forms.Form):
    match = forms.ModelChoiceField(queryset=Match.objects.all(), label="Матч")
    points = forms.IntegerField(label="Очки")
    # Добавьте остальные поля для статистики
