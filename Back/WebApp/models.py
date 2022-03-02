import math
from random import shuffle

from django.db import models


class Nation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image_path = models.CharField(max_length=250, null=True)

    @classmethod
    def create(cls, name, image):
        nation = Nation.objects.create(name=name, image_path=image)
        return nation

    def __str__(self):
        return self.name


class League(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    @classmethod
    def create(cls, name):
        league = League.objects.create(name=name)
        return league

    def __str__(self):
        return self.name


class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    budget = models.IntegerField()

    @classmethod
    def create(cls, name, budget, team):
        participant = Participant.objects.create(name=name, budget=budget)
        team.participant = participant
        team.save()
        return participant

    def __str__(self):
        return self.name


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, null=True, blank=True, on_delete=models.CASCADE)
    participant = models.OneToOneField(Participant, null=True, blank=True, on_delete=models.SET_NULL)
    image_path = models.CharField(max_length=250, null=True)

    @classmethod
    def create(cls, name, league, image):
        team = Team.objects.create(name=name, league=league, image_path=image)
        return team

    def __str__(self):
        return self.name


class Position(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    specific_positions = models.CharField(max_length=100, null=True)

    @classmethod
    def create(cls, name, specific_positions):
        position = Position.objects.create(name=name, specific_positions=specific_positions)
        return position

    def __str__(self):
        return self.name


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    overall = models.IntegerField()
    pace = models.IntegerField(null=True)
    shooting = models.IntegerField(null=True)
    passing = models.IntegerField(null=True)
    dribbling = models.IntegerField(null=True)
    defending = models.IntegerField(null=True)
    physical = models.IntegerField(null=True)
    likes = models.IntegerField(null=True)
    value = models.IntegerField(null=True, blank=True)
    image_path = models.CharField(max_length=250, null=True)
    position = models.ForeignKey(Position, null=True, blank=True, on_delete=models.SET_NULL)
    specific_position = models.CharField(max_length=5, null=True)
    team_origin = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name="team_origin")
    team_participant = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL,
                                            related_name="team_participant")
    nation = models.ForeignKey(Nation, null=True, blank=True, on_delete=models.SET_NULL)

    @classmethod
    def create(cls, name, overall, position, team_origin, nation, image, spec_pos, likes):
        player = Player.objects.create(name=name, overall=overall, position=position, team_origin=team_origin, 
        nation=nation, image_path=image, specific_position=spec_pos, likes=likes)
        return player

    def buyPlayer(self, team, price):
        if self.team_participant:
            self.team_participant.participant.budget += self.value
            self.team_participant.participant.save()
            self.team_participant = None
            self.value = None
            self.save()

        if not team:
            return True

        participant = Participant.objects.get(id=team.participant.id)

        if participant.budget - price < 0:
            return False

        participant.budget -= price
        participant.save()

        self.value = price
        self.team_participant = team
        self.save()

        return True

    def __str__(self):
        return self.name


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.CharField(max_length=100)
    teams = models.ManyToManyField(Team)

    @classmethod
    def create(cls, group):
        group = Group.objects.create(group=group)
        return group

    def addTeam(self, team):
        self.teams.add(team)
        self.save()

    def match_exists(self, team_1, team_2):
        if len(Match.objects.filter(group=self, team_1=team_1, team_2=team_2)) == 1 or \
                len(Match.objects.filter(group=self, team_1=team_2, team_2=team_1)) == 1:
            return True
        return False

    def findMatchGroupParticipantOpponent(self, team):
        match_1 = Match.objects.filter(group=self, team_1=team)
        match_2 = Match.objects.filter(group=self, team_2=team)

        if len(match_1) > 0:
            return match_1[0].team_2
        if len(match_2) > 0:
            return match_2[0].team_1

    def createMatches(self):
        teams_list = list(self.teams.all())
        shuffle(teams_list)

        matches = []

        half = math.floor(len(teams_list)/2)
        first_half = teams_list[:half]
        second_half = teams_list[half:]

        for i in range(len(teams_list)):
            for j in range(len(first_half)):
                matches.append(Match.create(self, first_half[j], list(reversed(second_half))[j]))
            first_half.append(second_half.pop(0))
            second_half.append(first_half.pop(0))

        return matches

    def getStats(self, stats, matches, team):
        for match in matches:
            if match.goals_team_1 is not None:
                if team == match.team_1:
                    stats['GF'] += match.goals_team_1
                    stats['GA'] += match.goals_team_2
                else:
                    stats['GF'] += match.goals_team_2
                    stats['GA'] += match.goals_team_1
                stats['GD'] = stats['GF'] - stats['GA']

                if (team == match.team_1 and match.goals_team_1 > match.goals_team_2) or \
                        (team == match.team_2 and match.goals_team_2 > match.goals_team_1):
                    stats['P'] += 3
                    stats['W'] += 1
                elif (team == match.team_1 and match.goals_team_2 > match.goals_team_1) or \
                        (team == match.team_2 and match.goals_team_1 > match.goals_team_2):
                    stats['L'] += 1
                else:
                    stats['P'] += 1
                    stats['D'] += 1

        return stats

    def getStatsTeam(self, team):
        stats = {'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0}
        group = self
        if 'Group' in self.group:
            groups = list(Group.objects.all())
            group = ([g for g in groups if ('Group' in g.group and len(list(g.teams.all())) > 0)])[0]
        matches = list(Match.objects.filter(team_1=team, group=group))
        stats = self.getStats(stats, matches, team)

        matches = list(Match.objects.filter(team_2=team, group=group))
        stats = self.getStats(stats, matches, team)

        return stats

    def getGroupTable(self):
        teams_list = list(self.teams.all())
        stats = dict()
        for team in teams_list:
            stats[team] = self.getStatsTeam(team)
        stats_list = list(stats.items())
        stats_list = sorted(stats_list, key=lambda x: (x[1]['P'], x[1]['W'], x[1]['GD'], x[1]['GF']), reverse=True)
        return stats_list

    def generateFinalRound(self):
        teams = self.getGroupTable()
        qualified = list()

        qualified.append(teams[0][0])
        qualified.append(teams[1][0])

        matches = []

        old_stage = Group.objects.filter(group='Final')
        if len(old_stage) > 0:
            old_stage = old_stage[0]
            old_stage.delete()
            
        final = Group.create('Final')

        for team in qualified:
            final.addTeam(team)

        matches.append(Match.create(final, qualified[0], qualified[1]))

        final.save()

        return matches

    def export_matches(self):
        file = open("matches.txt", "w")

        file.write('MATCHES: \n\n')

        strBuilder = ""
        strBuilder += '{}\n'.format(self.group.upper())
        for match in self.matches:
            team_1 = match.team_1.participant.name
            team_2 = match.team_2.participant.name
            goals_1 = match.goals_team_1
            if goals_1 is None:
                goals_1 = ''
            goals_2 = match.goals_team_2
            if goals_2 is None:
                goals_2 = ''
            strBuilder += '\t{} {} x {} {}\n'.format(team_1, goals_1, goals_2, team_2)
        strBuilder += '\n'
        file.write(strBuilder)

        file.close()

    def __str__(self):
        return self.group


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    goals_team_1 = models.IntegerField(null=True)
    goals_team_2 = models.IntegerField(null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_1")
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_2")

    @classmethod
    def create(cls, group, team_1, team_2):
        match = Match.objects.create(group=group, team_1=team_1, team_2=team_2)
        return match

    def registerScore(self, goals_team_1, goals_team_2):
        self.goals_team_1 = goals_team_1
        self.goals_team_2 = goals_team_2
        self.save()

    def __str__(self):
        return "{} {} x {} {}".format(self.team_1, self.goals_team_1, self.goals_team_2, self.team_2)
