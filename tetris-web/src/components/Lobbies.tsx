import React, { useEffect } from "react";
import { createLobby, getLobbies } from "../api/lobby";
import { Lobby } from "../types";

interface Props {}

export const Lobbies: React.FC<Props> = (props: Props) => {
  const [search, setSearch] = React.useState("");
  const [lobbyName, setLobbyName] = React.useState("");
  const [lobbies, setLobbies] = React.useState<Lobby[]>([]);

  useEffect(() => {
    const lobbyData = getLobbies(search);
    setLobbies(lobbyData);
  }, [search]);

  const onNewLobby = (e: any) => {
    e.preventDefault();
    createLobby(lobbyName);
  };

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="w-400 card">
          <div className="card-top">
            <h2 className="card-title">Join</h2>
            <input
              type="text"
              className="form-control w-200"
              placeholder="Search..."
              value={search}
              onChange={(e: any) => setSearch(e.target.value)}
            />
          </div>

          <div className="lobby-scroll">
            {lobbies.map((lobby: Lobby, index: number) => (
              <LobbyItem
                players={lobby.players}
                lobbyName={lobby.name}
                code={lobby.code}
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
        <p className="lobby-item-players">{props.players}/8 Players</p>
      </div>
      <button className="btn btn-primary">Join</button>
    </div>
  );
};
