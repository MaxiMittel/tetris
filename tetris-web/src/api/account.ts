import axios from "axios";
import { ENDPOINT } from "./endpoint";

export const signup = (username: string, password: string) => {
  return axios.post(`${ENDPOINT}/api/account/signup`, {
    username,
    password,
  });
};

export const signin = (username: string, password: string) => {
  axios.post(`${ENDPOINT}/api/account/signin`, {
    username,
    password,
  });
};

export const isAuthenticated = () => {
  return axios.get(`${ENDPOINT}/api/account/isAuthenticated`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("auth")}`,
    },
  });
};

export const getAuthenticatedUser = () => {
  return axios.get(`${ENDPOINT}/api/user/get`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("auth")}`,
    },
  });
};
