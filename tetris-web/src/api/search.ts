import axios from "axios";
import { requestEndpoint } from "./endpoint";

export const search = (query: string) => {
  return requestEndpoint().then((endpoint) => {
    return axios.get(`${endpoint}/api/user/search`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth")}`,
      },
      params: {
        query,
      },
    });
  });
};
