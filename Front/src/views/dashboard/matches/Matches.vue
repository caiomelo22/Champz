<template>
  <v-container v-if="!loading">
    <div>
      <v-card style="height: 100%">
        <v-toolbar color="primary" dark>
          <v-btn
            v-if="current_group_index"
            fab
            text
            large
            @click="
              current_group_index--;
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
          <v-col v-if="current_group_index == 0" cols="12" md="8">
            <v-row>
              <v-col cols="12" md="11">
                <div v-for="(table, index) in tables" :key="index">
                  <h4 class="text-center my-6">{{ groups[index].group }}</h4>
                  <table class="table table-striped ml-7">
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
                      <tr v-for="(participant, i) in table" :key="i">
                        <td class="champzFont">
                          <img
                            style="width: 30px"
                            :src="gs.get_team_image_path(participant[0].team.image_path)"
                          />
                          {{
                              participant[0].name.toUpperCase()
                          }}
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
                    <!-- </template> -->
                  </table>
                  <v-divider></v-divider>
                </div>
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
            <div
              v-for="group in get_dashboard_matches()"
              :key="group.id"
              class="mt-3"
            >
              <h5 class="text-center">{{ group.group }}</h5>
              <v-simple-table :class="current_group_index ? 'mx-8' : 'mr-0'">
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
                          match.goals_participant_1 == null &&
                          match.goals_participant_2 == null
                        "
                      >
                        {{
                          match.participant_1.name.toUpperCase()
                        }}

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
                            gs.get_team_image_path(match.participant_2.team.image_path)
                          "
                        />
                        {{
                          match.participant_2.name.toUpperCase()
                        }}
                      </td>
                      <td class="champzFont text-center" v-else>
                        {{
                          match.participant_1.name.toUpperCase()
                        }}
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
                        {{
                          match.participant_2.name.toUpperCase()
                        }}
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
              <v-btn class="mx-auto" color="red" @click="initialize_group()"
                >Reset</v-btn
              >
            </v-card-actions>
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
    <!-- Register Score Modal -->
    <v-dialog v-model="register_score_dialog" width="40%">
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
    loading: true,
    choice: false,
    final: false,
    register_score_dialog: false,
    reset_confirmation_dialog: false,
    participants: [],
    group_matches: [],
    groups: [],
    matches: [],
    table: [],
    tables: [],
    current_match: {},
    current_group_index: 0,
    current_group: {},
  }),
  mounted: function () {
    this.get_groups();
    this.get_participants();
    // this.initialize_group();
  },
  methods: {
    get_dashboard_matches() {
      if (this.current_group_index == 0) {
        return this.groups.filter((x) => x.group.includes("Group"));
      } else if (this.current_group_index == 1) {
        return this.groups.filter((x) => x.group.includes("Wildcard"));
      } else if (this.current_group_index == 2) {
        return this.groups.filter((x) => x.group.includes("Semi"));
      } else if (this.current_group_index == 3) {
        return this.groups.filter((x) => x.group.includes("Final"));
      }
    },
    next_stage_click() {
      if (this.current_group_index == 0) {
        this.knockout_stage_btn_click();
      } else if (!this.current_group_index == 0 && !this.final) {
        this.next_knockout_stage_btn_click();
      }
    },
    get_participants: function () {
      this.service
        .getRequest("/api/participant/")
        .then((response) => {
          this.participants = response;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
        });
    },
    get_match: function (match) {
      this.current_match = JSON.parse(JSON.stringify(match));
      this.register_score_dialog = true;
    },
    register_score: function () {
      var group_index = this.groups
        .map((x) => x.id)
        .indexOf(this.current_match.group);
      var match_index = this.groups[group_index].matches
        .map((x) => x.id)
        .indexOf(this.current_match.id);
      this.groups[group_index].matches[match_index] = this.current_match;
      var url = "/api/match/" + this.current_match.id + "/";
      this.register_score_dialog = false;
      this.service
        .patchRequest(url, this.current_match)
        .then((response) => {
          if (this.current_group_index == 0) {
            this.get_groups_table();
          }
        })
        .catch((err) => {});
    },
    get_groups: function () {
      this.loading = true;
      this.service
        .getRequest("/api/group/")
        .then((response) => {
          this.groups = response;
          if (this.groups.length == 0) {
            this.initialize_group();
          } else {
            this.groups.forEach((element) => {
              element.matches = [];
            });
            this.get_matches();
            this.get_groups_table();
          }
        })
        .catch((err) => {
          this.loading = false;
        });
    },
    get_groups_table: function () {
      this.service
        .getRequest("/api/tables/")
        .then((response) => {
          this.tables = response;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
        });
    },
    initialize_group: function () {
      this.loading = true;
      this.service
        .postRequest("/api/start-champz/")
        .then((response) => {
          this.get_groups();
          this.reset_confirmation_dialog = false;
        })
        .catch((err) => {
          this.loading = false;
        });
    },
    knockout_stage_btn_click: function () {
      if (this.groups.filter((x) => x.group.includes("Wildcard")).length > 1) {
        this.current_group_index += 1;
      } else {
        this.loading = true;
        this.generate_wildcard();
      }
    },
    get_group_title() {
      if (this.current_group_index == 0) {
        return "Group Stage";
      } else if (this.current_group_index == 1) {
        return "Wildcard";
      } else if (this.current_group_index == 2) {
        return "Semis";
      } else {
        return "Finals";
      }
    },
    next_knockout_stage_btn_click: function () {
      if (
        this.current_group_index == 1 &&
        this.groups.filter((x) => x.group.includes("Semi")).length == 0
      ) {
        this.generate_semis();
      } else if (
        this.current_group_index == 2 &&
        this.groups.filter((x) => x.group.includes("Final")).length == 0
      ) {
        this.generate_final();
      } else {
        this.current_group_index += 1;
      }
      if (this.current_group_index == 3) {
        this.final = true;
      }
    },
    generate_wildcard: function () {
      this.loading = true;
      this.service
        .postRequest("/api/generate_wildcards/")
        .then((response) => {
          this.current_group_index += 1;
          this.get_groups();
        })
        .catch((err) => {
          this.loading = false;
        });
    },
    generate_semis: function () {
      this.loading = true;
      this.service
        .postRequest("/api/generate_semis/")
        .then((response) => {
          this.current_group_index += 1;
          this.get_groups();
        })
        .catch((err) => {
          this.loading = false;
        });
    },
    generate_final: function () {
      this.loading = true;
      this.service
        .postRequest("/api/generate_final")
        .then((response) => {
          this.get_groups();
          this.current_group_index += 1;
          this.final = true;
        })
        .catch((err) => {
          this.loading = false;
        });
    },
    generate_champz_file: function () {
      this.loading = true;
      this.service
        .postRequest("/api/end_champz/")
        .then((response) => {
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
        });
    },
    match_to_group: function (match) {
      this.groups.forEach((element) => {
        if (match.group == element.id) {
          element.matches.push(match);
          return;
        }
      });
    },
    get_matches: function () {
      this.loading = true;
      this.service
        .getRequest("/api/match/")
        .then((response) => {
          this.matches = response;
          this.matches.forEach((element) => {
            this.match_to_group(element);
          });
        })
        .catch((err) => {
          this.loading = false;
        });
    },
  },
  computed: {},
};
</script>
