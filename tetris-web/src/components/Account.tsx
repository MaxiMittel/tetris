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
  const [highscore, setHighscore] = React.useState<number>(0);

  const { id } = useParams<any>();

  useEffect(() => {
    const userInfoPromise = id ? getUser(id) : getAuthenticatedUser();

    userInfoPromise
      .then((repsonse: any) => {
        const userInfo = repsonse.data;
        setUsername(userInfo.username);
        setHighscore(userInfo.highscore);        

        if (userInfo.stats.length > 0) {
          setHsData(
            generateDiagramData("Highscore",
              userInfo.stats.map((game: any) => game.score),
              "#D11149"
            )
          );
          setBpmData(
            generateDiagramData("Blocks per minute",
              userInfo.stats.map((game: any) => game.bpm),
              "#6610F2"
            )
          );
        }
      })
      .catch((error: any) => console.log(error));
  }, [id]);

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-lg-3">
          <div className="card">
            <h2 className="card-title">{username}</h2>
            <p>Highscore: {highscore}</p>
          </div>
        </div>
        <div className="col-lg-9">
          <div className="card">
            <h2 className="card-title">Highscores</h2>
            {hsData && <Line data={hsData} options={chartOptions} />}
            {!hsData && <p>No highscores</p>}
          </div>
          <div className="card">
            <h2 className="card-title">Blocks per minute</h2>
            {bpmData && <Line data={bpmData} options={chartOptions} />}
            {!bpmData && <p>No bpm data</p>}
          </div>
        </div>
      </div>
    </div>
  );
};

// Generate a data object for the chart
const generateDiagramData = (label: string, data: any[], color: string) => {
  if (data.length === 0) {
    return undefined;
  }

  return {
    labels: ["-", "-", "-", "-", "-", "-", "-"],
    datasets: [
      {
        label,
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
