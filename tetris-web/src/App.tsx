import React, { useEffect } from "react";
import { Navbar } from "./components/Navbar";
import "./index.css";
import "halfmoon/css/halfmoon-variables.min.css";
import { SignUp } from "./components/SignUp";

function App() {
  const halfmoon = require("halfmoon");

  useEffect(() => {
    halfmoon.onDOMContentLoaded();
  }, [halfmoon]);

  return (
    <div className="App">
      <Navbar>
        <SignUp></SignUp>
      </Navbar>
    </div>
  );
}

export default App;
