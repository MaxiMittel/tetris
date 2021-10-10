import React from "react";
import { SignIn } from "./SignIn";

interface Props {
  children: React.ReactNode;
  authenticated: boolean;
  onAuthenticated: () => void;
}

export const Authenticated: React.FC<Props> = (props: Props) => {
  return (
    <div>
      {props.authenticated && props.children}
      {!props.authenticated && <SignIn onAuthenticated={props.onAuthenticated} />}
    </div>
  );
};
