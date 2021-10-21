import axios from "axios";
import { ENDPOINT } from "./endpoint";

export const getLobbies = () => {
  return axios.get(`${ENDPOINT}/gameserver/list`);
};

export const createLobby = (name: string) => {
  return axios.post(`${ENDPOINT}/gameserver/allocate`, {name: name});
};
