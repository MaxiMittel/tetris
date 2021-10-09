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

  return (
    <div className="App">
      <Navbar>
        <BrowserRouter>
          <Switch>
            <Route path="/signin">
              <SignIn onAuthenticated={() => setAuth(true)}/>
            </Route>
            <Route path="/signup">
              <SignUp onAuthenticated={() => setAuth(true)}/>
            </Route>
            <Authenticated authenticated={isAuth} onAuthenticated={() => setAuth(true)}>
              <Route path="/account" component={Account} />
              <Route path="/" component={Lobbies} exact/>
            </Authenticated>
          </Switch>
        </BrowserRouter>
      </Navbar>
    </div>
  );
}

export default App;
