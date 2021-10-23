import axios from "axios";
import { requestEndpoint } from "./endpoint";

export const getLobbies = () => {
  return requestEndpoint().then((endpoint) => {
    return axios.get(`${endpoint}/sessions/list`);
  });
};

export const createLobby = (name: string) => {
  return requestEndpoint().then((endpoint) => {
    return axios.post(`${endpoint}/sessions/allocate`, { name: name });
  });
};

export const getLobby = (id: string) => {
  return requestEndpoint().then((endpoint) => {
    return axios.get(`${endpoint}/sessions/get`, { params: { id } });
  });
};

export const deleteLobby = (id: string, ip: string, port: number) => {
  return requestEndpoint().then((endpoint) => {
    return axios.post(`${endpoint}/sessions/delete`, { id, ip, port });
  });
};

export const migrateLobby = (id: string, name: string) => {
  return requestEndpoint().then((endpoint) => {
    return axios.post(`${endpoint}/sessions/migrate`, { id: id, name: name });
  });
};
