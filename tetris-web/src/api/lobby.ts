//import axios from "axios";

//const BASE_URL = "/";

export const getLobbies = (query: string) => {
  console.log("SEARCH LOBBY", query);
  return [
    { name: "Lobibi", players: 3, code: "9jiodsmf" },
    { name: "Lobbit", players: 4, code: "9jiodsmf" },
    { name: "Lob 2", players: 7, code: "9jiodsmf" },
    { name: "Lob 3", players: 2, code: "9jiodsmf" },
    { name: "Lob 4", players: 1, code: "9jiodsmf" },
  ];
};

export const createLobby = (name: string) => {
  console.log("CREATE NEW LOBBY", name);
};
