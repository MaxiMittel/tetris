import axios from "axios";
import { ENDPOINT } from "./endpoint";

export const getUser = (userID: number) => {
    return axios.get(`${ENDPOINT}/api/user/getbyid`,{
        headers: {
          Authorization: `Bearer ${localStorage.getItem("auth")}`,
        },
        params: {
            id: userID
        }
      });
};
