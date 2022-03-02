from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from WebApp.models import Nation, League, Participant, Team, Position, Player, Group, Match
from WebApp.serializers import NationSerializer, LeagueSerializer, ParticipantSerializer, TeamSerializer, \
    PositionSerializer, PlayerSerializer, GroupSerializer, MatchSerializer
from WebApp.services import get_players_db, getPlayersByPositionString, writePlayersSheet, strip_player_positions_string, getPlayersByPositionAlgorythm, update_teams_leagues
from django_filters.rest_framework import DjangoFilterBackend

import openpyxl

import operator


class NationViewSet(viewsets.ModelViewSet):
    queryset = Nation.objects.all()
    serializer_class = NationSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        nation = Nation.create(data['name'], data['image_path'])
        nation = NationSerializer(nation, context={'request': request})
        return Response(nation.data)


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        league = League.create(data['name'])
        league = LeagueSerializer(league, context={'request': request})
        return Response(league.data)


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        team = Team.objects.get(id=int(data['team']))
        if team.participant != None:
            return HttpResponseBadRequest("The chosen team has already been assigned to another participant.")
        participant = Participant.create(
            data['name'], int(data['budget']), team)
        participant = ParticipantSerializer(
            participant, context={'request': request})
        return Response(participant.data)

    def partial_update(self, request, *args, **kwargs):
        instance = Participant.objects.get(id=kwargs.get('pk'))
        data = dict(request.data)
        team = data.get('team')
        if team != None:
            old_team = Team.objects.filter(participant=instance.id)
            new_team = Team.objects.filter(id=int(team))
            if len(new_team)>0 and (new_team[0].participant != None and new_team[0].participant.id != instance.id):
                    return HttpResponseBadRequest("The chosen team has already been assigned to another participant.")
            elif len(new_team) > 0:
                new_team = new_team[0]
            else:
                return HttpResponseBadRequest("The chosen team does not exist.")

            if len(old_team) > 0:
                old_team = old_team[0]

                players_old_team = Player.objects.filter(team_participant=old_team.id)
                for player in players_old_team:
                    player.team_participant = new_team
                    player.save()
                
                if team != old_team.id:
                    old_team.participant = None
       
            new_team.participant = instance
            if old_team:
                old_team.save()
            new_team.save()
            del data['team']

        serializer = self.serializer_class(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = Participant.objects.get(id=kwargs.get('pk'))
        team = Team.objects.get(participant=instance.id)
        players = Player.objects.filter(team_participant=team.id)
        for player in players:
            player.team_participant = None
            player.value = None
            player.save()
        instance.delete()
        return Response(ParticipantSerializer(instance).data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['league']

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        league = League.objects.get(id=int(data['league']))
        team = Team.create(data['name'], league, data['image_path'])
        team = TeamSerializer(team, context={'request': request})
        return Response(team.data)


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        position = Position.create(data['name'])
        position = PositionSerializer(position, context={'request': request})
        return Response(position.data)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('-overall', '-pace')
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['position', 'team_participant', 'team_origin']

    def cut_player_quantity(self, position):
        if position.name == 'Goalkeepers':
            return getPlayersByPositionAlgorythm(position.id, 1.5)
        elif position.name == 'Center Backs':
            return getPlayersByPositionAlgorythm(position.id, 3)
        elif position.name == 'Full Backs':
            return getPlayersByPositionAlgorythm(position.id, 3)
        elif position.name == 'Defensive Midfielders':
            return getPlayersByPositionAlgorythm(position.id, 3)
        elif position.name == 'Ofensive Midfielders':
            return getPlayersByPositionAlgorythm(position.id, 1.5)
        elif position.name == 'Wingers':
            return getPlayersByPositionAlgorythm(position.id, 2.5)
        elif position.name == 'Attackers':
            return getPlayersByPositionAlgorythm(position.id, 2)

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        position = Position.objects.get(id=int(data['position']))
        team_origin = Team.objects.get(id=int(data['team_origin']))
        nation = Nation.objects.get(id=int(data['nation']))
        player = Player.create(data['name'], int(
            data['overall']), position, team_origin, nation, data['image_path'], data['specific_position'])
        player = PlayerSerializer(player, context={'request': request})
        return Response(player.data)

    def list(self, request, *args, **kwargs):
        players = list(Player.objects.all().order_by('-overall'))
        if 'team_participant' in request._request.__dict__['environ']['QUERY_STRING']:
            team_participant = request._request.__dict__['environ']['QUERY_STRING'].split('=')[1]
            players = [player for player in players if str(player.team_participant_id)==team_participant]
            players.sort(key=lambda item: (item.overall, item.pace), reverse=True)
        if 'position' in request._request.__dict__['environ']['QUERY_STRING']:
            position = request._request.__dict__['environ']['QUERY_STRING'].split('=')[1]
            position_obj = Position.objects.get(id=position)
            players = self.cut_player_quantity(position_obj)
        
        return Response(PlayerSerializer(players, many=True).data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        group = Group.create(data['group'])
        group = GroupSerializer(group, context={'request': request})
        return Response(group.data)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        group = Group.objects.get(id=int(data['group']))
        team_1 = Team.objects.get(id=int(data['team_1']))
        team_2 = Team.objects.get(id=int(data['team_2']))
        match = Match.create(group, team_1, team_2)
        match = MatchSerializer(match, context={'request': request})
        return Response(match.data)


class BuyPlayerView(APIView):
    def post(self, request, id):
        player = Player.objects.filter(id=id)
        if len(player) == 0:
            return HttpResponseNotFound("There are no players with the given id.")
        else:
            player = player[0]

        data = dict(request.data)

        team = None
        price = None
        if data.get('team_participant') is not None:
            team = Team.objects.filter(id=int(data['team_participant']))
            if len(team) == 0:
                return HttpResponseNotFound("There are no teams with the given id.")
            else:
                team = team[0]
            price = int(data['value'])

        result = player.buyPlayer(team, price)

        if result:
            return Response(PlayerSerializer(player).data)
        else:
            return HttpResponseBadRequest("The budget of {} is not enough to buy {}".format(data['team_participant'], player))


class AddTeamGroupView(APIView):
    def post(self, request, id):
        group = Group.objects.filter(id=id)
        if len(group) == 0:
            return HttpResponseNotFound("There are no groups with the given id.")
        else:
            group = group[0]

        data = dict(request.data)
        team = Team.objects.get(id=int(data['id']))
        group.addTeam(team)

        return Response(TeamSerializer(group.teams, many=True).data)


class CreateMatchesView(APIView):
    def post(self, request, id):
        group = Group.objects.filter(id=id)
        if len(group) == 0:
            return HttpResponseNotFound("There are no groups with the given id.")
        else:
            group = group[0]

        matches = group.createMatches()

        group.export_matches()

        matches = MatchSerializer(matches, many=True).data

        return Response(matches)

class StartChampzView(APIView):
    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    def post(self, request, groupsQuantity):
        groups = Group.objects.all()
        for group in groups:
            group.delete()

        matches = []

        participants = list(Participant.objects.all())

        participant_groups = self.chunks(participants, int(len(participants)/groupsQuantity))

        for i, group_participants in enumerate(participant_groups):
            group = Group.create('Group {}'.format(i+1))
            for participant in group_participants:
                team = Team.objects.get(participant=participant)
                group.addTeam(team)
            
            matches.extend(group.createMatches())

        group.export_matches()

        matches = MatchSerializer(matches, many=True).data

        return Response(matches)

class RedoGroupsMatchesView(APIView):
    def post(self, request):
        groups = list(Group.objects.all())
        matches = Match.objects.all()
        for match in matches:
            match.delete()

        matches = []

        group1 = list(groups[0].teams.all())
        group2 = list(groups[1].teams.all())
        for i in range(len(group1)):
            for j in range(len(group2)):
                team_1 = Team.objects.filter(id=group1[i].id)[0]
                team_2 = Team.objects.filter(id=group2[j].id)[0]
                matches.append(Match.create(groups[0], team_1, team_2))

        file = open("matches.txt", "w")

        file.write('MATCHES: \n\n')

        strBuilder = ""
        # strBuilder += '{}\n'.format(group.group.upper())
        for match in matches:
            team_1 = match.team_1.participant.name
            team_2 = match.team_2.participant.name
            goals_1 = match.goals_team_1
            print(goals_1, type(goals_1))
            if goals_1 is None:
                goals_1 = ''
            goals_2 = match.goals_team_2
            if goals_2 is None:
                goals_2 = ''
            strBuilder += '\t{} {} x {} {}\n'.format(team_1, goals_1, goals_2, team_2)
        strBuilder += '\n'
        file.write(strBuilder)

        file.close()

        matches = MatchSerializer(matches, many=True).data

        return Response(matches)

class GetGroupTableView(APIView):
    def get(self, request, id):
        group = Group.objects.filter(id=id)
        if len(group) == 0:
            return HttpResponseNotFound("There are no groups with the given id.")
        else:
            group = group[0]

        table = group.getGroupTable()
        new_table = []

        dic = dict()

        for participant in table:
            dic[participant[0].id] = participant[1]
            new_table.append(
                (TeamSerializer(participant[0]).data, participant[1]))
        return JsonResponse(new_table, safe=False)

class GetGroupsTableView(APIView):
    def get(self, request):
        groups = list(Group.objects.all())
        groups = [g for g in groups if 'Group' in g.group]
        if len(groups) == 0:
            return HttpResponseNotFound("No groups found.")
        
        tables = []

        for group in groups:
            table = group.getGroupTable()
            tables.append([])

            dic = dict()

            for participant in table:
                dic[participant[0].id] = participant[1]
                tables[-1].append(
                    (TeamSerializer(participant[0]).data, participant[1]))
        return JsonResponse(tables, safe=False)


class RegisterScoreView(APIView):
    def post(self, request, id):
        data = dict(request.data)
        match = Match.objects.filter(id=id)
        if len(match) == 0:
            return HttpResponseNotFound("There are no matches with the given id.")
        else:
            match = match[0]

        goals_team_1 = data.get('goals_team_1')
        goals_team_2 = data.get('goals_team_2')

        if goals_team_1 == None or goals_team_2 == None:
            return HttpResponseBadRequest("Invalid value for goals scored.")

        data = dict(request.data)

        match.registerScore(int(goals_team_1),
                            int(goals_team_2))

        return Response(MatchSerializer(match).data)


class GenerateFirstKnockoutRoundView(APIView):
    def post(self, request):
        matches = []

        old_stage = Group.objects.filter(group='Knockout 1')
        if len(old_stage) > 0:
            old_stage = old_stage[0]
            old_stage.delete()

        groups = list(Group.objects.filter(group='Group 1'))

        if len(groups) == 1:
            table = groups[0].getGroupTable()[:4]
            knockout_1 = Group.create('Knockout 1')

            for team in table:
                knockout_1.addTeam(team[0])

            matches.append(Match.create(knockout_1, table[0][0], table[3][0]))
            matches.append(Match.create(knockout_1, table[1][0], table[2][0]))
        else:
            return HttpResponseBadRequest("Number of groups does not allow the generation of a knockout round.")

        knockout_1.save()

        matches = MatchSerializer(matches, many=True)

        return Response(matches.data)

class GenerateWildcardKnockoutRoundView(APIView):
    def post(self, request):
        matchesWildcard = []

        old_stage = Group.objects.filter(group='Wildcard')
        if len(old_stage) > 0:
            old_stage = old_stage[0]
            old_stage.delete()

        groups = list(Group.objects.filter(group='Group 1'))

        if len(groups) == 1:
            tableWildcard = groups[0].getGroupTable()[2:6]
            wildcard = Group.create('Wildcard')

            for team in tableWildcard:
                wildcard.addTeam(team[0])

            matchesWildcard.append(Match.create(wildcard, tableWildcard[0][0], tableWildcard[3][0]))
            matchesWildcard.append(Match.create(wildcard, tableWildcard[1][0], tableWildcard[2][0]))
            
            wildcard.save()

        elif len(groups) == 2:
            print(groups)
            for i in range(2):
                tableWildcard = groups[i].getGroupTable()[1:3]
                wildcard = Group.create('Wildcard {}'.format(i+1))

                for team in tableWildcard:
                    wildcard.addTeam(team[0])

                matchesWildcard.append(Match.create(wildcard, tableWildcard[0][0], tableWildcard[1][0]))
                
                wildcard.save()

        else:
            return HttpResponseBadRequest("Number of groups does not allow the generation of a knockout round.")


        matchesWildcard = MatchSerializer(matchesWildcard, many=True)

        return Response(matchesWildcard.data)


class GenerateSemiFinalsRoundView(APIView):
    def checkPositionGroupStage(self, team, group_stage):
        for i, position in enumerate(group_stage):
            if position[0] == team:
                return i
        return -1

    def get_group_winners(self, group, teams, group_stage):
        qualified = []
        group = Group.objects.get(group=group)
        for team in teams:
            if team[1]['P'] == 3:
                qualified.append(team[0])
            elif team[1]['P'] == 1:
                opponent = group.findMatchGroupParticipantOpponent(team[0])
                position_team = self.checkPositionGroupStage(team[0], group_stage)
                position_opponent = self.checkPositionGroupStage(opponent, group_stage)
                if position_team < position_opponent:
                    qualified.append(team[0])

            if len(qualified) == 2:
                break

        return qualified

    def post(self, request):
        wildcard_stage = [g for g in groups if 'Wildcard' in g.group]
        matchesSemi = []

        old_stage = Group.objects.filter(group='Semis')
        if len(old_stage) > 0:
            old_stage = old_stage[0]
            old_stage.delete()

        group_stage = Group.objects.get(group='Group 1')
        table_group_stage = group_stage.getGroupTable()
 
        wildcard_stage = Group.objects.get(group='Wildcard')
        table_wildcard = wildcard_stage.getGroupTable()
        semis = Group.create('Semis')
        
        if len(group_stage) == 1:
            table_group_stage = group_stage[0].getGroupTable()
            table_wildcard = wildcard_stage[0].getGroupTable()

            wildcard_winners = self.get_group_winners('Wildcard', table_wildcard, table_group_stage)

            semis.addTeam(table_group_stage[0][0])
            semis.addTeam(table_group_stage[1][0])
            semis.addTeam(wildcard_winners[0])
            semis.addTeam(wildcard_winners[1])

            wc1_position = self.checkPositionGroupStage(wildcard_winners[0], table_group_stage)
            wc2_position = self.checkPositionGroupStage(wildcard_winners[1], table_group_stage)

            if wc1_position < wc2_position:
                matchesSemi.append(Match.create(semis, table_group_stage[0][0], wildcard_winners[1]))
                matchesSemi.append(Match.create(semis,  wildcard_winners[1], table_group_stage[0][0]))
                matchesSemi.append(Match.create(semis, table_group_stage[1][0], wildcard_winners[0]))
                matchesSemi.append(Match.create(semis, wildcard_winners[0], table_group_stage[1][0]))
            else:
                matchesSemi.append(Match.create(semis, table_group_stage[0][0], wildcard_winners[0]))
                matchesSemi.append(Match.create(semis, wildcard_winners[0], table_group_stage[0][0]))
                matchesSemi.append(Match.create(semis, table_group_stage[1][0], wildcard_winners[1]))
                matchesSemi.append(Match.create(semis, wildcard_winners[1], table_group_stage[1][0]))

        if len(group_stage) == 2:
            qualified = []
            for i in range(2):
                table_group_stage = group_stage[i].getGroupTable()
                table_wildcard = wildcard_stage[i].getGroupTable()

                wildcard_winners = self.get_group_winners('Wildcard {}'.format(i+1), table_wildcard, table_group_stage)
                qualified.append(table_group_stage[0][0])
                qualified.append(wildcard_winners[0])
                semis.addTeam(table_group_stage[0][0])
                semis.addTeam(wildcard_winners[0])
                
            matchesSemi.append(Match.create(semis, qualified[0], qualified[1]))
            matchesSemi.append(Match.create(semis, qualified[1], qualified[0]))
            matchesSemi.append(Match.create(semis, qualified[2], qualified[3]))
            matchesSemi.append(Match.create(semis, qualified[3], qualified[2]))

        semis.save()

        matchesSemi = MatchSerializer(matchesSemi, many=True)

        return Response(matchesSemi.data)


class GenerateFinalView(APIView):
    def checkPositionGroupStage(self, team, group_stage):
        for i, position in enumerate(group_stage):
            print(position, i)
            if position[0] == team:
                return i
        return -1
        
    def post(self, request):
        old_stage = Group.objects.filter(group='Final')
        if len(old_stage) > 0:
            old_stage = old_stage[0]
            old_stage.delete()

        semis = Group.objects.get(group='Semis')

        finalMatch = semis.generateFinalRound()

        finalMatch = MatchSerializer(finalMatch, many=True)

        return Response(finalMatch.data)


class TransfersView(APIView):
    def get(self, request):
        file = open("transfers.txt", "w", encoding="utf-8")
        leagues = League.objects.all().order_by('name')
        team_participant = None
        for league in leagues:
            team_participant = None
            strBuilder = ""
            strBuilder += ("LEAGUE: {}\n".format(league.name.upper()))
            teams = Team.objects.filter(league=league.id).order_by('name')
            for team in teams:
                strBuilder += ("\tTEAM: {}\n".format(team.name.replace('ş', 's').upper()))
                players = Player.objects.filter(team_origin=team.id).order_by(
                    '-team_participant', '-overall')
                for player in players:
                    if player.team_participant != None and player.team_participant != team:
                        team_participant = player.team_participant
                        strBuilder += ("\t\tTO {}: {} - {}\n".format(
                            team_participant.name.upper(), player.overall, player.name.upper()))
            strBuilder += ('--------------------------------------------------------------------------\n')
            if team_participant is not None:
                file.write(strBuilder)

        file.close()

        return Response()

class ChampzPlayersView(APIView):
    def get(self, request):
        positions = list(Position.objects.all())
        wb = openpyxl.Workbook()
        for i,position in enumerate(positions):
            wb.create_sheet(index = i , title = position.name)
        n_participants = len(list(Participant.objects.all()))
        wb.active = 0
        getPlayersByPositionString(wb.active, positions[0], 1.5*n_participants)
        wb.active = 1
        getPlayersByPositionString(wb.active, positions[1], 3*n_participants)
        wb.active = 2
        getPlayersByPositionString(wb.active, positions[2], 3*n_participants)
        wb.active = 3
        getPlayersByPositionString(wb.active, positions[3], 3*n_participants)
        wb.active = 4
        getPlayersByPositionString(wb.active, positions[4], 1.5*n_participants)
        wb.active = 5
        getPlayersByPositionString(wb.active, positions[5], 2.5*n_participants)
        wb.active = 6
        getPlayersByPositionString(wb.active, positions[6], 2*n_participants)

        wb.save("players.xlsx") 

        return Response()

class ParticipantsTeamsView(APIView):
    def get(self, request):
        participants = Participant.objects.all()
        wb = openpyxl.Workbook()
        for i,participant in enumerate(participants):
            participant_team = Team.objects.get(participant=participant)
            participant_players = Player.objects.filter(team_participant=participant_team).order_by('position', 'specific_position', '-overall')
            wb.create_sheet(index = i , title = "{}({})".format(participant.name, participant_team.name))
            wb.active = i
            writePlayersSheet(wb.active, participant_players)

        wb.save("teams.xlsx") 

        return Response()

class EndChampzView(APIView):
    def post(self, request):
        file = open("champz.txt", "w", encoding="utf-8")
        participants = Participant.objects.all()
        file.write("TEAMS: \n\n")
        for participant in participants:
            strBuilder = ""
            strBuilder += 'TEAM {}'.format(participant.name.upper())
            team_participant = Team.objects.get(participant=participant)
            strBuilder += '({})\n'.format(team_participant.name.upper())
            players_participant = Player.objects.filter(team_participant=team_participant).order_by('-overall')
            for player in players_participant:
                strBuilder += '\t{} - {} - ${}\n'.format(player.name, player.overall, player.value)
            strBuilder += '\n'
            print(strBuilder)
            file.write(strBuilder)

        groups = list(Group.objects.all())
        group_stage = [g for g in groups if 'Group' in g.group]

        for index, group in enumerate(group_stage):
            table = group.getGroupTable()

            file.write('GROUP {} TABLE\n\n'.format(index+1))
            file.write('TEAM\t\tP\tW\tD\tL\tGF\tGA\tGD\n')
            for el in table:
                team = Team.objects.get(name=el[0])
                if len(team.participant.name) > 8:
                    file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(team.participant.name, el[1]['P'], el[1]['W'], el[1]['D'], el[1]['L'], el[1]['GF'], el[1]['GA'], el[1]['GD']))
                else:
                    file.write('{}\t\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(team.participant.name, el[1]['P'], el[1]['W'], el[1]['D'], el[1]['L'], el[1]['GF'], el[1]['GA'], el[1]['GD']))
            file.write('\n')


        file.write('MATCHES: \n\n')

        for group in groups:
            strBuilder = ""
            strBuilder += '{}\n'.format(group.group.upper())
            matches = Match.objects.filter(group=group)
            for match in matches:
                team_1 = match.team_1.participant.name
                team_2 = match.team_2.participant.name
                goals_1 = match.goals_team_1
                print(goals_1, type(goals_1))
                if goals_1 is None:
                    goals_1 = ''
                goals_2 = match.goals_team_2
                if goals_2 is None:
                    goals_2 = ''
                strBuilder += '\t{} {} x {} {}\n'.format(team_1, goals_1, goals_2, team_2)
            strBuilder += '\n'
            file.write(strBuilder)

        file.close()

        return Response()

class UpdatePlayerDatabaseView(APIView):
    def post(self, request):
        get_players_db()
        return Response()

class UpdateTeamsLeaguesDatabaseView(APIView):
    def post(self, request):
        update_teams_leagues()
        return Response()
