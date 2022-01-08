<template>
  <v-container v-if="!loading">
    <v-row>
      <v-card class="mx-4" style="width: 100%">
        <v-card-title>
          <h3>Set budget</h3>
        </v-card-title>
        <v-card-text>
          <v-text-field
            class="mt-2"
            min="0"
            v-model="genericBudget"
          ></v-text-field>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row>
      <v-card class="mx-4" style="width: 100%">
        <v-card-title>
          <h3>List of participants</h3>
          <v-spacer></v-spacer>
          <v-btn color="green" fab @click="open_participant_dialog(null)">
            <v-icon large>mdi-plus</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">
                    <b>Name</b>
                  </th>
                  <th scope="col">
                    <b>Budget</b>
                  </th>
                  <th scope="col">
                    <b>Team</b>
                  </th>
                  <th scope="col">
                    <b>Action</b>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(participant, i) in participants" :key="i">
                  <td class="champzFont">{{ participant.id }}</td>
                  <td class="champzFont">{{ participant.name }}</td>
                  <td class="champzFont">${{ participant.budget }}</td>
                  <td class="champzFont">
                    <!-- <img
                      style="width:30px;"
                      :src="getPlayerTeam(getParticipantTeam(participant.id).id).image_link"
                    />-->
                    {{ getParticipantTeam(participant.id).name }}
                  </td>
                  <td>
                    <v-btn
                      color="blue"
                      small
                      fab
                      @click="open_participant_dialog(participant)"
                    >
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn
                      color="red"
                      class="ml-2"
                      small
                      fab
                      @click="deleteParticipant(participant.id)"
                    >
                      <v-icon>mdi-trash-can</v-icon>
                    </v-btn>
                    <v-btn
                      color="purple"
                      class="ml-2"
                      small
                      fab
                      :loading="participant.teamLoading"
                      @click="
                        currentParticipant = participant;
                        getPlayersByTeam(
                          participant.id,
                          getParticipantTeam(participant.id).id
                        );
                        showParticipantTeamModal = true;
                      "
                    >
                      <v-icon>mdi-eye</v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card-text>
      </v-card>
    </v-row>

    <v-row>
      <v-card class="mx-4" style="width: 100%">
        <v-card-title>
          <h3>List of Players</h3>
        </v-card-title>
        <v-card-text>
          <v-tabs v-model="tab">
            <v-tab>Goalkeepers</v-tab>
            <v-tab>Center Backs</v-tab>
            <v-tab>Full Backs</v-tab>
            <v-tab>Defensive Midfielders</v-tab>
            <v-tab>Ofensive Midfielders</v-tab>
            <v-tab>Wingers</v-tab>
            <v-tab>Attackers</v-tab>
          </v-tabs>
          <v-row justify="center" v-if="playersLoading" class="my-6">
            <v-progress-circular indeterminate size="15"></v-progress-circular>
          </v-row>
          <v-simple-table class="mt-4" v-else>
            <template v-slot:default>
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">
                    <b>Player</b>
                  </th>
                  <th scope="col">
                    <b>Overall</b>
                  </th>
                  <th scope="col">
                    <b>Position</b>
                  </th>
                  <th scope="col">
                    <b>Owner</b>
                  </th>
                  <th scope="col">
                    <b>Price</b>
                  </th>
                  <th scope="col">
                    <b>Action</b>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(player, i) in selectedPosition" :key="i">
                  <td class="champzFont">{{ player.id }}</td>
                  <!-- <td class="champzFont">
                    <img :src="gs.getPlayerImageLink(player.image_link)">
                  </td> -->
                  <td class="champzFont">
                    <!-- <img class="mb-2" style="width:30px;" :src="getPlayerNation(player.nation).image_link" />
                    <img class="ml-1" style="width:30px;" :src="getPlayerTeam(player.team_origin).image_link" />-->
                    <span>{{ player.name }}</span>
                  </td>
                  <td class="champzFont">{{ player.overall }}</td>
                  <td class="champzFont">{{ player.specific_position }}</td>
                  <td class="champzFont">
                    <!-- <img
                      v-show="player.team_participant!=null"
                      style="width:30px;"
                      :src="getPlayerTeam(player.team_participant).image_link"
                    />-->
                    {{ getPlayerOwner(player.team_participant) }}
                  </td>
                  <td class="champzFont">${{ player.value }}</td>
                  <td>
                    <v-btn color="green" fab @click="getPlayer(player)">
                      <v-icon large>mdi-cash-plus</v-icon>
                    </v-btn>
                    <v-btn
                      color="red"
                      fab
                      class="ml-2"
                      @click="removeBuy(player.id)"
                    >
                      <v-icon large>mdi-cash-minus</v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card-text>
      </v-card>
    </v-row>

    <!-- <h3>List of Players</h3>
      
      <div class="container">
        <button
          class="btn btn-outline-info"
          v-on:click="generateTransfersFile()"
        >Generate Transfers File</button>
        <button
          class="btn btn-outline-info"
          v-on:click="generatePlayersFile()"
        >Generate Players Excel</button>
        <button
          class="btn btn-outline-info"
          v-on:click="generateTeamsFile()"
        >Generate Participants Teams Excel</button>
        <a style="float: right;" class="btn btn-success" :href="'/webapp/matches'">Matches</a>
      </div>
      <br />
      <br />
      <br />
    <br />-->
    <!-- Add Participant Modal -->
    <v-dialog v-model="addParticipantModal" width="40%">
      <v-card>
        <v-card-title>
          <h5>ADD PARTICIPANT</h5>
        </v-card-title>
        <v-card-text>
          <form @submit.prevent="addParticipant()">
            <v-text-field
              label="Name"
              v-model="newParticipant.name"
            ></v-text-field>
            <v-combobox
              v-model="newParticipant.team"
              :items="plTeams"
              item-text="name"
              label="Team"
              outlined
              dense
            ></v-combobox>
            <v-card-actions>
              <v-btn color="red" @click="addParticipantModal = false"
                >Cancel</v-btn
              >
              <v-btn type="submit" color="green">Save changes</v-btn>
            </v-card-actions>
          </form>
        </v-card-text>
      </v-card>
    </v-dialog>
    <!-- Buy Player Modal -->
    <v-dialog v-model="buyPlayerModal" width="40%">
      <v-card>
        <v-card-title>
          <h5>BUY PLAYER</h5>
        </v-card-title>
        <v-card-text>
          <h4>{{ currentPlayer.name }}</h4>
          <form v-on:submit.prevent="buyPlayer()">
            <v-text-field
              type="number"
              v-model="currentPlayer.value"
              label="Value"
              prefix="$"
            ></v-text-field>
            <v-combobox
              v-model="currentPlayer.team_participant"
              :items="participants"
              item-text="name"
              label="Participant"
              outlined
              dense
            ></v-combobox>
            <v-card-actions>
              <v-btn color="red" @click="buyPlayerModal = false">Cancel</v-btn>
              <v-btn type="submit" color="green">Save changes</v-btn>
            </v-card-actions>
          </form>
        </v-card-text>
      </v-card>
    </v-dialog>
    <!-- Show participant team Modal -->
    <v-dialog v-model="showParticipantTeamModal" width="40%">
      <v-card>
        <v-card-title>
          <h5>{{ currentParticipant.name }}'s Team</h5>
        </v-card-title>
        <v-card-text>
          <v-simple-table>
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Overall</th>
                <th scope="col">Price</th>
                <th scope="col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(player, i) in selectedTeam" :key="i">
                <th scope="row">{{ player.id }}</th>
                <td>{{ player.name }}</td>
                <td>{{ player.overall }}</td>
                <td>{{ player.value }}</td>
                <td>
                  <v-btn
                    color="red"
                    @click="
                      removeBuy(player.id);
                      getPlayersByTeam(
                        currentParticipant.id,
                        getParticipantTeam(currentParticipant.id).id
                      );
                    "
                  >
                    Remove Buy
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
        </v-card-text>
      </v-card>
    </v-dialog>
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
  font-size: 18px;
  font-weight: 500;
  font-family: system-ui;
}
</style>

<script>
import Service from "@/services/Service";
import GeneralServices from "@/services/GeneralServices";
export default {
  name: "Draft",
  data: () => ({
    gs: new GeneralServices(),
    service: new Service(),
    playersLoading: false,
    tab: 0,
    addParticipantModal: false,
    buyPlayerModal: false,
    showParticipantTeamModal: false,
    participants: [],
    genericBudget: 250,
    teams: [],
    edit: false,
    nations: [],
    positions: [],
    leagues: [],
    selectedPosition: [],
    selectedTeam: [],
    keepers: [],
    fullBacks: [],
    centerBacks: [],
    defensiveMids: [],
    attackingMids: [],
    wingers: [],
    attackers: [],
    plTeams: [],
    loading: false,
    currentPlayer: {},
    currentParticipant: {},
    selectedTeam: null,
    newParticipant: { name: null, budget: null, team: null },
  }),
  watch: {
    tab() {
      if (this.tab == 0) {
        this.selectedPosition = this.keepers;
      } else if (this.tab == 1) {
        this.selectedPosition = this.centerBacks;
      } else if (this.tab == 2) {
        this.selectedPosition = this.fullBacks;
      } else if (this.tab == 3) {
        this.selectedPosition = this.defensiveMids;
      } else if (this.tab == 4) {
        this.selectedPosition = this.attackingMids;
      } else if (this.tab == 5) {
        this.selectedPosition = this.wingers;
      } else if (this.tab == 6) {
        this.selectedPosition = this.attackers;
      }
    },
  },
  mounted: function () {
    this.getParticipants();
    this.getLeagues();
    this.getTeams();
    this.getNations();
    this.getPositions();
  },
  methods: {
    select_cbx_item: function (id, array) {
      var i;
      for (i = 0; i < array.length; i++) {
        if (array[i].id == id) {
          return array[i];
        }
      }
    },
    open_participant_dialog: function (participant) {
      if (participant == null) {
        this.edit = false;
        this.newParticipant = { name: null, budget: null, team: null };
        this.addParticipantModal = true;
      } else {
        this.newParticipant = participant;
        this.edit = true;
        this.newParticipant.team = this.getParticipantTeam(participant.id);
        this.addParticipantModal = true;
      }
    },
    getParticipants: function () {
      this.loading = true;
      this.service
        .getRequest("/api/participant/")
        .then((response) => {
          response = response.map((x) => {
            x.teamLoading = false;
            return x;
          });
          this.participants = response;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log("erro", err);
        });
    },
    getTeams: function () {
      this.loading = true;
      this.service
        .getRequest("/api/team/")
        .then((response) => {
          this.teams = response;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    getNations: function () {
      this.loading = true;
      this.service
        .getRequest("/api/nation/")
        .then((response) => {
          this.nations = response;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    getPositions: function () {
      this.loading = true;
      this.service
        .getRequest("/api/position/")
        .then((response) => {
          this.positions = response;
          this.getPlayersByPosition(response[6].id);
          this.getPlayersByPosition(response[5].id);
          this.getPlayersByPosition(response[4].id);
          this.getPlayersByPosition(response[3].id);
          this.getPlayersByPosition(response[2].id);
          this.getPlayersByPosition(response[1].id);
          this.getPlayersByPosition(response[0].id);
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    compare: function (a, b) {
      if (a.overall - b.overall == 0) {
        return a.pace - b.pace;
      } else {
        return a.overall - b.overall;
      }
    },
    selectPlayers: function (a, b) {
      if (a.overall > b.overall) {
        return 1;
      } else if (a.overall < b.overall) {
        return -1;
      }

      // Else go to the 2nd item
      if (a.pace < b.pace) {
        return -1;
      } else if (a.pace > b.pace) {
        return 1;
      } else {
        // nothing to split them
        return 0;
      }
      // return (
      //   (a.overall * 100 + a.likes) / 101 - (b.overall * 100 + b.likes) / 101
      // );
    },
    filterPlayers: function (array, n) {
      console.log(array);
      array.sort(this.selectPlayers);
      array.reverse();
      array = array.slice(0, Math.round(n * this.participants.length));
      array.sort(this.compare);
      array.reverse();
      return array;
    },
    getPlayersByPosition: function (id_position) {
      this.loading = true;
      this.service
        .getRequest("/api/player?position=" + id_position)
        .then((response) => {
          if (id_position === this.positions[0].id) {
            this.keepers = response;
            this.keepers = this.filterPlayers(this.keepers, 1.5);
            this.selectedPosition = this.keepers;
          } else if (id_position === this.positions[1].id) {
            this.centerBacks = response;
            this.centerBacks = this.filterPlayers(this.centerBacks, 3);
            this.selectedPosition = this.centerBacks;
          } else if (id_position === this.positions[2].id) {
            this.fullBacks = response;
            this.fullBacks = this.filterPlayers(this.fullBacks, 3);
            this.selectedPosition = this.fullBacks;
          } else if (id_position === this.positions[3].id) {
            this.defensiveMids = response;
            this.defensiveMids = this.filterPlayers(this.defensiveMids, 3);
            this.selectedPosition = this.defensiveMids;
          } else if (id_position === this.positions[4].id) {
            this.attackingMids = response;
            this.attackingMids = this.filterPlayers(this.attackingMids, 1.5);
            this.selectedPosition = this.attackingMids;
          } else if (id_position === this.positions[5].id) {
            this.wingers = response;
            this.wingers = this.filterPlayers(this.wingers, 2.5);
            this.selectedPosition = this.wingers;
          } else if (id_position === this.positions[6].id) {
            this.attackers = response;
            this.attackers = this.filterPlayers(this.attackers, 2);
            this.selectedPosition = this.attackers;
          }
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    getPlayersByTeam: function (participant_id, id_team) {
      var index = this.participants.map((x) => x.id).indexOf(participant_id);
      this.participants[index].teamLoading = true;
      return this.service
        .getRequest("/api/player?team_participant=" + id_team)
        .then((response) => {
          this.selectedTeam = response;
          this.participants[index].teamLoading = false;
          return response;
        })
        .catch((err) => {
          this.participants[index].teamLoading = false;
          console.log(err);
        });
    },
    getPLTeams: function () {
      this.loading = true;
      this.service
        .getRequest("/api/team?league=" + this.leagues[1].id)
        .then((response) => {
          this.plTeams = response;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    getLeagues: function () {
      this.loading = true;
      this.service
        .getRequest("/api/league/")
        .then((response) => {
          this.leagues = response;
          this.getPLTeams();
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    getPlayerTeam: function (id) {
      var obj = {};
      this.teams.forEach((element) => {
        if (element.id === id) {
          obj = element;
          return obj;
        }
      });
      return obj;
    },
    getPlayerNation: function (id) {
      var obj = {};
      this.nations.forEach((element) => {
        if (element.id === id) {
          obj = element;
          return obj;
        }
      });
      return obj;
    },
    getPlayer: function (player) {
      // this.currentPlayer = player;
      this.currentPlayer = Object.assign({}, player);
      if (this.currentPlayer.team_participant != null) {
        this.currentPlayer.team_participant = this.getPlayerTeam(
          this.currentPlayer.team_participant
        );
      }
      this.buyPlayerModal = true;

      // var url = "/api/player/" + id + "/";
      // this.service
      //   .getRequest(url)
      //   .then((response) => {
      //     this.currentPlayer = response;
      //     console.log(this.currentPlayer);
      //     this.buyPlayerModal = true;
      //     this.loading = false;
      //   })
      //   .catch((err) => {
      //     this.loading = false;
      //     console.log(err);
      //   });
    },
    getPlayerOwner: function (id) {
      // console.log('were in boys');
      var owner, team, name;
      owner = "";
      if (id != null) {
        // console.log('hello again');
        this.participants.forEach((element) => {
          team = this.getParticipantTeam(element.id);
          if (team.id === id) {
            name = element.name;
            owner = name;
            return owner;
          }
        });
      }
      return owner;
    },
    getParticipantTeam: function (id) {
      var team = {};
      this.plTeams.forEach((element) => {
        if (element.participant === id) {
          team = element;
          return team;
        }
      });
      return team;
    },
    addParticipant: function () {
      this.loading = true;
      if (!this.edit) {
        this.newParticipant.budget = this.genericBudget;
        this.newParticipant.team = this.newParticipant.team.id;
        this.service
          .postRequest("/api/participant/", this.newParticipant)
          .then((response) => {
            this.getParticipants();
            this.getPLTeams();
            this.getPositions();
            this.loading = false;
            this.newParticipant.name = null;
            this.newParticipant.budget = null;
            this.newParticipant.team = null;
            this.selectedPosition = null;
            this.addParticipantModal = false;
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          });
      } else {
        this.updateParticipant();
      }
    },
    updateParticipant: function () {
      this.loading = true;
      var url = "/api/participant/" + this.newParticipant.id + "/";
      this.newParticipant.team = this.newParticipant.team.id;
      this.service
        .patchRequest(url, this.newParticipant)
        .then((response) => {
          this.getParticipants();
          this.getPLTeams();
          this.getPositions();
          this.selectedPosition = null;
          this.addParticipantModal = false;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err.body);
        });
    },
    deleteParticipant: function (id) {
      console.log(id);
      this.loading = true;
      var url = "/api/participant/" + id + "/";
      console.log(url);
      this.service
        .deleteRequest(url)
        .then((response) => {
          this.loading = false;
          this.getParticipants();
          this.getPLTeams();
          this.getPositions();
          this.selectedPosition = [];
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    removeBuy: function (id) {
      this.loading = true;
      var url = "/api/buy/" + id;
      this.service
        .postRequest(url, { team_participant: null })
        .then((response) => {
          this.loading = false;
          this.currentPlayer = response;
          this.getPlayersByPosition(this.currentPlayer.position);
          this.getParticipants();
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    updateParticipantBudget() {
      var index = this.participants
        .map((x) => x.team)
        .indexOf(this.currentPlayer.team_participant);
      this.participants[index].budget -= this.currentPlayer.value;
    },
    updatePlayer() {
      var index = this.selectedPosition
        .map((x) => x.id)
        .indexOf(this.currentPlayer.id);
      this.selectedPosition[index] = this.currentPlayer;
    },
    async buyPlayer() {
      this.buyPlayerModal = false;
      this.playersLoading = true;
      this.currentPlayer.team_participant =
        this.currentPlayer.team_participant.team;
      var url = "/api/buy/" + this.currentPlayer.id;
      await this.service
        .postRequest(url, this.currentPlayer)
        .then((response) => {
          this.currentPlayer = response;
          this.updatePlayer();
          this.updateParticipantBudget();
        })
        .catch((err) => {
          console.log(err);
        });
      this.playersLoading = false;
    },
    generateTransfersFile: function () {
      this.loading = true;
      var url = "/api/transfers/";
      this.service
        .postRequest(url)
        .then((response) => {
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    generateTeamsFile: function () {
      this.loading = true;
      var url = "/api/participants_teams/";
      this.service
        .postRequest(url)
        .then((response) => {
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        });
    },
    generatePlayersFile: function () {
      this.loading = true;
      var url = "/api/champz_players/";
      this.service
        .postRequest(url)
        .then((response) => {
          this.loading = false;
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
