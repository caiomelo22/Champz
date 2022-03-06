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
                    <img
                      style="width: 30px"
                      :src="gs.getTeamImageLink(participant.team.image_path)"
                    />
                    {{ participant.team.name }}
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
                        getPlayersByTeam(participant.id, participant.team.id);
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
          <v-simple-table class="mt-4" v-else-if="tab != -1">
            <template v-slot:default>
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">
                    <b>Player</b>
                  </th>
                  <th></th>
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
                  <td class="champzFont">
                    <img
                      :src="gs.getPlayerImageLink(player.image_path)"
                      style="max-height: 80px"
                    />
                    <img
                      style="width: 30px"
                      :src="gs.getNationImageLink(player.nation.image_path)"
                    />
                    <img
                      style="width: 30px"
                      :src="gs.getTeamImageLink(player.team_origin.image_path)"
                    />
                  </td>
                  <td class="champzFont">
                    <span>{{ player.name }}</span>
                  </td>
                  <td class="champzFont">{{ player.overall }}</td>
                  <td class="champzFont">{{ player.specific_position }}</td>
                  <td class="champzFont">
                    {{
                      player.team_participant
                        ? get_participant_name(
                            player.team_participant.participant
                          )
                        : "-"
                    }}
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
                      @click="removeBuy(player)"
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
    <v-dialog v-if="buyPlayerModal" v-model="buyPlayerModal" width="40%">
      <v-card>
        <v-card-title>
          <h5>BUY PLAYER</h5>
        </v-card-title>
        <v-card-text>
          <div
            class="text-center"
            style="display: flex; justify-content: center; position: relative"
          >
            <div class="card-info">
              <div class="card-left-info">
                <span
                  style="
                    margin-bottom: 10px;
                    font-size: 40px;
                    font-weight: bold;
                    z-index: 2;
                  "
                  >{{ currentPlayer.overall }}</span
                >
                <span style="font-size: 25px; z-index: 2">{{
                  currentPlayer.specific_position
                }}</span>
                <img
                  style="width: 60px; z-index: 2; margin: auto"
                  :src="gs.getNationImageLink(currentPlayer.nation.image_path)"
                />
                <img
                  style="width: 60px; z-index: 2; margin: auto"
                  :src="
                    gs.getTeamImageLink(currentPlayer.team_origin.image_path)
                  "
                />
              </div>
              <img
                :src="gs.getPlayerImageLink(currentPlayer.image_path)"
                style="
                  max-height: 160px;
                  z-index: 2;
                  position: absolute;
                  top: 100px;
                  left: -28px;
                "
              />
              <div class="card-name">
                <span style="font-weight: 700; font-size: 17px">{{
                  currentPlayer.name
                }}</span>
              </div>
              <div class="card-stats">
                <div class="vertical-divisor"></div>
                <div class="card-stats-left">
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      currentPlayer.pace
                    }}</span
                    ><span class="mr-1 card-stat-name">PAC</span>
                  </v-row>
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      currentPlayer.shooting
                    }}</span
                    ><span class="mr-1 card-stat-name">SHO</span>
                  </v-row>
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      currentPlayer.passing
                    }}</span
                    ><span class="mr-1 card-stat-name">PAS</span>
                  </v-row>
                </div>
                <div class="card-stats-right text-end">
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      currentPlayer.dribbling
                    }}</span
                    ><span class="mr-1 card-stat-name">DRI</span>
                  </v-row>
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      currentPlayer.defending
                    }}</span
                    ><span class="mr-1 card-stat-name">DEF</span>
                  </v-row>
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      currentPlayer.physical
                    }}</span
                    ><span class="mr-1 card-stat-name">PHY</span>
                  </v-row>
                </div>
              </div>
            </div>
            <img
              src="../../../assets/gold.png"
              style="height: 500px; z-index: 1"
            />
          </div>
          <form v-on:submit.prevent="buyPlayer()">
            <v-text-field
              type="number"
              v-model="currentPlayer.value"
              label="Value"
              prefix="$"
            ></v-text-field>
            <v-combobox
              v-model="participant_selected"
              :items="participants"
              item-text="name"
              @change="
                currentPlayer.team_participant = participant_selected.team
              "
              label="Participant"
              outlined
              dense
            ></v-combobox>
            <v-card-actions style="display: flex; justify-content: flex-end">
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
                      removeBuy(player);
                      getPlayersByTeam(
                        currentParticipant.id,
                        currentParticipant.team.id
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
.card-info {
  position: absolute;
}
.card-stat-name {
  font-weight: 400;
}
.card-stat-value {
  font-weight: bold;
}
.vertical-divisor {
  height: 100%;
  width: 1px;
  top: 65%;
  opacity: 0.8;
  margin-left: auto;
  margin-right: auto;
  display: block;
  background-color: #645215;
}
.card-name {
  z-index: 2;
  position: absolute;
  top: 261px;
  left: -137px;
  width: 273px;
}
.card-stats-left {
  position: absolute;
  width: 50%;
  bottom: 16px;
  padding-left: 50px;
  font-size: 20px;
}
.card-stats-right {
  position: absolute;
  width: 50%;
  bottom: 16px;
  right: 0;
  padding-left: 20px;
  font-size: 20px;
}
.card-stats {
  z-index: 2;
  position: absolute;
  top: 300px;
  left: -136px;
  height: 102px;
  width: 273px;
}
.card-left-info {
  z-index: 2;
  display: grid;
  margin-left: -120px;
  margin-top: 63px;
}
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
    edit: false,
    nations: [],
    positions: [],
    leagues: [],
    selectedPosition: [],
    selectedTeam: [],
    plTeams: [],
    loading: false,
    currentPlayer: {},
    currentParticipant: {},
    selectedTeam: null,
    participant_selected: null,
    newParticipant: { name: null, budget: null, team: null },
  }),
  watch: {
    tab() {
      this.getPlayersByPosition(this.positions[this.tab].id);
    },
  },
  mounted: async function () {
    await this.getParticipants();
    await this.getLeagues();
    await this.getPLTeams();
    await this.getPositions();
  },
  methods: {
    get_participant_name(id) {
      if (!id) {
        return null;
      }
      return this.participants.filter((x) => x.id == id)[0].name;
    },
    open_participant_dialog: function (participant) {
      if (participant == null) {
        this.edit = false;
        this.newParticipant = { name: null, budget: null, team: null };
        this.addParticipantModal = true;
      } else {
        this.newParticipant = JSON.parse(JSON.stringify(participant));
        this.edit = true;
        this.addParticipantModal = true;
      }
    },
    getParticipants: async function () {
      this.loading = true;
      await this.service
        .getRequest("/api/participant/")
        .then((response) => {
          this.participants = response;
        })
        .catch((err) => {});
      this.loading = false;
    },
    getPositions: async function () {
      this.loading = true;
      this.service
        .getRequest("/api/position/")
        .then((response) => {
          this.positions = response;
          this.getPlayersByPosition(response[0].id);
        })
        .catch((err) => {});
      this.loading = false;
    },
    getPlayersByPosition: async function (id_position) {
      this.loading = true;
      await this.service
        .getRequest("/api/player?position=" + id_position)
        .then((response) => {
          this.selectedPosition = response;
        })
        .catch((err) => {});
      this.loading = false;
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
    getPLTeams: async function () {
      this.loading = true;
      var pl = this.leagues.filter((x) => x.name.includes("ENG 1"))[0];
      await this.service
        .getRequest("/api/team?league=" + pl.id)
        .then((response) => {
          this.plTeams = response;
        })
        .catch((err) => {});
      this.loading = false;
    },
    getLeagues: async function () {
      this.loading = true;
      await this.service
        .getRequest("/api/league/")
        .then((response) => {
          this.leagues = response;
        })
        .catch((err) => {});
      this.loading = false;
    },
    getPlayer: function (player) {
      this.currentPlayer = JSON.parse(JSON.stringify(player))
      this.buyPlayerModal = true;
    },
    addParticipant: async function () {
      this.loading = true;
      if (!this.edit) {
        this.newParticipant.budget = this.genericBudget;
        this.newParticipant.team = this.newParticipant.team.id;
        await this.service
          .postRequest("/api/participant/", this.newParticipant)
          .then((response) => {
            this.participants.push(response);
            this.newParticipant.name = null;
            this.newParticipant.budget = null;
            this.newParticipant.team = null;
            this.tab = -1;
            this.addParticipantModal = false;
          })
          .catch((err) => {});
        this.loading = false;
      } else {
        this.updateParticipant();
      }
    },
    updateParticipant: async function () {
      this.loading = true;
      var url = "/api/participant/" + this.newParticipant.id + "/";
      this.newParticipant.team = this.newParticipant.team.id;
      await this.service
        .patchRequest(url, this.newParticipant)
        .then((response) => {
          var index = this.participants
            .map((x) => x.id)
            .indexOf(this.newParticipant.id);
          this.participants[index] = response;
          this.tab = -1;
          this.addParticipantModal = false;
        })
        .catch((err) => {});
      this.loading = false;
    },
    deleteParticipant: async function (id) {
      this.loading = true;
      var url = "/api/participant/" + id + "/";
      await this.service
        .deleteRequest(url)
        .then((response) => {
          var index = this.participants.map((x) => x.id).indexOf(id);
          this.participants.splice(index, 1);
        })
        .catch((err) => {});
      this.loading = false;
    },
    removeBuy: async function (player) {
      this.loading = true;
      this.updateParticipantBudget(player, true);
      var url = "/api/buy/" + player.id;
      await this.service
        .postRequest(url, { team_participant: null })
        .then((response) => {
          var index = this.selectedPosition.indexOf(player);
          if (index != -1) {
            this.selectedPosition[index] = response;
          }
        })
        .catch((err) => {});
      this.loading = false;
    },
    updateParticipantBudget(player, add) {
      var index = this.participants
        .map((x) => x.team.id)
        .indexOf(player.team_participant.id);
      if (index != -1) {
        if (add) {
          this.participants[index].budget += player.value;
        } else {
          this.participants[index].budget -= player.value;
        }
      }
    },
    updatePlayer(player) {
      var index = this.selectedPosition
        .map((x) => x.id)
        .indexOf(player.id);
      this.selectedPosition[index] = player;
    },
    async buyPlayer() {
      this.playersLoading = true;
      var player = JSON.parse(JSON.stringify(this.currentPlayer));
      player.team_participant = this.currentPlayer.team_participant.id;
      var url = "/api/buy/" + this.currentPlayer.id;
      await this.service
        .postRequest(url, player)
        .then((response) => {
          var player = response;
          this.updatePlayer(player);
          this.updateParticipantBudget(player);
          this.buyPlayerModal = false;
        })
        .catch((err) => {});
      this.playersLoading = false;
    },
    generateTransfersFile: async function () {
      this.loading = true;
      var url = "/api/transfers/";
      await this.service
        .postRequest(url)
        .then((response) => {})
        .catch((err) => {});
      this.loading = false;
    },
    generateTeamsFile: async function () {
      this.loading = true;
      var url = "/api/participants_teams/";
      await this.service
        .postRequest(url)
        .then((response) => {})
        .catch((err) => {});
      this.loading = false;
    },
    generatePlayersFile: async function () {
      this.loading = true;
      var url = "/api/champz_players/";
      await this.service
        .postRequest(url)
        .then((response) => {})
        .catch((err) => {});
      this.loading = false;
    },
  },
  computed: {},
};
</script>
