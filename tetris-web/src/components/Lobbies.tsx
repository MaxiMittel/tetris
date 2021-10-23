import React, { useEffect } from "react";
import { createLobby, getLobbies } from "../api/lobby";
import { Lobby } from "../types";

interface Props {}

export const Lobbies: React.FC<Props> = (props: Props) => {
  const [lobbyName, setLobbyName] = React.useState("");
  const [lobbies, setLobbies] = React.useState<Lobby[]>([]);

  useEffect(() => {
    getLobbies().then((response) => {
      setLobbies(response.data.sessions);
    });
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      getLobbies().then((response) => {
        setLobbies(response.data.sessions);
      });
    }, 1000);

    return () => { clearInterval(interval); };
  }, []);

  const onNewLobby = (e: any) => {
    e.preventDefault();
    createLobby(lobbyName).then((response) => {
      window.location.href = `/lobby/${response.data.id}`;
    });
  };

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="w-400 card">
          <div className="card-top">
            <h2 className="card-title">Join</h2>
          </div>

          <div className="lobby-scroll">
            {lobbies.map((lobby: Lobby, index: number) => (
              <LobbyItem
                players={lobby.players}
                lobbyName={lobby.name}
                code={lobby.id}
                key={"lobby_item_" + index}
              />
            ))}
          </div>
        </div>
        <div>
          <div className="w-400 card">
            <h2 className="card-title">Create</h2>

            <form onSubmit={onNewLobby} className="mw-full">
              <div className={"form-group"}>
                <label htmlFor="lobbyName" className="required">
                  Lobby name
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="lobbyName"
                  placeholder="e.g. Cool lobby"
                  required
                  value={lobbyName}
                  onChange={(e) => setLobbyName(e.target.value)}
                />
              </div>
              <div className="form-group">
                <input
                  className="btn btn-primary btn-block"
                  type="submit"
                  value="Create new"
                />
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

interface LobbyItemProps {
  lobbyName: string;
  players: number;
  code: string;
}

const LobbyItem: React.FC<LobbyItemProps> = (props: LobbyItemProps) => {
  return (
    <div className="lobby-item">
      <div className="lobby-item-text">
        <h2 className="lobby-item-heading">{props.lobbyName}</h2>
      </div>
      <a href={`/lobby/${props.code}`}>
        <button className="btn btn-primary">Join</button>
      </a>
    </div>
  );
};
