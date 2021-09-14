import React from "react";

interface Props {

}

export const Navbar: React.FC<Props> = ({children}) => {
  return (
    <div>
      <div className="page-wrapper with-navbar">
        <nav className="navbar">
          <a href="/" className="navbar-brand">
            <img
              src="https://www.gethalfmoon.com/static/halfmoon/img/hm-logo-white.svg"
              alt="logo"
            />
          </a>
          <ul className="navbar-nav d-none d-md-flex">
            <li className="nav-item active">
              <a href="/play" className="nav-link">
                Play
              </a>
            </li>
            <li className="nav-item">
              <a href="/account" className="nav-link">
                Account
              </a>
            </li>
          </ul>
          <form
            className="form-inline d-none d-md-flex ml-auto"
            action="..."
            method="..."
          >
            <input
              type="text"
              className="form-control"
              placeholder="Search ..."
              required
            />
            <button className="btn btn-primary" type="submit">
              Sign up
            </button>
          </form>
          <div className="navbar-content d-md-none ml-auto">
            <div className="dropdown with-arrow">
              <button
                className="btn"
                data-toggle="dropdown"
                type="button"
                id="navbar-dropdown-toggle-btn-1"
              >
                Menu
                <i className="fa fa-angle-down" aria-hidden="true"></i>
              </button>
              <div
                className="dropdown-menu dropdown-menu-right w-200"
                aria-labelledby="navbar-dropdown-toggle-btn-1"
              >
                <a href="/play" className="dropdown-item">
                  Play
                </a>
                <a href="/account" className="dropdown-item">
                  Account
                </a>
                <div className="dropdown-divider"></div>
                <div className="dropdown-content">
                  <form action="..." method="...">
                    <div className="form-group">
                      <input
                        type="text"
                        className="form-control"
                        placeholder="Email address"
                        required
                      />
                    </div>
                    <button className="btn btn-primary btn-block" type="submit">
                      Sign up
                    </button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <div className="content-wrapper">
          {children}
        </div>
      </div>
    </div>
  );
};
