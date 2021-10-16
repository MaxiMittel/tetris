import React, { useEffect, useState } from "react";
import { randomBlock } from "../tetris/blocks";
import { ChatMessage, Colors, PlayerEntry } from "../types";
import { Tetris } from "./Tetris";
import io from "socket.io-client";
import { LobbyInfo } from "./LobbyInfo";

const room = "asdasd132s";
const username = "Maxi" + Math.floor(Math.random() * 100);
const id = "1" + Math.floor(Math.random() * 100);

const fieldSize = { x: 10, y: 20 };

interface Props {}

export const TetrisSocket: React.FC<Props> = (props: Props) => {
  let fielda = new Array<Colors[]>(fieldSize.y);

  for (var i = 0; i < fielda.length; i++) {
    fielda[i] = new Array<Colors>(fieldSize.x).fill(Colors.EMPTY);
  }

  const [player, setPlayer] = useState<PlayerEntry>({
    id: id,
    username: username,
    block: randomBlock(randInt(0, fieldSize.x - 3)),
    ready: false,
  });
  const [players, setPlayers] = useState<PlayerEntry[]>([]);
  const [field, setField] = useState(fielda);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [playerReady, setPlayerReady] = useState(false);
  const [gameRunning, setGameRunning] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [lobbyText, setLobbyText] = useState("Waiting for other players...");
  const [socket, setSocket] = useState<any>(null);

  useEffect(() => {
    const newSocket = io("ws://localhost:5000");
    setSocket(newSocket);
    return () => {
      newSocket.close();
      return;
    };
  }, [setSocket]);

  /**
   * Join the room
   */
  useEffect(() => {
    if (socket) {
      socket.emit("join", { room, username: username, id: id });
    }
  }, [socket]);

  /**
   * React to socket events
   */
  useEffect(() => {
    if (!socket) return;

    socket.on("disconnect", () => {
      console.log("disconnected");
    })

    // New player joins
    socket.on("onJoin", (response: any) => {
      setPlayers(response);
    });

    // New player joins
    socket.on("onLeave", (response: any) => {
      setPlayers(response);
    });

    // Player updates
    socket.on("onPlayerUpdate", (response: any) => {
      setPlayers(response);
    });

    // Field update
    socket.on("onFieldUpdate", (response: any) => {
      setField(response);
    });

    // Chat message
    socket.on("onChatMessage", (response: any) => {
      console.log("Message received");
      setChatMessages((messages) => [...messages, response.message]);
    });

    // Player ready
    socket.on("onPlayerReady", (response: any) => {
      setPlayers(response);
    });

    socket.on("onGameStart", (response: any) => {
      setGameRunning(true);
    });

    socket.on("onGameOver", (response: any) => {
      setLobbyText(`Game over! Score: ${response.score}`);
      setGameOver(true);
      setGameRunning(false);
    });
  }, [socket]);

  const onBlockFix = (newField: Colors[][]) => {
    setField(newField);
    setPlayer((player) => {
      player.block = randomBlock(randInt(0, fieldSize.x - 4));
      return player;
    });
    socket.emit("fieldUpdate", { room, field: newField });
  };

  const onPlayerMove = (newPlayer: PlayerEntry) => {
    setPlayer(newPlayer);
    socket.emit("playerUpdate", {
      room,
      id: id,
      block: newPlayer.block,
    });
  };

  const sendChatMessage = (message: ChatMessage) => {
    console.log("message");
    socket.emit("chatMessage", { room, msg: message });
  };

  const onReady = () => {
    setPlayerReady(true);
    socket.emit("playerReady", { room, id: id });
  };

  return (
    <div className="gameContainer">
      <LobbyInfo
        messages={chatMessages}
        onMessage={sendChatMessage}
        userId={id}
        players={players.map((p) => {
          return { username: p.username, id: p.id, ready: p.ready };
        })}
      />
      {gameRunning && (
        <Tetris
          field={field}
          player={player}
          players={players.filter((p) => p.id !== id)}
          onPlayerMove={onPlayerMove}
          onBlockFix={onBlockFix}
        ></Tetris>
      )}
      {!gameRunning && (
        <div className="waiting-container">
          <p className="waiting-text">{lobbyText}</p>
          {!playerReady && (
            <button className="btn btn-primary" onClick={onReady}>
              Ready
            </button>
          )}
          {gameOver && (
            <a href="/" ><button className="btn btn-primary" onClick={onReady}>
              Continue
            </button></a>
          )}
        </div>
      )}
    </div>
  );
};

//min,max (inclusive)
const randInt = (min: number, max: number) => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};
