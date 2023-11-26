from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from players import models


@admin.register(models.Player)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "link_to_user", "team", "number", "birth_date")

    def link_to_user(self, obj):
        link = reverse("admin:accounts_customuser_change", args=[obj.user_id])
        return format_html('<a href="{}">{}</a>', link, obj.user.username)

    link_to_user.short_description = 'Edit user'


@admin.register(models.Team)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    ordering = ("-name",)


@admin.register(models.Match)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "team_home", "team_away", "date", "is_finished", "total_score", "winner")
    ordering = ("is_finished", "date",)


@admin.register(models.MatchStatistics)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "match", "time_played_min", "goals_scored")

    @staticmethod
    def time_played_min(obj):
        return obj.time_played.strftime("%M:%S")
