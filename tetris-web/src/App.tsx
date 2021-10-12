import { useEffect, useState } from "react";
import { Navbar } from "./components/Navbar";
import "./index.css";
import "halfmoon/css/halfmoon-variables.min.css";
import { SignIn } from "./components/SignIn";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import { Lobbies } from "./components/Lobbies";
import { SignUp } from "./components/SignUp";
import { Account } from "./components/Account";
import { Authenticated } from "./components/Authenticated";
import { isAuthenticated } from "./api/account";
import { TetrisSocket } from "./components/TetrisSocket";
import { Search } from "./components/Search";
import { Chat } from "./components/Chat";
import { LobbyInfo } from "./components/LobbyInfo";
import { ChatMessage } from "./types";

function App() {
  const halfmoon = require("halfmoon");

  useEffect(() => {
    halfmoon.onDOMContentLoaded();
  }, [halfmoon]);

  const [isAuth, setAuth] = useState(true);

  useEffect(() => {
    isAuthenticated()
      .then((response) => setAuth(response.data.message === "Success"))
      .catch(() => setAuth(false));
  }, []);

  const messages = [
    { id: "a", message: "Hi" },
    { id: "b", message: "Hello" },
    { id: "c", message: "How are you?" },
    { id: "a", message: "I'm fine" },
    { id: "e", message: "How are you?" },
    { id: "a", message: "I'm fine" },
    { id: "a", message: "How are you?" },
    { id: "h", message: "I'm fine" },
    { id: "i", message: "How are you?" },
    { id: "a", message: "I'm fine" },
    { id: "k", message: "How are you?" },
    { id: "a", message: "I'm fine" },
  ];

  const players = [
    { id: "a", username: "John" },
    { id: "a", username: "John" },
    { id: "a", username: "John" },
    { id: "a", username: "John" },
    { id: "a", username: "John" },
  ];

  return (
    <div className="App">
      <Navbar authenticated={isAuth} buttonText={isAuth? "Account" : "Sign in"}>
        <BrowserRouter>
          <Switch>
            <Route path="/signin">
              <SignIn onAuthenticated={() => setAuth(true)}/>
            </Route>
            <Route path="/signup">
              <SignUp onAuthenticated={() => setAuth(true)}/>
            </Route>
            <Route path="/tetris" component={TetrisSocket} />
            <Authenticated authenticated={isAuth} onAuthenticated={() => setAuth(true)}>
              <Route path="/account" component={Account} />
              <Route path="/user/:id" component={Account} />
              <Route path="/" component={Lobbies} exact/>
              <Route path="/search" component={Search} />
            </Authenticated>
            
          </Switch>
        </BrowserRouter>
      </Navbar>
    </div>
  );
}

export default App;
