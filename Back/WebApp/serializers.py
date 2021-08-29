from rest_framework import serializers

from WebApp import models


class NationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Nation
        fields = ['id', 'name', 'image_link']


class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.League
        fields = ['id', 'name']


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=models.Team.objects.all())
    class Meta:
        model = models.Participant
        fields = ['id', 'name', 'budget', 'team']


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    league = serializers.PrimaryKeyRelatedField(queryset=models.League.objects.all())
    participant = serializers.PrimaryKeyRelatedField(queryset=models.Participant.objects.all(), required=False)
    class Meta:
        model = models.Team
        fields = ['id', 'name', 'league', 'participant', 'image_link']


class PositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Position
        fields = ['id', 'name']


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    team_participant = serializers.PrimaryKeyRelatedField(queryset=models.Team.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=models.Position.objects.all())
    nation = serializers.PrimaryKeyRelatedField(queryset=models.Nation.objects.all())
    team_origin = serializers.PrimaryKeyRelatedField(queryset=models.Team.objects.all())
    class Meta:
        model = models.Player
        fields = ['id', 'name', 'overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical', 'likes',
                  'value', 'position', 'team_origin', 'team_participant', 'nation', 'image_link', 'specific_position']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    teams = TeamSerializer(read_only=True, many=True)
    class Meta:
        model = models.Group
        fields = ['id', 'group', 'teams']


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all())
    team_1 = serializers.PrimaryKeyRelatedField(queryset=models.Team.objects.all())
    team_2 = serializers.PrimaryKeyRelatedField(queryset=models.Team.objects.all())
    class Meta:
        model = models.Match
        fields = ['id', 'group', 'goals_team_1', 'goals_team_2', 'team_1', 'team_2']
