import React, { useEffect } from "react";
import { Line } from "react-chartjs-2";
import { useParams } from "react-router";
import { getAuthenticatedUser } from "../api/account";
import { getUser } from "../api/user";

interface Props {}

export const Account: React.FC<Props> = (props: Props) => {
  const [hsData, setHsData] = React.useState<object | undefined>(undefined);
  const [bpmData, setBpmData] = React.useState<object | undefined>(undefined);
  const [username, setUsername] = React.useState<string>("");
  const [bio, setBio] = React.useState<string>("");

  const { id } = useParams<any>();

  useEffect(() => {
    const userInfoPromise = id ? getUser(id) : getAuthenticatedUser();

    userInfoPromise
      .then((repsonse: any) => {
        const userInfo = repsonse.data;
        setUsername(userInfo.username);
        setBio(userInfo.description);

        setHsData(
          generateDiagramData(
            userInfo.games.map((game: any) => game.score),
            "#D11149"
          )
        );
        setBpmData(
          generateDiagramData(
            userInfo.games.map((game: any) => game.bpm),
            "#6610F2"
          )
        );
      })
      .catch((error: any) => console.log(error));
  }, []);

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-lg-3">
          <div className="card">
            <h2 className="card-title">{username}</h2>
            <p>{bio}</p>
          </div>
        </div>
        <div className="col-lg-9">
          <div className="card">
            <h2 className="card-title">Highscores</h2>
            <Line data={hsData} options={chartOptions} />
          </div>
          <div className="card">
            <h2 className="card-title">Blocks per minute</h2>
            <Line data={bpmData} options={chartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
};

// Generate a data object for the chart
const generateDiagramData = (data: any[], color: string) => {
  return {
    labels: ["-", "-", "-", "-", "-", "-", "-"],
    datasets: [
      {
        label: "Highscores",
        data,
        fill: true,
        borderColor: color,
        tension: 0.1,
      },
    ],
  };
};

const chartOptions = {
  plugins: {
    title: {
      display: false,
    },
    legend: {
      display: false,
    },
  },
};
