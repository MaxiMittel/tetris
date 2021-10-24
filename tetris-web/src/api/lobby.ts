import axios from "axios";
import { SocketAddress } from "../types";
import { getGameServers, requestEndpoint } from "./endpoint";
import { getBestServer } from "./ping";

export const getLobbies = () => {
  return requestEndpoint().then((endpoint) => {
    return axios.get(`${endpoint}/sessions/list`);
  });
};

export const createLobby = (name: string) => {
  return new Promise((resolve, reject) => {
    requestEndpoint().then((endpoint) => {
      getGameServers()
        .then((servers) => {
          getBestServer(servers as SocketAddress[])
            .then((server) => {
              axios
                .post(`${endpoint}/sessions/allocate`, { name, server })
                .then((res) => resolve(res))
                .catch((err) => reject(err));
            })
            .catch((err) => reject(err));
        })
        .catch((err) => reject(err));
    });
  });
};

export const getLobby = (id: string) => {
  return requestEndpoint().then((endpoint) => {
    return axios.get(`${endpoint}/sessions/get`, { params: { id } });
  });
};

export const deleteLobby = (id: string, ip: string, port: number) => {
  return requestEndpoint().then((endpoint) => {
    return axios.post(`${endpoint}/sessions/delete`, { id, ip, port });
  });
};

export const migrateLobby = (id: string, old: SocketAddress, name: string) => {
  return requestEndpoint().then((endpoint) => {
    return new Promise((resolve, reject) => {
      getGameServers()
        .then((servers) => {
          getBestServer(servers as SocketAddress[], old)
            .then((server) => {
              axios
                .post(`${endpoint}/sessions/migrate`, {
                  id,
                  name,
                  old,
                  server,
                })
                .then((res) => resolve(res))
                .catch((err) => reject(err));
            })
            .catch((err) => reject(err));
        })
        .catch((err) => reject(err));
    });
  });
};
