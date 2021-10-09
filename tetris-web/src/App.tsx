import { useEffect } from "react";
import { Navbar } from "./components/Navbar";
import "./index.css";
import "halfmoon/css/halfmoon-variables.min.css";
import { SignIn } from "./components/SignIn";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import { Lobbies } from "./components/Lobbies";
import { SignUp } from "./components/SignUp";
import { Account } from "./components/Account";

function App() {
  const halfmoon = require("halfmoon");

  useEffect(() => {
    halfmoon.onDOMContentLoaded();
  }, [halfmoon]);

  return (
    <div className="App">
      <Navbar>
        <BrowserRouter>
          <Switch>
            <Route path="/signin" component={SignIn} />
            <Route path="/signup" component={SignUp} />
            <Route path="/account" component={Account} />
            <Route path="/" component={Lobbies} />
          </Switch>
        </BrowserRouter>
      </Navbar>
    </div>
  );
}

export default App;
