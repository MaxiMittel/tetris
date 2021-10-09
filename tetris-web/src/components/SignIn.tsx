import React from "react";
import { signup } from "../api/account";

interface Props {
  onAuthenticated: () => void;
}

export const SignIn: React.FC<Props> = (props: Props) => {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");

  const [loginSuccessfull, setLoginSuccessfull] = React.useState(true);

  //Submit the form
  const onSubmit = async (e: any) => {
    e.preventDefault();

    signup(username, password)
      .then(response => {
        setLoginSuccessfull(true);
        localStorage.setItem("token", response.data.token);
        props.onAuthenticated();
      })
      .catch((err) => {
        setLoginSuccessfull(false);
        console.log(err);
      });
  };

  return (
    <div className="w-400 card">
      <h2 className="card-title">Sign In</h2>
      <form onSubmit={onSubmit} className="w-400 mw-full">
        <div className={"form-group"}>
          <label htmlFor="username" className="required">
            Username
          </label>
          <input
            type="text"
            className="form-control"
            id="username"
            placeholder="Username"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div
          className={"form-group " + (!loginSuccessfull ? "is-invalid" : "")}
        >
          <label htmlFor="password" className="required">
            Password
          </label>
          <input
            type="password"
            className="form-control"
            id="password"
            placeholder="Password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {!loginSuccessfull && (
            <div className="invalid-feedback">
              The username or password is incorrect.
            </div>
          )}
        </div>
        <div className="form-group">
          <input
            className="btn btn-primary btn-block"
            type="submit"
            value="Sign in"
          />
        </div>
        <span className="space-top">
          Don't have an account? <a href="/signup">Sign up</a>
        </span>
      </form>
    </div>
  );
};
