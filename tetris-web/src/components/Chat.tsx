import React, { useState } from "react";
import { ChatMessage } from "../types";

interface Props {
  messages: ChatMessage[];
  userId: string;
  onMessage: (message: ChatMessage) => void;
}

export const Chat: React.FC<Props> = (props: Props) => {
  const [msg, setMsg] = useState("");

  const sendMessage = () => {
    if (msg.length > 0) {
      props.onMessage({
        id: props.userId,
        message: msg,
      });
      setMsg("");
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-message-container">
        {props.messages.map((message, index) => (
          <div
            key={index}
            className={message.id === props.userId ? "chat-right" : "chat-left"}
          >
            <div className="chat-message">{message.message}</div>
          </div>
        ))}
      </div>
      <form
        onSubmit={(e: any) => {
          e.preventDefault();
          sendMessage();
        }}
      >
        <div className="input-group">
          <input
            type="text"
            className="form-control"
            placeholder="Message..."
            value={msg}
            onChange={(e) => setMsg(e.target.value)}
          />
          <div className="input-group-append">
            <button
              className="btn btn-primary"
              type="submit"
              onClick={sendMessage}
            >
              Send
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};
