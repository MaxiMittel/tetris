import axios from "axios";

const DIRECTORY_SERVICE = "http://127.0.0.1:7777/";
export var ENDPOINT = "";

export const requestEndpoint = () => {
  return new Promise((resolve, reject) => {
    if (ENDPOINT !== "") {
      resolve(ENDPOINT);
    } else {
      axios
        .get(`${DIRECTORY_SERVICE}/directory-service/getlb`)
        .then((response) => {
          // Get all available load balancers
          const loadBalancers = response.data.server.map((lb: any) => {
            return `http://${lb.ip}:${lb.port}`;
          });

          // Choose a random load balancer
          ENDPOINT =
            loadBalancers[Math.floor(Math.random() * loadBalancers.length)];

          resolve(ENDPOINT);
        })
        .catch((error) => {
          console.log(error);
          reject();
        });
    }
  });
};

export const getGameServers = () => {
  return new Promise((resolve, reject) => {
    axios
      .get(`${DIRECTORY_SERVICE}/directory-service/getgs`)
      .then((response) => {
        // Get all available load balancers
        const gameServers = response.data.server.map((gs: any) => {
          return {ip: gs.ip, port: gs.port};
        });

        resolve(gameServers);
      })
      .catch((error) => {
        console.log(error);
        reject();
      });
  });
}