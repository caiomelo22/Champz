<template>
  <v-container v-if="!loading">
    <!-- <v-btn
      v-show="choice==false"
      style="text-align: center;"
      class="btn btn-success"
      @click="choice=true; loading=true; initializeGroup()"
    >Generate Group Matches</v-btn>
    <v-btn
      v-show="choice==false"
      style="text-align: center;"
      class="btn btn-success"
      @click="choice=true; getGroups();"
    >Continue With Latest Matchups</v-btn>-->
    <div>
      <v-card style="height: 100%">
        <v-toolbar color="primary" dark>
          <v-btn
            v-if="currentGroupIndex"
            fab
            text
            large
            @click="
              currentGroupIndex--;
              final = false;
            "
          >
            <v-icon dark large>mdi-chevron-left</v-icon>
          </v-btn>
          <v-toolbar-title class="mx-auto">{{
            get_group_title()
          }}</v-toolbar-title>
          <v-btn fab text large @click="next_stage_click()">
            <v-icon dark large>mdi-chevron-right</v-icon>
          </v-btn>
        </v-toolbar>
        <v-row>
          <v-col v-if="currentGroupIndex == 0" cols="12" md="8">
            <v-row>
              <v-col cols="12" md="11">
                <table
                  v-if="currentGroupIndex == 0"
                  class="table table-striped ml-7"
                >
                  <!-- <template v-slot:default> -->
                  <thead>
                    <tr>
                      <th class="champzFont" scope="col">Team</th>
                      <th class="champzFont" scope="col">P</th>
                      <th class="champzFont" scope="col">W</th>
                      <th class="champzFont" scope="col">D</th>
                      <th class="champzFont" scope="col">L</th>
                      <th class="champzFont" scope="col">GF</th>
                      <th class="champzFont" scope="col">GA</th>
                      <th class="champzFont" scope="col">GD</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(team, i) in table" :key="i">
                      <td class="champzFont">
                        <!-- <img style="width:30px;" :src="team[0].image_link" /> -->
                        {{
                          getTeamParticipant(
                            team[0].participant
                          ).name.toUpperCase()
                        }}
                      </td>
                      <td class="champzFont">{{ team[1].P }}</td>
                      <td class="champzFont">{{ team[1].W }}</td>
                      <td class="champzFont">{{ team[1].D }}</td>
                      <td class="champzFont">{{ team[1].L }}</td>
                      <td class="champzFont">{{ team[1].GF }}</td>
                      <td class="champzFont">{{ team[1].GA }}</td>
                      <td class="champzFont">{{ team[1].GD }}</td>
                    </tr>
                  </tbody>
                  <!-- </template> -->
                </table>
              </v-col>
              <v-col cols="12" md="1" class="champzDivider">
                <v-divider class="ml-8" vertical></v-divider>
              </v-col>
            </v-row>
          </v-col>
          <v-col
            cols="12"
            :md="currentGroupIndex ? 12 : 4"
            :class="currentGroupIndex ? 'champzKnockout' : 'champzMatches'"
          >
            <div v-for="group in get_dashboard_matches()" :key="group.id">
              <v-row class="mx-6">
                <h3>{{ group.group }}</h3>
              </v-row>
              <v-simple-table :class="currentGroupIndex ? 'mx-8' : 'mr-12'">
                <template v-slot:default>
                  <thead class="thead-dark">
                    <tr>
                      <th class="champzFont" scope="col">Match</th>
                      <th class="champzFont" scope="col">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(match, i) in group.matches" :key="i">
                      <td
                        class="champzFont text-center"
                        v-if="
                          match.goals_team_1 == null &&
                          match.goals_team_2 == null
                        "
                      >
                        {{
                          getTeamParticipant(
                            getTeamById(match.team_1).participant
                          ).name.toUpperCase()
                        }}
                        <!-- <img
                style="width:30px;"
                :src="getTeamById(match.team_1).image_link"
                      />-->
                        X
                        <!-- <img style="width:30px;" :src="getTeamById(match.team_2).image_link" /> -->
                        {{
                          getTeamParticipant(
                            getTeamById(match.team_2).participant
                          ).name.toUpperCase()
                        }}
                      </td>
                      <td class="champzFont text-center" v-else>
                        {{
                          getTeamParticipant(
                            getTeamById(match.team_1).participant
                          ).name.toUpperCase()
                        }}
                        <!-- <img
                style="width:30px;"
                :src="getTeamById(match.team_1).image_link"
                      />-->
                        {{ match.goals_team_1 }} X
                        {{ match.goals_team_2 }}
                        <!-- <img
                style="width:30px;"
                :src="getTeamById(match.team_2).image_link"
                      />-->
                        {{
                          getTeamParticipant(
                            getTeamById(match.team_2).participant
                          ).name.toUpperCase()
                        }}
                      </td>
                      <td>
                        <v-btn
                          small
                          fab
                          color="primary"
                          @click="getMatch(match)"
                        >
                          <v-icon small>mdi-pencil</v-icon>
                        </v-btn>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </div>
          </v-col>
        </v-row>
        <div class="text-center">
          <v-btn
            large
            class="mx-auto mb-12"
            light
            color="primary"
            v-if="final"
            v-on:click="generateChampzFile()"
            >Generate Champz File</v-btn
          >
        </div>
      </v-card>
      <v-spacer></v-spacer>
      <a @click="resetConfirmationModal = true">Reset matches</a>
      <v-dialog v-model="resetConfirmationModal" width="40%">
        <v-card>
          <v-card-title>
            <h3>
              Are you sure that you want to reset the matches? All of the
              current groups are going to be erased.
            </h3>
          </v-card-title>
          <v-card-text>
            <v-card-actions class="text-center">
              <v-btn class="mx-auto" color="red" @click="initializeGroup()"
                >Reset</v-btn
              >
            </v-card-actions>
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
    <!-- Register Score Modal -->
    <v-dialog v-model="registerScoreModal" width="40%">
      <v-card>
        <v-card-title>
          <h5>REGISTER SCORE</h5>
        </v-card-title>
        <v-card-text>
          <form v-on:submit.prevent="registerScore()">
            <v-row>
              <v-col cols="12" md="3">
                <span class="champzFont mr-2 mt-1" style="float: right">{{
                  getTeamParticipant(
                    getTeamById(currentMatch.team_1).participant
                  ).name
                }}</span>
              </v-col>
              <v-col cols="12" md="2">
                <v-text-field
                  outlined
                  dense
                  type="number"
                  v-model="currentMatch.goals_team_1"
                  min="0"
                  required="required"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="2">
                <span class="champzFont ml-7 mt-1">X</span>
              </v-col>
              <v-col cols="12" md="2">
                <v-text-field
                  outlined
                  dense
                  type="number"
                  v-model="currentMatch.goals_team_2"
                  min="0"
                  required="required"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <span class="champzFont ml-3 mt-1" style="float: left">{{
                  getTeamParticipant(
                    getTeamById(currentMatch.team_2).participant
                  ).name
                }}</span>
              </v-col>
            </v-row>
            <!-- <span>{{getTeamParticipant(getTeamById(currentMatch.team_1).participant).name}}</span>
                <v-text-field
                  style="float: right"
                  type="number"
                  v-model="currentMatch.goals_team_1"
                  min="0"
                  required="required"
                ></v-text-field>
                <span>X</span>
                <v-text-field
                  style="float: left"
                  type="number"
                  v-model="currentMatch.goals_team_2"
                  min="0"
                  required="required"
                ></v-text-field>
                <span>{{getTeamParticipant(getTeamById(currentMatch.team_2).participant).name}}</span> -->
            <v-card-actions>
              <v-btn
                type="button"
                color="red"
                @click="registerScoreModal = false"
                >Close</v-btn
              >
              <v-btn type="submit" color="green">Save changes</v-btn>
            </v-card-actions>
          </form>
        </v-card-text>
      </v-card>
    </v-dialog>
    <!-- End Register Score modal -->
  </v-container>

  <v-container v-else>
    <v-progress-circular
      style="margin-left: 50%"
      indeterminate
      size="70"
      color="primary"
    ></v-progress-circular>
  </v-container>
</template>

<style lang="scss" scoped>
.champzFont {
  font-size: 15px;
  font-weight: 500;
  font-family: system-ui;
}

.table {
  height: 61vh;
}

.champzDivider {
  height: 64vh;
}
.champzKnockout {
  height: 100%;
}
.champzMatches {
  height: 67vh;
  overflow-y: auto;
}
</style>

<script>
import Service from "@/services/Service";
export default {
  name: "Matches",

  data: () => ({
    service: new Service(),
    loading: true,
    choice: false,
    final: false,
    registerScoreModal: false,
    resetConfirmationModal: false,
    participants: [],
    groupMatches: [],
    plTeams: [],
    groups: [],
    matches: [],
    table: [],
    currentMatch: {},
    currentGroupIndex: 0,
    currentGroup: {},
  }),
  mounted: function () {
    this.getGroups();
    this.getParticipants();
    this.getPLTeams();
    // this.initializeGroup();
  },
  methods: {
    get_dashboard_matches() {
      if (this.currentGroupIndex == 0) {
        return [this.groups[0]];
      } else if (this.currentGroupIndex == 1) {
        return [this.groups[1]];
      } else if (this.currentGroupIndex == 2) {
        return this.groups.slice(2, 4);
      } else if (this.currentGroupIndex == 3) {
        return this.groups.slice(4, 6);
      }
    },
    next_stage_click() {
      if (this.currentGroupIndex == 0) {
        this.knockoutStageButtonClick();
      } else if (!this.currentGroupIndex == 0 && !this.final) {
        this.nextKnockoutStageButtonClick();
      }
    },
    getPLTeams: function () {
      this.service
        .getRequest("/api/team?league=98")
        .then((response) => {
          this.plTeams = response;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    getParticipants: function () {
      this.service
        .getRequest("/api/participant/")
        .then((response) => {
          console.log(response);
          this.participants = response;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    getTeamParticipant: function (id) {
      var participant = null;
      this.participants.forEach((element) => {
        if (element.id === id) {
          participant = element;
          return participant;
        }
      });
      if (participant == null) {
        participant = {
          name: "",
        };
      }
      return participant;
    },
    getTeamById: function (id) {
      var team = {};
      this.plTeams.forEach((element) => {
        if (element.id === id) {
          team = element;
          return team;
        }
      });
      return team;
    },
    getMatch: function (match) {
      this.currentMatch = Object.assign({}, match);
      this.registerScoreModal = true;

      // this.loading = true;
      // url = "/api/match/" + id + "/";
      // this.service
      //   .get(url)
      //   .then((response) => {
      //     this.currentMatch = response.data;
      //     $("#registerScoreModal").modal("show");
      //     this.loading = false;
      //   })
      //   .catch((err) => {
      //     this.loading = false;
      //     console.log(err);
      //   });
    },
    deleteGroups: function () {
      var i;
      var groupsToDelete = this.groups.slice(this.currentGroupIndex + 1);
      for (i = 0; i < groupsToDelete.length; i++) {
        this.deleteGroup(groupsToDelete[i].id);
      }
    },
    deleteGroup: function (id) {
      this.loading = true;
      var url = "/api/group/" + id + "/";
      this.service
        .deleteRequest(url)
        .then((response) => {
          this.loading = false;
          this.getGroups();
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    registerScore: function () {
      var groupIndex = this.groups
        .map((x) => x.id)
        .indexOf(this.currentMatch.group);
      var matchIndex = this.groups[groupIndex].matches
        .map((x) => x.id)
        .indexOf(this.currentMatch.id);
      this.groups[groupIndex].matches[matchIndex] = this.currentMatch;
      var url = "/api/match/" + this.currentMatch.id + "/";
          this.registerScoreModal = false;
      this.service
        .patchRequest(url, this.currentMatch)
        .then((response) => {
          if (this.currentGroupIndex == 0) {
            this.getGroupTable();
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getGroups: function () {
      this.loading = true;
      this.service
        .getRequest("/api/group/")
        .then((response) => {
          this.groups = response;
          if (this.groups.length == 0) {
            this.initializeGroup();
          } else {
            this.groups.forEach((element) => {
              element.matches = [];
            });
            this.getMatches();
            this.getGroupTable();
          }
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    getGroupTable: function () {
      this.service
        .getRequest("/api/table/" + this.groups[0].id)
        .then((response) => {
          this.table = response;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    initializeGroup: function () {
      this.loading = true;
      this.service
        .postRequest("/api/start-champz/1")
        .then((response) => {
          this.getGroups();
          this.resetConfirmationModal = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    knockoutStageButtonClick: function () {
      if (this.groups.length > 1) {
        this.currentGroupIndex += 1;
      } else {
        this.loading = true;
        this.generateWildcard();
      }
    },
    get_group_title() {
      if (this.currentGroupIndex == 0) {
        return "Group Stage";
      } else if (this.currentGroupIndex == 1) {
        return "Wildcard";
      } else if (this.currentGroupIndex == 2) {
        return "Semis";
      } else {
        return "Finals";
      }
    },
    nextKnockoutStageButtonClick: function () {
      if (
        this.currentGroupIndex == 1 &&
        this.currentGroupIndex + 1 == this.groups.length
      ) {
        this.generateSemis();
      } else if (
        this.currentGroupIndex == 2 &&
        this.currentGroupIndex + 2 == this.groups.length
      ) {
        this.generateFinal();
      } else {
        this.currentGroupIndex += 1;
      }
      if (this.currentGroupIndex == 3) {
        this.final = true;
      }
    },
    generateFirstKnockout: function () {
      this.loading = true;
      this.service
        .postRequest("/api/generate_1st_knockout/")
        .then((response) => {
          this.currentGroupIndex += 1;
          this.getGroups();
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    generateWildcard: function () {
      this.loading = true;
      this.service
        .postRequest("/api/generate_wildcards/")
        .then((response) => {
          console.log(response);
          this.currentGroupIndex += 1;
          this.getGroups();
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    generateSemis: function () {
      this.loading = true;
      this.service
        .postRequest("/api/generate_semis/")
        .then((response) => {
          this.currentGroupIndex += 1;
          this.getGroups();
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    generateFinal: function () {
      this.loading = true;
      this.service
        .postRequest("/api/generate_final")
        .then((response) => {
          this.getGroups();
          this.currentGroupIndex += 1;
          this.final = true;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    generateChampzFile: function () {
      this.loading = true;
      this.service
        .postRequest("/api/end_champz/")
        .then((response) => {
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    matchToGroup: function (match) {
      this.groups.forEach((element) => {
        if (match.group == element.id) {
          element.matches.push(match);
          return;
        }
      });
    },
    getMatches: function () {
      this.loading = true;
      this.service
        .getRequest("/api/match/")
        .then((response) => {
          this.matches = response;
          this.matches.forEach((element) => {
            this.matchToGroup(element);
          });
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
  },
  computed: {},
};
</script>
