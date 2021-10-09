import { useEffect } from "react";
import { Navbar } from "./components/Navbar";
import "./index.css";
import "halfmoon/css/halfmoon-variables.min.css";
import { SignIn } from "./components/SignIn";

function App() {
  const halfmoon = require("halfmoon");

  useEffect(() => {
    halfmoon.onDOMContentLoaded();
  }, [halfmoon]);

  return (
    <div className="App">
      <Navbar>
        <SignIn></SignIn>
      </Navbar>
    </div>
  );
}

export default App;
