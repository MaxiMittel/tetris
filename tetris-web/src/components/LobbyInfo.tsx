import React from "react";
import { ChatMessage } from "../types";
import { Chat } from "./Chat";

interface Props {
  messages: ChatMessage[];
  userId: string;
  onMessage: (message: ChatMessage) => void;
  players: { username: string; id: string, ready: boolean }[];
}

export const LobbyInfo: React.FC<Props> = (props: Props) => {
  const [tab, setTab] = React.useState<"players" | "chat">("players");  

  return (
    <div className="w-300 card">
      <div className="tab-header">
        <span
          className={tab === "players" ? "tab-item-selected" : "tab-item"}
          onClick={() => setTab("players")}
        >
          Players
        </span>
        <span
          className={tab === "chat" ? "tab-item-selected" : "tab-item"}
          onClick={() => setTab("chat")}
        >
          Chat
        </span>
      </div>
      {tab === "players" && (
        <div>
          {props.players.map((player, index) => (
            <div className="player-item" key={index}>
              <span>{player.username}</span>
                <span className={player.ready? "player-item-ready" : ""}/>
              </div>
          ))}
        </div>
      )}
      {tab === "chat" && (
        <Chat
          messages={props.messages}
          userId={props.userId}
          onMessage={props.onMessage}
        />
      )}
    </div>
  );
};
