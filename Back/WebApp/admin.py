from django.contrib import admin

# Register your models here.
from WebApp.models import Nation, League, Team, Participant, Position, Player, Group, Match

admin.site.register(Nation)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Participant)
admin.site.register(Position)
admin.site.register(Player)
admin.site.register(Group)
admin.site.register(Match)

