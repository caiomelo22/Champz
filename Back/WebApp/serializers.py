from rest_framework import serializers

from WebApp import models


class NationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Nation
        fields = ['id', 'name', 'image_path']


class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.League
        fields = ['id', 'name']

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    league = LeagueSerializer()
    participant = serializers.PrimaryKeyRelatedField(queryset=models.Participant.objects.all())
    class Meta:
        model = models.Team
        fields = ['id', 'name', 'league', 'image_path', 'participant']


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    team = TeamSerializer(read_only = True)
    team_loading_att = serializers.SerializerMethodField('is_team_loading')

    def is_team_loading(self, obj):
        return False
        
    class Meta:
        model = models.Participant
        fields = ['id', 'name', 'budget', 'team', 'team_loading_att']


class PositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Position
        fields = ['id', 'name']


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    team_participant = TeamSerializer()
    position = PositionSerializer()
    nation = NationSerializer()
    team_origin = TeamSerializer()
    class Meta:
        model = models.Player
        fields = ['id', 'name', 'overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical', 'likes',
                  'value', 'position', 'team_origin', 'team_participant', 'nation', 'image_path', 'specific_position']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    participants = ParticipantSerializer(read_only=True, many=True)
    class Meta:
        model = models.Group
        fields = ['id', 'group', 'participants']


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    group = GroupSerializer()
    participant_1 = ParticipantSerializer()
    participant_2 = ParticipantSerializer()
    class Meta:
        model = models.Match
        fields = ['id', 'group', 'goals_participant_1', 'goals_participant_2', 'participant_1', 'participant_2']
