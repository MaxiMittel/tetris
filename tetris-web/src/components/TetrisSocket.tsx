import React, { useEffect, useState } from "react";
import { randomBlock } from "../tetris/blocks";
import { Colors, PlayerEntry } from "../types";
import { Tetris } from "./Tetris";
import io from "socket.io-client";

const socket = io("ws://localhost:5000");
const room = "vally";
const username = "Maxi" + Math.floor(Math.random() * 100);
const id = "1" + Math.floor(Math.random() * 100);

interface Props {}

export const TetrisSocket: React.FC<Props> = (props: Props) => {
  let fielda = new Array<Colors[]>(20);

  for (var i = 0; i < fielda.length; i++) {
    fielda[i] = new Array<Colors>(10).fill(Colors.EMPTY);
  }

  const [player, setPlayer] = useState<PlayerEntry>({
    id: id,
    username: username,
    block: randomBlock(),
  });
  const [players, setPlayers] = useState<PlayerEntry[]>([]);
  const [field, setField] = useState(fielda);

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
  }, [players]);

  const onBlockFix = (newField: Colors[][]) => {
    setField(newField);
    setPlayer((player) => { player.block = randomBlock(); return player; });
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

  return (
    <div className="gameContainer">
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
