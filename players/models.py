from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime

User = get_user_model()


def validate_time_range(value):
    min_time = datetime.strptime("00:00:00", "%H:%M:%S").time()
    max_time = datetime.strptime("00:50:00", "%H:%M:%S").time()
    if not (min_time <= value <= max_time):
        raise ValidationError("Неверное время")


class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} {'(' + self.number + ')' if self.number else ''}"


class Match(models.Model):
    team_home = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    team_away = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(default="09:00:00")
    place = models.TextField(default="ул. Биатлонная, 25Б")
    is_finished = models.BooleanField("Игра состоялась", default=0)

    team_home_score = models.PositiveIntegerField(default=0)
    team_away_score = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("is_finished", "date",)

    def __str__(self):
        return f"{self.team_home} vs {self.team_away} ({self.date})"

    @property
    def winner(self):
        if self.team_home_score == self.team_away_score:
            return None
        return self.team_home if self.team_home_score > self.team_away_score else self.team_away

    @property
    def total_score(self):
        return f"{self.team_home_score} : {self.team_away_score}"


class MatchStatistics(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    time_played = models.TimeField(default="00:00:00", validators=[validate_time_range])
    throw_count = models.PositiveIntegerField(default=0)
    goal_three_count = models.PositiveIntegerField(default=0)
    goal_two_count = models.PositiveIntegerField(default=0)
    goal_penalty_count = models.PositiveIntegerField(default=0)
    rebound_home = models.PositiveIntegerField(default=0)
    rebound_away = models.PositiveIntegerField(default=0)
    assist = models.PositiveIntegerField(default=0)
    interception = models.PositiveIntegerField(default=0)
    loss = models.PositiveIntegerField(default=0)
    block_shot = models.PositiveIntegerField(default=0)
    fouls_player = models.PositiveIntegerField(default=0)
    fouls_opponent = models.PositiveIntegerField(default=0)

    @property
    def goals_scored(self):
        return self.goal_three_count * 3 + self.goal_two_count * 2 + self.goal_penalty_count

    @property
    def goals_total(self):
        return self.goal_three_count + self.goal_two_count + self.goal_penalty_count

    @property
    def rebounds_total(self):
        return self.rebound_home + self.rebound_away

    @property
    def kpi(self):
        return self.goals_scored + self.assist + self.interception + self.block_shot + self.fouls_opponent - self.throw_count - self.loss - self.fouls_player

    def __str__(self):
        return f"Статистика {self.player.user.get_full_name()}"
