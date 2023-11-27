from django.shortcuts import render
from .models import Team, Player, Match
from .forms import PlayerStatForm


def team_list(request):
    teams = Team.objects.all()
    return render(request, "players/team_list.html", {"teams": teams})


def team_detail(request, team_id):
    team = Team.objects.get(pk=team_id)
    players = Player.objects.filter(team=team)
    return render(request, "players/team_detail.html", {"team": team, "players": players})


def match_list(request):
    matches = Match.objects.filter(is_finished=0)
    return render(request, "players/match_list.html", {"matches": matches})


def past_match_list(request):
    matches = Match.objects.filter(is_finished=1)
    return render(request, "players/match_list.html", {"matches": matches, "is_finished": True})


def player_stat(request, player_id):
    player = Player.objects.get(pk=player_id)

    if request.method == "POST":
        form = PlayerStatForm(request.POST)
        if form.is_valid():
            ...
    else:
        form = PlayerStatForm()

    return render(request, "players/player_stat.html", {"player": player, "form": form})


def home_view(request):
    return render(request, "home.html")
