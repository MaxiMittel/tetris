import React, { useEffect, useState } from "react";
import { randomBlock } from "../tetris/blocks";
import { ChatMessage, Colors, PlayerEntry } from "../types";
import { Tetris } from "./Tetris";
import io from "socket.io-client";
import { LobbyInfo } from "./LobbyInfo";

const socket = io("ws://10.0.1.3:5000");
const room = "vally";
const username = "Maxi" + Math.floor(Math.random() * 100);
const id = "1" + Math.floor(Math.random() * 100);

const fieldSize = {x: 40, y: 20};

interface Props {}

export const TetrisSocket: React.FC<Props> = (props: Props) => {
  let fielda = new Array<Colors[]>(fieldSize.y);

  for (var i = 0; i < fielda.length; i++) {
    fielda[i] = new Array<Colors>(fieldSize.x).fill(Colors.EMPTY);
  }

  const [player, setPlayer] = useState<PlayerEntry>({
    id: id,
    username: username,
    block: randomBlock(Math.floor(Math.random() * fieldSize.x-2) + 2),
  });
  const [players, setPlayers] = useState<PlayerEntry[]>([]);
  const [field, setField] = useState(fielda);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);

  /**
   * Join the room
   */
  useEffect(() => {
    socket.emit("join", { room: room, username: username, id: id });
  }, []);

  /**
   * React to socket events
   */
  useEffect(() => {
    // New player joins
    socket.on("onJoin", (response) => {
      //Insert new player
      response.players.forEach((player: any) => {
        if (!players.some((p) => p.id === player.id)) {
          setPlayers((players) => [...players, player]);
        }
      });
    });

    // Player updates
    socket.on("onPlayerUpdate", (response) => {
      console.log("update");
      if (response.id !== id) {
        setPlayers((players) => {
          let player = players.find((p) => p.id === response.id);
          if (player) {
            player.block = response.block;
          }
          return players;
        });
      }
    });

    // Field update
    socket.on("onFieldUpdate", (response) => {
      setField(response.field);
    });

    // Chat message
    socket.on("onChatMessage", (response) => {
      setChatMessages((messages) => [...messages, response.message]);
    });

  }, [players]);

  const onBlockFix = (newField: Colors[][]) => {
    setField(newField);
    setPlayer((player) => {
      player.block = randomBlock(Math.floor(Math.random() * fieldSize.x-2) + 2);
      return player;
    });
    socket.emit("fieldUpdate", { room: room, field: newField });
  };

  const onPlayerMove = (newPlayer: PlayerEntry) => {
    setPlayer(newPlayer);
    socket.emit("playerUpdate", {
      room: room,
      id: id,
      block: newPlayer.block,
      time: Date.now(),
    });
  };

  const sendChatMessage = (message: ChatMessage) => {
    socket.emit("chatMessage", { room: room, msg: message });
  };

  return (
    <div className="gameContainer">
      <LobbyInfo
        players={players.map((p) => {
          return { username: p.username, id: p.id };
        })}
        userId={id}
        messages={chatMessages}
        onMessage={sendChatMessage}
      ></LobbyInfo>
      <Tetris
        field={field}
        player={player}
        players={players}
        onPlayerMove={onPlayerMove}
        onBlockFix={onBlockFix}
      ></Tetris>
    </div>
  );
};
