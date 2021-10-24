import axios from "axios";
import { SocketAddress } from "../types";

const pingServer = (server: SocketAddress) => {
  return new Promise((resolve, reject) => {
    let start = Date.now();
    axios
      .get(`http://${server.ip}:${server.port}/ping`)
      .then(() => {
        resolve({ ...server, ping: Math.floor((Date.now() - start) / 10) });
      })
      .catch((err) => reject(err));
  });
};

const pingAllServers = (servers: SocketAddress[]) => {
  return Promise.all(servers.map((server) => pingServer(server)));
};

export const getBestServer = (
  servers: SocketAddress[],
  exclude?: SocketAddress
) => {
  return pingAllServers(servers).then((servers) => {
    //Get all servers with a ping less than 100ms
    let acceptableServers = servers
      .sort((a: any, b: any) => a!.ping - b!.ping)
      .filter((server: any) => server.ping && server.ping < 100);

    if (exclude) {
      acceptableServers = acceptableServers.filter(
        (server: any) =>
          server.ip !== exclude.ip && server.port !== exclude.port
      );
    }

    //Return random acceptable server
    return acceptableServers[
      Math.floor(Math.random() * acceptableServers.length)
    ];
  });
};
