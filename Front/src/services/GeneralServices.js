import ApiClient from "./ApiClient";
import Vue from "vue";
const { stringifyUrl } = require("query-string");

export default class Service {
  constructor() {
    this.apiClient = new ApiClient();
  }

  async getPlayerImageLink(link) {
    var index = link.indexOf('Player');
    return `http://127.0.0.1:8000/wwwroot/${link.slice(index, link.length)}`
  }
  async getNationImageLink(link) {
    var index = link.indexOf('Nation');
    return `http://localhost:8000/wwwroot/${link.slice(index, link.length)}`
  }
  async getTeamImageLink(link) {
    var index = link.indexOf('Team');
    return `http://localhost:8000/wwwroot/${link.slice(index, link.length)}`
  }
}