import React, { useEffect } from "react";
import { Navbar } from "./components/Navbar";
import "./index.css";
import "halfmoon/css/halfmoon-variables.min.css";
import { Account } from "./components/Account";

function App() {
  const halfmoon = require("halfmoon");

  useEffect(() => {
    halfmoon.onDOMContentLoaded();
  }, [halfmoon]);

  return (
    <div className="App">
      <Navbar>
        <Account></Account>
      </Navbar>
    </div>
  );
}

export default App;
