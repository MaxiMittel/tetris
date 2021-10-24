import axios from "axios";
import { requestEndpoint } from "./endpoint";

export const signup = (username: string, password: string) => {
  return requestEndpoint().then((endpoint) => {
    return axios.post(`${endpoint}/api/account/signup`, {
      username,
      password,
    });
  });
};

export const signin = (username: string, password: string) => {
  return requestEndpoint().then((endpoint) => {
    return axios.post(`${endpoint}/api/account/signin`, {
      username,
      password,
    });
  });
};

export const isAuthenticated = () => {
  return requestEndpoint().then((endpoint) => {
    return axios.get(`${endpoint}/api/account/isAuthenticated`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth")}`,
      },
    });
  });
};

export const getAuthenticatedUser = () => {
  return requestEndpoint().then((endpoint) => {
    return axios.get(`${endpoint}/api/user/get`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth")}`,
      },
    });
  });
};

export const updateUserStats = (gamescore: any) => {
  return requestEndpoint().then((endpoint) => {
    return axios.post(`${endpoint}/api/user/updateStats`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth")}`,
      },
      data: {
        gamescore
      }
    });
  });
}