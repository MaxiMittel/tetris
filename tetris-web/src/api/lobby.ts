import axios from "axios";
import { SocketAddress } from "../types";
import { getGameServers, requestEndpoint } from "./endpoint";
import { getBestServer } from "./ping";

export const getLobbies = () => {
  return requestEndpoint().then((endpoint) => {
    return axios.get(`${endpoint}/sessions/list`);
  });
};

export const createLobby = (name: string) => {
  return requestEndpoint().then((endpoint) => {
    getGameServers().then((servers) => {
      getBestServer(servers as SocketAddress[]).then((server) => {
        return axios.post(`${endpoint}/sessions/allocate`, { name, server });
      });
    });
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
    getGameServers().then((servers) => {
      getBestServer(servers as SocketAddress[]).then((server) => {
        return axios.post(`${endpoint}/sessions/migrate`, { id, name, server });
      });
    });
  });
};
