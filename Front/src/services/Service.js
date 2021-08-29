import ApiClient from "./ApiClient";
const { stringifyUrl } = require("query-string");

export default class Service {
  constructor() {
    this.apiClient = new ApiClient();
  }

  async postRequest(route, data) {
    const resp = await this.apiClient.post(route, data);
    return resp;
  }

  async putRequest(route, data) {
    const resp = await this.apiClient.put(route, data);
    return resp;
  }

  async patchRequest(route, data) {
    const resp = await this.apiClient.patch(route, data);
    return resp;
  }

  async deleteRequest(route, data) {
    const resp = await this.apiClient.delete(route, data);
    return resp;
  }

  async getRequest(route) {
    const resp = await this.apiClient.get(route);
    return resp;
  }

  async getTestUrl() {
    var query = {};
    const requestURL = stringifyUrl({
      url: `User`,
      query: query,
    });
    const resp = await this.apiClient.get(requestURL);
    return resp;
  }
}
