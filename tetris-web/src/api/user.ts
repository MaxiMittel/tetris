import axios from "axios";
import { requestEndpoint } from "./endpoint";

export const getUser = (userID: number) => {
  return requestEndpoint().then((endpoint) => {
    return axios.get(`${endpoint}/api/user/getbyid`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("auth")}`,
      },
      params: {
        id: userID,
      },
    });
  });
};
