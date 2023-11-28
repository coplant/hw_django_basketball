from datetime import timedelta

from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from .models import Team, Player, Match, MatchStatistics


def team_list(request):
    teams = Team.objects.all()
    return render(request, "players/team_list.html", {"teams": teams})


def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    players = Player.objects.filter(team=team)
    statistic = {}
    vb = {}
    for player in players:
        statistic[player.pk] = player_stat(request, player)
        if not vb:
            vb = statistic.get(player.pk).get("verbose_names")

    return render(request, "players/team_detail.html", {
        "team": team, "statistic": statistic, "vb": vb
    })


def match_list(request):
    matches = Match.objects.filter(is_finished=0)
    return render(request, "players/match_list.html", {"matches": matches})


def past_match_list(request):
    matches = Match.objects.filter(is_finished=1)
    return render(request, "players/match_list.html", {"matches": matches, "is_finished": True})


def player_stat(request, player=None):
    if not player:
        player = get_object_or_404(Player, pk=request.user.player.pk)
    match_statistics_fields = [(field.name, field.verbose_name) for field in MatchStatistics._meta.get_fields()]

    aggregation_dict = {}
    verbose_names = {}
    for field, verbose in match_statistics_fields[3:]:
        verbose_names[field] = verbose
        if field == "time_played":
            continue
        aggregation_dict[field] = Sum(field)

    current_player_statistics = MatchStatistics.objects.filter(player=player)

    times = MatchStatistics.objects.filter(player=player).values_list("time_played", flat=True)
    hours = map(lambda time: time.hour * 60 * 60 + time.minute * 60 + time.second, times)
    time_played = sum(hours)

    total_statistics = {"time_played": str(timedelta(seconds=time_played))}
    total_statistics.update(current_player_statistics.aggregate(**aggregation_dict))
    return {"player": player, "statistic": total_statistics, "verbose_names": verbose_names}


def home_view(request):
    matches = Match.objects.all()
    return render(request, "home.html", {"matches": matches})
