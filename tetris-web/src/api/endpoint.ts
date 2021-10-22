import axios from "axios";

const DIRECTORY_SERVICE = "http://localhost:7777"; //TODO: Replace with .env
export var ENDPOINT = "";

export const requestEndpoint = () => {
    return new Promise((resolve, reject) => {
        axios.get(`${DIRECTORY_SERVICE}/directory-service/getlb`).then(response => {            

            // Get all available load balancers
            const loadBalancers = response.data.server.map((lb: any) => {return `http://${lb.ip}:${lb.port}`;});

            // Choose a random load balancer
            ENDPOINT = loadBalancers[Math.floor(Math.random() * loadBalancers.length)];            

            resolve(true);

        }).catch(error => {
            console.log(error);
            reject();
        });
    });
}