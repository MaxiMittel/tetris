import React, { useEffect, useState } from "react";
import { randomBlock } from "../tetris/blocks";
import { ChatMessage, Colors, PlayerEntry } from "../types";
import { Tetris } from "./Tetris";
import io from "socket.io-client";
import { LobbyInfo } from "./LobbyInfo";
import { useParams } from "react-router";
import { deleteLobby, getLobby, migrateLobby } from "../api/lobby";

const fieldSize = { x: 30, y: 20 };

interface Props {
  username: string;
  id: string;
}

export const TetrisSocket: React.FC<Props> = (props: Props) => {
  const { username, id } = props;
  const { room } = useParams<any>();

  const initPlayer = {
    id: id,
    username: username,
    block: randomBlock(randInt(0, fieldSize.x - 3)),
    ready: false,
  };

  const [player, setPlayer] = useState<PlayerEntry>(initPlayer);
  const [players, setPlayers] = useState<PlayerEntry[]>([]);
  const [field, setField] = useState(
    generateEmptyField(fieldSize.x, fieldSize.y)
  );
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [playerReady, setPlayerReady] = useState(false);
  const [gameRunning, setGameRunning] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [lobbyText, setLobbyText] = useState("Waiting for other players...");
  const [socketAddress, setSocketAddress] =
    useState<{ ip: string; port: number }>();
  const [socket, setSocket] = useState<any>(null);

  useEffect(() => {
    //Get the lobbys assigned game-server
    getLobby(room).then((response) => {
      setSocketAddress({ ip: response.data.ip, port: response.data.port });
    });
  }, [room]);

  useEffect(() => {
    let newSocket: any;

    if (socketAddress) {
      newSocket = io(`ws://${socketAddress.ip}:${socketAddress.port}`);
      setSocket(newSocket);
    }

    return () => {
      newSocket.close();
    };
  }, [socketAddress]);

  /**
   * Join the room
   */
  useEffect(() => {
    if (socket) {
      socket.emit("join", { room, username: username, id: id });
    }
  }, [socket, username, id, room]);

  useEffect(() => {
    if (socket) {
      socket.on("connect", () => {
        if (players.length !== 0) {
          socket.emit("migrate", { room, field, players });
        }
      });
    }
  }, [socket, players, field, room]);

  /**
   * React to socket events
   */
  useEffect(() => {
    if (!socket) return;

    socket.on("disconnect", () => {
      // All players will send a migrate event when they disconnect with a random delay
      setTimeout(() => {
        if (socketAddress) {
          deleteLobby(room, socketAddress.ip, socketAddress.port).then(() => {
            migrateLobby(room, "migrated-lobby").then((response) => {
              setSocketAddress({
                ip: response.data.ip,
                port: response.data.port,
              });
            });
          });
        }
      }, Math.random() * 3000);
    });

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
  }, [socket, room, socketAddress]);

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
            <a href="/">
              <button className="btn btn-primary" onClick={onReady}>
                Continue
              </button>
            </a>
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

const generateEmptyField = (width: number, height: number) => {
  let f = new Array<Colors[]>(fieldSize.y);

  for (var i = 0; i < f.length; i++) {
    f[i] = new Array<Colors>(fieldSize.x).fill(Colors.EMPTY);
  }

  return f;
};
