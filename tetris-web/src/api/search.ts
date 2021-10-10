import axios from "axios";

const BASE_URL = "http://10.0.1.3:9090/user";

export const search = (query: string) => {
    return axios.get(`${BASE_URL}/search`,{
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      params: {
          q: query
        }
    });
  }