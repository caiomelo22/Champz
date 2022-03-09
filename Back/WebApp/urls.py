from django.urls import path, include
from rest_framework import routers
from WebApp import views as WebAppViews
from WebApp.views import BuyPlayerView, AddParticipantGroupView, CreateMatchesView, GetGroupTableView, RegisterScoreView, \
    GenerateFirstKnockoutRoundView, GenerateFinalView, TransfersView, ChampzPlayersView, StartChampzView, EndChampzView, \
    ParticipantsTeamsView, GenerateWildcardKnockoutRoundView, GenerateSemiFinalsRoundView, UpdatePlayerDatabaseView, \
    UpdateTeamsLeaguesDatabaseView

router = routers.DefaultRouter()
router.register(r'nation', WebAppViews.NationViewSet)
router.register(r'league', WebAppViews.LeagueViewSet)
router.register(r'participant', WebAppViews.ParticipantViewSet)
router.register(r'team', WebAppViews.TeamViewSet)
router.register(r'position', WebAppViews.PositionViewSet)
router.register(r'player', WebAppViews.PlayerViewSet)
router.register(r'group', WebAppViews.GroupViewSet)
router.register(r'match', WebAppViews.MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('buy/<int:id>', BuyPlayerView.as_view(), name='post'),
    path('add-team-group/<int:id>', AddParticipantGroupView.as_view(), name='post'),
    path('create-matches/<int:id>', CreateMatchesView.as_view(), name='post'),
    path('table/<int:id>', GetGroupTableView.as_view(), name='get'),
    path('register-score/<int:id>', RegisterScoreView.as_view(), name='post'),
    path('generate-1st-knockout/', GenerateFirstKnockoutRoundView.as_view(), name='post'),
    path('generate-wildcards/', GenerateWildcardKnockoutRoundView.as_view(), name='post'),
    path('generate-semis/', GenerateSemiFinalsRoundView.as_view(), name='post'),
    path('generate-final', GenerateFinalView.as_view(), name='post'),
    path('transfers/', TransfersView.as_view(), name='get'),
    path('champz-players/', ChampzPlayersView.as_view(), name='get'),
    path('participants-teams/', ParticipantsTeamsView.as_view(), name='get'),
    path('start-champz/', StartChampzView.as_view(), name='post'),
    path('end-champz/', EndChampzView.as_view(), name='post'),
    path('update-players/', UpdatePlayerDatabaseView.as_view(), name='post'),
    path('update-teams-leagues/', UpdateTeamsLeaguesDatabaseView.as_view(), name='post'),
]