import React, { useEffect, useState } from "react";
import { randomBlock } from "../tetris/blocks";
import { Block, Colors } from "../types";
import { Tetris } from "./Tetris";
import io from "socket.io-client";

const socket = io("ws://localhost:5000");
const room = "room1";
const username = "Maxi" + Math.floor(Math.random() * 100);
const id = "1" + Math.floor(Math.random() * 100);

interface Props {}

export const TetrisSocket: React.FC<Props> = (props: Props) => {
  let fielda = new Array<Colors[]>(20);

  for (var i = 0; i < fielda.length; i++) {
    fielda[i] = new Array<Colors>(10).fill(Colors.EMPTY);
  }

  type PlayerEntry = {
    id: string;
    username: string;
    block: Block;
  };

  const [player, setPlayer] = useState<Block>(randomBlock());
  const [players, setPlayers] = useState<PlayerEntry[]>([]);
  const [field, setField] = useState(fielda);

  /**
   * Join the room
   */
  useEffect(() => {
    socket.emit("join", { room: room, username: username, id: id });
  }, [socket]);

  /**
   * React to socket events
   */
  useEffect(() => {
    // New player joins
    socket.on("onJoin", (response) => {
      //Insert new player
      response.players.forEach((player: any) => {
        if (!players.some((p) => p.id === player.id)) {
          player["block"] = undefined;
          setPlayers((players) => [...players, player]);
        }
      });
    });

    // Player updates
    socket.on("onPlayerUpdate", (response) => {
      setPlayers((players) =>
        players.map((p) => {
          if (p.id === response.id) {
            p.block = response.block;
          }
          return p;
        })
      );
    });

    // Field update
    socket.on("onFieldUpdate", (response) => {      
      setField(response.field);
    });
  }, [socket, players]);

  /**
   * Send any player update
   */
  useEffect(() => {
    socket.emit("onPlayerUpdate", {
      room: room,
      id: id,
      block: player,
    });
  }, [player]);

  const onBlockFix = (newField: Colors[][]) => {
    setField(newField);
    setPlayer(randomBlock());
    socket.emit("fieldUpdate", { room: room, field: newField });
  };

  return (
    <div className="gameContainer">
      <Tetris
        field={field}
        player={player}
        onPlayerMove={(newPlayer: Block) => setPlayer(newPlayer)}
        onBlockFix={onBlockFix}
      ></Tetris>
    </div>
  );
};
