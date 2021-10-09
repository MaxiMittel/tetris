import React from "react";
import { SignIn } from "./SignIn";

interface Props {
    children: React.ReactNode;
}

export const Secured: React.FC<Props> = (props: Props) => {

    const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  
  return (
    <div>
      {isLoggedIn && (props.children)}
      {!isLoggedIn && (<SignIn></SignIn>)}
    </div>
  );
};
