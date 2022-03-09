<template>
  <v-container>
    <v-row>
      <v-card class="mx-4 pa-3" style="width: 100%">
        <v-card-title>
          <h3 style="font-weight: bold !important">Set budget</h3>
        </v-card-title>
        <v-card-text>
          <v-text-field
            class="mt-2"
            min="0"
            v-model="generic_budget"
          ></v-text-field>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row>
      <v-card class="mx-4 pa-3" style="width: 100%">
        <v-card-title>
          <h3 style="font-weight: bold !important">List of participants</h3>
          <v-spacer></v-spacer>
          <v-btn color="green" fab @click="open_participant_dialog(null)">
            <v-icon large>mdi-plus</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-row
            justify="center"
            align="center"
            v-if="participants_loading"
            class="pa-6"
          >
            <v-progress-circular
              inderteminate
              size="20"
              color="primary"
            ></v-progress-circular>
          </v-row>
          <v-simple-table v-else>
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
                      @click="delete_participant(participant.id)"
                    >
                      <v-icon>mdi-trash-can</v-icon>
                    </v-btn>
                    <v-btn
                      color="purple"
                      class="ml-2"
                      small
                      fab
                      :loading="participant.team_loading_att"
                      @click="
                        get_players_by_team(participant, participant.team.id)
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
      <v-card class="mx-4 pa-3" style="width: 100%">
        <v-card-title>
          <h3 style="font-weight: bold !important">List of Players</h3>
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
          <v-row justify="center" v-if="players_loading" class="my-6 pa-4">
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
                <tr
                  v-for="player in selected_position"
                  :key="`${player.id}-${player.team_participant}-${player.value}`"
                >
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
                    <v-btn color="green" fab @click="get_player(player)">
                      <v-icon large>mdi-cash-plus</v-icon>
                    </v-btn>
                    <v-btn
                      color="red"
                      fab
                      class="ml-2"
                      @click="remove_buy(player)"
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
          v-on:click="generate_transfers_file()"
        >Generate Transfers File</button>
        <button
          class="btn btn-outline-info"
          v-on:click="generate_players_file()"
        >Generate Players Excel</button>
        <button
          class="btn btn-outline-info"
          v-on:click="generate_teams_file()"
        >Generate Participants Teams Excel</button>
        <a style="float: right;" class="btn btn-success" :href="'/webapp/matches'">Matches</a>
      </div>
      <br />
      <br />
      <br />
    <br />-->
    <!-- Add Participant Modal -->
    <v-dialog v-model="add_participant_modal" width="40%">
      <v-card>
        <v-card-title>
          <h5>ADD PARTICIPANT</h5>
        </v-card-title>
        <v-card-text>
          <form @submit.prevent="add_participant()">
            <v-text-field
              label="Name"
              v-model="new_participant.name"
            ></v-text-field>
            <v-combobox
              v-model="new_participant.team"
              :items="
                pl_teams.filter(
                  (x) => !participants.map((p) => p.team.id).includes(x.id)
                )
              "
              item-text="name"
              label="Team"
              outlined
              dense
            ></v-combobox>
            <v-card-actions>
              <v-btn color="red" @click="add_participant_modal = false"
                >Cancel</v-btn
              >
              <v-btn type="submit" color="green" :loading="updating_participant"
                >Save changes</v-btn
              >
            </v-card-actions>
          </form>
        </v-card-text>
      </v-card>
    </v-dialog>
    <!-- Buy Player Modal -->
    <v-dialog
      v-if="buy_player_modal"
      v-model="buy_player_modal"
      width="40%"
      persistent
    >
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
                  >{{ current_player.overall }}</span
                >
                <span style="font-size: 25px; z-index: 2">{{
                  current_player.specific_position
                }}</span>
                <img
                  style="width: 60px; z-index: 2; margin: auto"
                  :src="gs.getNationImageLink(current_player.nation.image_path)"
                />
                <img
                  style="width: 60px; z-index: 2; margin: auto"
                  :src="
                    gs.getTeamImageLink(current_player.team_origin.image_path)
                  "
                />
              </div>
              <img
                :src="gs.getPlayerImageLink(current_player.image_path)"
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
                  current_player.name
                }}</span>
              </div>
              <div class="card-stats">
                <div class="vertical-divisor"></div>
                <div class="card-stats-left">
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      current_player.pace
                    }}</span
                    ><span class="mr-1 card-stat-name">PAC</span>
                  </v-row>
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      current_player.shooting
                    }}</span
                    ><span class="mr-1 card-stat-name">SHO</span>
                  </v-row>
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      current_player.passing
                    }}</span
                    ><span class="mr-1 card-stat-name">PAS</span>
                  </v-row>
                </div>
                <div class="card-stats-right text-end">
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      current_player.dribbling
                    }}</span
                    ><span class="mr-1 card-stat-name">DRI</span>
                  </v-row>
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      current_player.defending
                    }}</span
                    ><span class="mr-1 card-stat-name">DEF</span>
                  </v-row>
                  <v-row no-gutters>
                    <span class="mr-1 card-stat-value">{{
                      current_player.physical
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
          <form v-on:submit.prevent="buy_player()">
            <v-text-field
              type="number"
              v-model="current_player.value"
              label="Value"
              prefix="$"
            ></v-text-field>
            <v-combobox
              v-model="participant_selected"
              :items="participants"
              item-text="name"
              @change="
                current_player.team_participant = participant_selected.team
              "
              label="Participant"
              outlined
              dense
            ></v-combobox>
            <v-card-actions style="display: flex; justify-content: flex-end">
              <v-btn color="red" @click="reset_player_modal">Cancel</v-btn>
              <v-btn type="submit" color="green" :loading="updating_player"
                >Save changes</v-btn
              >
            </v-card-actions>
          </form>
        </v-card-text>
      </v-card>
    </v-dialog>
    <!-- Show participant team Modal -->
    <v-dialog v-model="participant_team_modal" width="60%">
      <v-card>
        <v-card-title>
          <h5>{{ current_participant.name }}'s Team</h5>
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
              <tr v-for="(player, i) in selected_team" :key="i">
                <th scope="row">{{ player.id }}</th>
                <td>{{ player.name }}</td>
                <td>{{ player.overall }}</td>
                <td>{{ player.value }}</td>
                <td>
                  <v-btn color="red" @click="remove_buy(player)">
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
    tab: 0,
    add_participant_modal: false,
    buy_player_modal: false,
    participant_team_modal: false,
    participants: [],
    generic_budget: 250,
    positions: [],
    leagues: [],
    selected_position: [],
    selected_team: [],
    pl_teams: [],
    players_loading: false,
    updating_player: false,
    removing_player: false,
    updating_participant: false,
    participants_loading: false,
    current_player: {},
    current_participant: {},
    selected_team: null,
    participant_selected: null,
    new_participant: { name: null, budget: null, team: null },
  }),
  watch: {
    participant_team_modal() {
      if (!this.participant_team_modal) {
        this.selected_team = [];
      }
    },
    tab() {
      this.get_players_by_position_algorithm(this.positions[this.tab].id);
    },
  },
  mounted: async function () {
    await this.get_participants();
    await this.get_leagues();
    await this.get_pl_teams();
    await this.get_positions();
  },
  methods: {
    reset_player_modal() {
      this.participant_selected = null;
      this.buy_player_modal = false;
    },
    get_participant_name(id) {
      if (!id) {
        return null;
      }
      return this.participants.filter((x) => x.id == id)[0].name;
    },
    open_participant_dialog: function (participant) {
      if (participant == null) {
        this.new_participant = { name: null, budget: null, team: null };
      } else {
        this.new_participant = JSON.parse(JSON.stringify(participant));
      }
      this.add_participant_modal = true;
    },
    get_participants: async function () {
      this.participants_loading = true;
      await this.service
        .getRequest("/api/participant/")
        .then((response) => {
          this.participants = response;
        })
        .catch((err) => {});
      this.participants_loading = false;
    },
    get_positions: async function () {
      this.players_loading = true;
      this.service
        .getRequest("/api/position/")
        .then((response) => {
          this.positions = response;
          this.get_players_by_position_algorithm(response[0].id);
        })
        .catch((err) => {});
      this.players_loading = false;
    },
    get_players_by_position_algorithm: async function (id_position) {
      this.players_loading = true;
      await this.service
        .getRequest("/api/player?position=" + id_position)
        .then((response) => {
          this.selected_position = response;
        })
        .catch((err) => {});
      this.players_loading = false;
    },
    get_players_by_team: async function (participant, id_team) {
      this.current_participant = participant;
      var index = this.participants.map((x) => x.id).indexOf(participant.id);
      this.participants[index].team_loading_att = true;
      await this.service
        .getRequest("/api/player?team_participant=" + id_team)
        .then((response) => {
          this.selected_team = response;
        })
        .catch((err) => {});
      this.participants[index].team_loading_att = false;
      this.participant_team_modal = true;
    },
    get_pl_teams: async function () {
      var pl = this.leagues.filter((x) => x.name.includes("ENG 1"))[0];
      await this.service
        .getRequest("/api/team?league=" + pl.id)
        .then((response) => {
          this.pl_teams = response;
        })
        .catch((err) => {});
    },
    get_leagues: async function () {
      await this.service
        .getRequest("/api/league/")
        .then((response) => {
          this.leagues = response;
        })
        .catch((err) => {});
    },
    get_player: function (player) {
      this.current_player = JSON.parse(JSON.stringify(player));
      this.buy_player_modal = true;
    },
    add_participant: async function () {
      this.updating_participant = true;
      this.new_participant.team = this.new_participant.team.id;
      if (!this.new_participant.id) {
        this.new_participant.budget = this.generic_budget;
        await this.service
          .postRequest("/api/participant/", this.new_participant)
          .then((response) => {
            this.participants.push(response);
            this.new_participant.name = null;
            this.new_participant.budget = null;
            this.new_participant.team = null;
            this.add_participant_modal = false;
            this.get_players_by_position_algorithm(this.positions[this.tab].id);
          })
          .catch((err) => {});
      } else {
        await this.service
          .patchRequest(
            `/api/participant/${this.new_participant.id}/`,
            this.new_participant
          )
          .then((response) => {
            var index = this.participants
              .map((x) => x.id)
              .indexOf(this.new_participant.id);
            this.participants = this.participants
              .slice(0, index)
              .concat([response])
              .concat(
                this.participants.slice(index + 1, this.participants.length)
              );
            this.add_participant_modal = false;
            this.get_players_by_position_algorithm(this.positions[this.tab].id);
          })
          .catch((err) => {});
      }
      this.updating_participant = false;
    },
    delete_participant: async function (id) {
      var url = "/api/participant/" + id + "/";
      var index = this.participants.map((x) => x.id).indexOf(id);
      this.participants.splice(index, 1);
      await this.service
        .deleteRequest(url)
        .then((response) => {
          this.get_players_by_position_algorithm(this.positions[this.tab].id);
        })
        .catch((err) => {});
    },
    remove_buy: async function (player) {
      this.update_participant_budget(player, true);
      await this.service
        .postRequest(`/api/buy/${player.id}`, { team_participant: null })
        .then((response) => {
          this.update_player(response);
          if (this.selected_team.length > 0) {
            var index = this.selected_team.map((x) => x.id).indexOf(player.id);
            if (index != -1) {
              this.selected_team.splice(index, 1);
            }
          }
        })
        .catch((err) => {});
    },
    update_participant_budget(player, add) {
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
    update_player(player) {
      if (this.positions[this.tab].id == player.position.id) {
        var index = this.selected_position.map((x) => x.id).indexOf(player.id);
        this.selected_position = this.selected_position
          .slice(0, index)
          .concat([player])
          .concat(
            this.selected_position.slice(
              index + 1,
              this.selected_position.length
            )
          );
      }
    },
    async buy_player() {
      this.updating_player = true;
      var player = JSON.parse(JSON.stringify(this.current_player));
      player.team_participant = this.current_player.team_participant.id;
      var url = "/api/buy/" + this.current_player.id;
      await this.service
        .postRequest(url, player)
        .then((response) => {
          var player = response;
          this.update_player(player);
          this.update_participant_budget(player, false);
          this.participant_selected = null;
          this.buy_player_modal = false;
        })
        .catch((err) => {});
      this.updating_player = false;
    },
    generate_transfers_file: async function () {
      var url = "/api/transfers/";
      await this.service
        .postRequest(url)
        .then((response) => {})
        .catch((err) => {});
    },
    generate_teams_file: async function () {
      var url = "/api/participants_teams/";
      await this.service
        .postRequest(url)
        .then((response) => {})
        .catch((err) => {});
    },
    generate_players_file: async function () {
      var url = "/api/champz_players/";
      await this.service
        .postRequest(url)
        .then((response) => {})
        .catch((err) => {});
    },
  },
  computed: {},
};
</script>
