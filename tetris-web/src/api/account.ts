import axios from "axios";

const BASE_URL = "/";

export const signup = (username: string, password: string) => {
  return axios.post(`${BASE_URL}/signup`, {
    username,
    password,
  });
};

export const signin = (username: string, password: string) => {
  return axios.post(`${BASE_URL}/signin`, {
    username,
    password,
  });
};
