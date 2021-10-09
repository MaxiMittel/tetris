import axios from "axios";

const BASE_URL = "http://10.0.1.3:9090/account";

export const signup = (username: string, password: string) => {
  return axios.post(`${BASE_URL}/signup`, {
    username,
    password,
  });
};

export const signin = (username: string, password: string) => {
  axios.post(`${BASE_URL}/signin`, {
    username,
    password,
  });
};

export const isAuthenticated = () => {
  return axios.get(`${BASE_URL}/isAuthenticated`,{
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
}