import axios from "axios";
import { ENDPOINT } from "./endpoint";

export const getLobbies = () => {
  return axios.get(`${ENDPOINT}/gameserver/list`);
};

export const createLobby = (name: string) => {
  return axios.post(`${ENDPOINT}/gameserver/allocate`, { name: name });
};

export const getLobby = (id: string) => {
  return axios.get(`${ENDPOINT}/gameserver/get`, { params: { id } });
};

export const deleteLobby = (id: string, ip: string, port: number) => {
  return axios.post(`${ENDPOINT}/gameserver/delete`, { id, ip, port });
};

export const migrateLobby = (id: string, name: string) => {
  return axios.post(`${ENDPOINT}/gameserver/migrate`, { id: id, name: name });
};
