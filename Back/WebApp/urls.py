from django.urls import path, include
from rest_framework import routers
from WebApp import views as WebAppViews
from WebApp.views import BuyPlayerView, AddTeamGroupView, CreateMatchesView, GetGroupTableView, RegisterScoreView, \
    GenerateFirstKnockoutRoundView, GenerateFinalView, TransfersView, ChampzPlayersView, StartGroupView, EndChampzView, \
    ParticipantsTeamsView, GenerateWildcardKnockoutRoundView, GenerateSemiFinalsRoundView, UpdatePlayerDatabaseView, \
    StripPlayerPositionView

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
    path('add_team_group/<int:id>', AddTeamGroupView.as_view(), name='post'),
    path('create_matches/<int:id>', CreateMatchesView.as_view(), name='post'),
    path('table/<int:id>', GetGroupTableView.as_view(), name='get'),
    path('register_score/<int:id>', RegisterScoreView.as_view(), name='post'),
    path('generate_1st_knockout/', GenerateFirstKnockoutRoundView.as_view(), name='post'),
    path('generate_wildcards/', GenerateWildcardKnockoutRoundView.as_view(), name='post'),
    path('generate_semis/', GenerateSemiFinalsRoundView.as_view(), name='post'),
    path('generate_final', GenerateFinalView.as_view(), name='post'),
    path('transfers/', TransfersView.as_view(), name='get'),
    path('champz_players/', ChampzPlayersView.as_view(), name='get'),
    path('participants_teams/', ParticipantsTeamsView.as_view(), name='get'),
    path('start_group/', StartGroupView.as_view(), name='post'),
    path('end_champz/', EndChampzView.as_view(), name='post'),
    path('update-players/', UpdatePlayerDatabaseView.as_view(), name='get'),
    path('strip-players-position/', StripPlayerPositionView.as_view(), name='get'),
]