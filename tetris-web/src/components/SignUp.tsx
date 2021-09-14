import React, { useEffect } from "react";
import { signup } from "../api/account";

interface Props {}

export const SignUp: React.FC<Props> = (props: Props) => {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [confirmPassword, setConfirmPassword] = React.useState("");

  const [passwordValid, setPasswordValid] = React.useState(true);
  const [passwordsMatch, setPasswordsMatch] = React.useState(true);
  const [usernameAvailable, setUsernameAvailable] = React.useState(true);

  //Check if password satisifes the password requirements
  useEffect(() => {
    setPasswordValid(passwordIsValid(password) || password.length === 0);
  }, [password]);

  //Check if passwords match
  useEffect(() => {
    setPasswordsMatch(
      password === confirmPassword || confirmPassword.length === 0
    );
  }, [password, confirmPassword]);

  //Submit the form
  const onSubmit = async (e: any) => {
    e.preventDefault();

    if (
      passwordValid &&
      passwordsMatch &&
      password.length >= 8 &&
      username.length > 0
    ) {
      //TODO: Hash password client side?
      //TODO: Check if username is available
      signup(username, password)
        .then(() => console.log("Success!"))
        .catch((err) => {
          setUsernameAvailable(false);
          console.log(err);
        });
    }
  };

  return (
    <div className="w-400 card">
      <h2 className="card-title">Sign Up</h2>
      <form onSubmit={onSubmit} className="w-400 mw-full">
        <div
          className={"form-group " + (!usernameAvailable ? "is-invalid" : "")}
        >
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
          {!usernameAvailable && (
            <div className="invalid-feedback">
              This username is already taken.
            </div>
          )}
        </div>
        <div className={"form-group " + (!passwordValid ? "is-invalid" : "")}>
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
          {!passwordValid && (
            <div className="invalid-feedback">
              <ul>
                <li>Password must be at least 8 characters long</li>
                <li>Contain at least one digit (0-9)</li>
                <li>Contain at least one uppercase letter (A-Z)</li>
              </ul>
            </div>
          )}
        </div>
        <div className={"form-group " + (!passwordsMatch ? "is-invalid" : "")}>
          <label htmlFor="confirm-password" className="required">
            Confirm password
          </label>
          <input
            type="password"
            className="form-control"
            id="confirm-password"
            placeholder="Confirm password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          {!passwordsMatch && (
            <div className="invalid-feedback">The passwords don't match.</div>
          )}
        </div>
        <div className="form-group">
          <input
            className="btn btn-primary btn-block"
            type="submit"
            value="Sign up"
          />
        </div>
        <span className="space-top">
          Already have an account? <a href="/signin">Sign in</a>
        </span>
      </form>
    </div>
  );
};

/**
 * Checks if the password fullfills the requirements.
 * @param password The password to validate
 * @returns true if the password is valid, false otherwise
 */
const passwordIsValid = (password: string) => {
  const passwordLengthValid = password.length >= 8;
  const passwordContainsCaps = password.match(/[A-Z]/) !== null;
  const passwordContainsDigit = password.match(/\d/) !== null;

  return passwordLengthValid && passwordContainsCaps && passwordContainsDigit;
};
