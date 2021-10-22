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
import { requestEndpoint } from "./api/endpoint";

function App() {
  const halfmoon = require("halfmoon");

  useEffect(() => {
    halfmoon.onDOMContentLoaded();
  }, [halfmoon]);

  const [isAuth, setAuth] = useState(true);

  useEffect(() => {
    requestEndpoint().then(() => {
      isAuthenticated()
        .then((response) => setAuth(response.data.message === "Success"))
        .catch(() => setAuth(false));
    }).catch(() => setAuth(false));
  }, []);

  return (
    <div className="App">
      <Navbar
        authenticated={isAuth}
        buttonText={isAuth ? "Account" : "Sign in"}
      >
        <BrowserRouter>
          <Switch>
            <Route path="/signin">
              <SignIn onAuthenticated={() => setAuth(true)} />
            </Route>
            <Route path="/signup">
              <SignUp onAuthenticated={() => setAuth(true)} />
            </Route>
            <Authenticated
              authenticated={isAuth}
              onAuthenticated={() => setAuth(true)}
            >
              <Route path="/account" component={Account} />
              <Route path="/user/:id" component={Account} />
              <Route path="/lobby/:room" component={TetrisSocket} />
              <Route path="/" component={Lobbies} exact />
              <Route path="/search" component={Search} />
            </Authenticated>
          </Switch>
        </BrowserRouter>
      </Navbar>
    </div>
  );
}

export default App;
