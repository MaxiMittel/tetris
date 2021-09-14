//import axios from "axios";

//const BASE_URL = "/";

export const getUser = (userID: number) => {
    return {
        username: "John452",
        description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Est nam ipsa consequatur laborum explicabo.",
        games: [
            {score: 1000, bpm: 4.56, date: 1631647493076},
            {score: 1005, bpm: 4.89, date: 1631647493076},
            {score: 980, bpm: 4.6, date: 1631647493076},
            {score: 1100, bpm: 3.2, date: 1631647493076},
            {score: 1090, bpm: 4.23, date: 1631647493076},
            {score: 1150, bpm: 4.54, date: 1631647493076},
            {score: 1200, bpm: 5.1, date: 1631647493076}
        ]
    }
};
