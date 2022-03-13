<template>
  <v-container>
    <v-row v-if="loading" justify="center" align="center" class="pa-4">
      <v-progress-circular indeterminate size="40" color="primary">
      </v-progress-circular>
    </v-row>
    <div v-else>
      <v-card style="height: 100%">
        <v-toolbar color="primary" dark>
          <v-btn
            :disabled="!current_group_index"
            fab
            text
            large
            @click="previous_stage_click"
          >
            <v-icon dark large>mdi-chevron-left</v-icon>
          </v-btn>
          <v-toolbar-title class="mx-auto">{{
            selected_group.name
          }}</v-toolbar-title>
          <v-btn fab text large @click="next_stage_click">
            <v-icon dark large>mdi-chevron-right</v-icon>
          </v-btn>
        </v-toolbar>
        <v-row
          v-if="group_loading"
          justify="center"
          align="center"
          class="pa-4"
        >
          <v-progress-circular indeterminate size="20" color="primary">
          </v-progress-circular>
        </v-row>
        <v-row v-else>
          <v-col v-if="current_group_index == 0" cols="12" md="8">
            <v-row>
              <v-col cols="12" md="11">
                <h4 class="text-center my-6">{{ selected_group.name }}</h4>
                <table class="table table-striped ml-7">
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
                    <tr v-for="(participant, i) in table" :key="i">
                      <td class="champzFont">
                        <img
                          style="width: 30px"
                          :src="
                            gs.get_team_image_path(
                              participant[0].team.image_path
                            )
                          "
                        />
                        {{ participant[0].name.toUpperCase() }}
                      </td>
                      <td class="champzFont">{{ participant[1].P }}</td>
                      <td class="champzFont">{{ participant[1].W }}</td>
                      <td class="champzFont">{{ participant[1].D }}</td>
                      <td class="champzFont">{{ participant[1].L }}</td>
                      <td class="champzFont">{{ participant[1].GF }}</td>
                      <td class="champzFont">{{ participant[1].GA }}</td>
                      <td class="champzFont">{{ participant[1].GD }}</td>
                    </tr>
                  </tbody>
                </table>
                <v-divider></v-divider>
              </v-col>
              <v-col cols="12" md="1" class="champzDivider">
                <v-divider class="ml-8" vertical></v-divider>
              </v-col>
            </v-row>
          </v-col>
          <v-col
            cols="12"
            :md="current_group_index ? 12 : 4"
            :class="current_group_index ? 'champzKnockout' : 'champzMatches'"
          >
            <h5 class="text-center mt-3">{{ selected_group.name }}</h5>
            <v-simple-table :class="current_group_index ? 'mx-8' : 'mr-0'">
              <template v-slot:default>
                <thead class="thead-dark">
                  <tr>
                    <th class="champzFont" scope="col">Match</th>
                    <th class="champzFont" scope="col">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(match, i) in selected_group.matches" :key="i">
                    <td
                      class="champzFont text-center"
                      v-if="
                        match.goals_participant_1 == null &&
                        match.goals_participant_2 == null
                      "
                    >
                      {{ match.participant_1.name.toUpperCase() }}

                      <img
                        style="width: 30px"
                        :src="
                          gs.get_team_image_path(
                            match.participant_1.team.image_path
                          )
                        "
                      />
                      X
                      <img
                        style="width: 30px"
                        :src="
                          gs.get_team_image_path(
                            match.participant_2.team.image_path
                          )
                        "
                      />
                      {{ match.participant_2.name.toUpperCase() }}
                    </td>
                    <td class="champzFont text-center" v-else>
                      {{ match.participant_1.name.toUpperCase() }}
                      <img
                        style="width: 30px"
                        :src="
                          gs.get_team_image_path(
                            match.participant_1.team.image_path
                          )
                        "
                      />
                      {{ match.goals_participant_1 }} X
                      {{ match.goals_participant_2 }}
                      <img
                        style="width: 30px"
                        :src="
                          gs.get_team_image_path(
                            match.participant_2.team.image_path
                          )
                        "
                      />
                      {{ match.participant_2.name.toUpperCase() }}
                    </td>
                    <td>
                      <v-btn
                        small
                        fab
                        color="primary"
                        @click="get_match(match)"
                      >
                        <v-icon small>mdi-pencil</v-icon>
                      </v-btn>
                    </td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
            <v-divider></v-divider>
          </v-col>
        </v-row>
        <div class="text-center">
          <v-btn
            large
            class="mx-auto mb-12"
            light
            color="primary"
            v-if="final"
            v-on:click="generate_champz_file()"
            >Generate Champz File</v-btn
          >
        </div>
      </v-card>
      <v-spacer></v-spacer>
      <a @click="reset_confirmation_dialog = true">Reset matches</a>
      <v-dialog v-model="reset_confirmation_dialog" width="40%">
        <v-card>
          <v-card-title>
            <h3>
              Are you sure that you want to reset the matches? All of the
              current groups are going to be erased.
            </h3>
          </v-card-title>
          <v-card-text>
            <v-card-actions class="text-center">
              <v-btn class="mx-auto" color="red" @click="reset_matches_click"
                >Reset</v-btn
              >
            </v-card-actions>
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
    <!-- Register Score Modal -->
    <v-dialog
      v-if="register_score_dialog"
      v-model="register_score_dialog"
      width="40%"
    >
      <v-card>
        <v-card-title>
          <h5>REGISTER SCORE</h5>
        </v-card-title>
        <v-card-text>
          <form v-on:submit.prevent="register_score()">
            <v-row>
              <v-col cols="12" md="3">
                <span class="champzFont mr-2 mt-1" style="float: right">{{
                  current_match.participant_1.name
                }}</span>
              </v-col>
              <v-col cols="12" md="2">
                <v-text-field
                  outlined
                  dense
                  type="number"
                  v-model="current_match.goals_participant_1"
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
                  v-model="current_match.goals_participant_2"
                  min="0"
                  required="required"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <span class="champzFont ml-3 mt-1" style="float: left">{{
                  current_match.participant_2.name
                }}</span>
              </v-col>
            </v-row>
            <v-card-actions>
              <v-btn
                type="button"
                color="red"
                @click="register_score_dialog = false"
                >Close</v-btn
              >
              <v-btn
                type="submit"
                color="green"
                :disabled="!current_match.goals_participant_2 || !current_match.goals_participant_1"
                :loading="register_score_loading"
                >Save changes</v-btn
              >
            </v-card-actions>
          </form>
        </v-card-text>
      </v-card>
    </v-dialog>
    <!-- End Register Score modal -->
  </v-container>
</template>

<style lang="scss" scoped>
// tr {
//   height: 35px !important;
// }
.champzFont {
  font-size: 15px;
  font-weight: 500;
  font-family: system-ui;
  vertical-align: inherit !important;
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
  height: 100%;
  overflow-y: auto;
}
</style>

<script>
import Service from "@/services/Service";
import GeneralServices from "@/services/GeneralServices";
export default {
  name: "Matches",

  data: () => ({
    service: new Service(),
    gs: new GeneralServices(),
    final: false,
    register_score_dialog: false,
    reset_confirmation_dialog: false,
    selected_group: {},
    table: [],
    current_match: {},
    current_group_index: 0,
    loading: true,
    group_loading: false,
    register_score_loading: false,
    replace: [false, false, false, false],
  }),
  async created() {
    await this.get_group_stage(false);
    this.loading = false;
  },
  methods: {
    async next_stage_click() {
      this.group_loading = true;
      this.current_group_index += 1;
      switch (this.current_group_index) {
        case 1:
          await this.get_wildcard(this.replace[this.current_group_index]);
          break;
        case 2:
          await this.get_semis(this.replace[this.current_group_index]);
          break;
        case 3:
          await this.get_final(this.replace[this.current_group_index]);
          break;
      }
      this.replace[this.current_group_index] = false;
      this.group_loading = false;
    },
    async previous_stage_click() {
      this.group_loading = true;
      this.current_group_index -= 1;
      switch (this.current_group_index) {
        case 0:
          await this.get_group_stage(false);
          break;
        case 1:
          await this.get_wildcard(false);
          break;
        case 2:
          await this.get_semis(false);
          break;
      }
      this.group_loading = false;
    },
    get_match: function (match) {
      this.current_match = JSON.parse(JSON.stringify(match));
      this.register_score_dialog = true;
    },
    register_score: async function () {
      this.register_score_loading = true;
      var match_index = this.selected_group.matches
        .map((x) => x.id)
        .indexOf(this.current_match.id);
      this.selected_group.matches = this.selected_group.matches
        .slice(0, match_index)
        .concat([this.current_match])
        .concat(
          this.selected_group.matches.slice(
            match_index + 1,
            this.selected_group.length
          )
        );

      // Setting the replace flag to true to update de matchups for the next stage
      if (this.current_group_index != 3) {
        this.replace[this.current_group_index + 1] = true;
      }

      var url = `/api/match/${this.current_match.id}`;
      await this.service
        .patchRequest(url, this.current_match)
        .then((response) => {})
        .catch((err) => {});

      if (this.current_group_index == 0) {
        await this.get_table(this.selected_group.id);
      }

      this.register_score_loading = false;
      this.register_score_dialog = false;
    },
    async reset_matches_click() {
      await this.get_group_stage(true);
      this.replace = [false, false, false, false];
      this.current_group_index = 0;
      this.reset_confirmation_dialog = false;
    },
    get_group_stage: async function (replace) {
      await this.service
        .postRequest(`/api/group-stage`, { replace: replace })
        .then((response) => {
          this.selected_group = response;
        })
        .catch((err) => {});
      if ((this.table.length == 0 || replace) && this.selected_group.id) {
        await this.get_table(this.selected_group.id);
      }
    },
    get_table: async function (id) {
      await this.service
        .getRequest(`/api/table/${id}`)
        .then((response) => {
          this.table = response;
        })
        .catch((err) => {});
    },
    get_wildcard: async function (replace) {
      await this.service
        .postRequest("/api/wildcards", { replace: replace })
        .then((response) => {
          this.selected_group = response;
        })
        .catch((err) => {});
    },
    get_semis: async function (replace) {
      await this.service
        .postRequest("/api/semis", { replace: replace })
        .then((response) => {
          this.selected_group = response;
          this.final = false;
        })
        .catch((err) => {});
    },
    get_final: async function (replace) {
      await this.service
        .postRequest("/api/final", { replace: replace })
        .then((response) => {
          this.selected_group = response;
          this.final = true;
        })
        .catch((err) => {});
    },
    generate_champz_file: async function () {
      await this.service
        .postRequest("/api/end-champz")
        .then((response) => {})
        .catch((err) => {});
    },
  },
  computed: {},
};
</script>
