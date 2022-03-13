from django.urls import path, include
from rest_framework import routers
from WebApp import views as WebAppViews
from WebApp.views import BuyPlayerView, GetFinalView, TransfersView, ChampzPlayersView, GetGroupStageView, EndChampzView, ParticipantsTeamsView, GetWildcardKnockoutRoundView, GetSemiFinalsRoundView, UpdatePlayerDatabaseView, UpdateTeamsLeaguesDatabaseView, GetGroupTableView

router = routers.DefaultRouter(trailing_slash=False)
router.register('nation', WebAppViews.NationViewSet)
router.register('league', WebAppViews.LeagueViewSet)
router.register('participant', WebAppViews.ParticipantViewSet)
router.register('team', WebAppViews.TeamViewSet)
router.register('position', WebAppViews.PositionViewSet)
router.register('player', WebAppViews.PlayerViewSet)
router.register('group', WebAppViews.GroupViewSet)
router.register('match', WebAppViews.MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('buy/<int:id>', BuyPlayerView.as_view(), name='post'),
    path('table/<int:id>', GetGroupTableView.as_view(), name='get'),
    path('group-stage', GetGroupStageView.as_view(), name='post'),
    path('wildcards', GetWildcardKnockoutRoundView.as_view(), name='post'),
    path('semis', GetSemiFinalsRoundView.as_view(), name='post'),
    path('final', GetFinalView.as_view(), name='post'),
    path('transfers', TransfersView.as_view(), name='get'),
    path('champz-players', ChampzPlayersView.as_view(), name='get'),
    path('participants-teams', ParticipantsTeamsView.as_view(), name='get'),
    path('end-champz', EndChampzView.as_view(), name='post'),
    path('update-players', UpdatePlayerDatabaseView.as_view(), name='post'),
    path('update-teams-leagues', UpdateTeamsLeaguesDatabaseView.as_view(), name='post'),
]