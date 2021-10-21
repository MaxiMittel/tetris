import axios from "axios";
import { ENDPOINT } from "./endpoint";

export const search = (query: string) => {
    return axios.get(`${ENDPOINT}/api/search`,{
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth")}`,
      },
      params: {
          query
        }
    });
  }