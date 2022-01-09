import ApiClient from "./ApiClient";
import Vue from "vue";
const { stringifyUrl } = require("query-string");

export default class Service {
  constructor() {
    this.apiClient = new ApiClient();
  }

  getPlayerImageLink(link) {
    var index = link.indexOf('Player');
    return `http://127.0.0.1:8000/wwwroot/${link.slice(index, link.length)}`
  }
  getNationImageLink(link) {
    var index = link.indexOf('Nation');
    return `http://localhost:8000/wwwroot/${link.slice(index, link.length)}`
  }
  getTeamImageLink(link) {
    var index = link.indexOf('Team');
    return `http://localhost:8000/wwwroot/${link.slice(index, link.length)}`
  }
}