import React, { useEffect } from "react";
import { Navbar } from "./components/Navbar";
import "./index.css";
import "halfmoon/css/halfmoon-variables.min.css";
import { Lobbies } from "./components/Lobbies";

function App() {
  const halfmoon = require("halfmoon");

  useEffect(() => {
    halfmoon.onDOMContentLoaded();
  }, [halfmoon]);

  return (
    <div className="App">
      <Navbar>
        <Lobbies></Lobbies>
      </Navbar>
    </div>
  );
}

export default App;
