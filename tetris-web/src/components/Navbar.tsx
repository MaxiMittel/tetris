import React from "react";

interface Props {
  authenticated: boolean;
  buttonText: string;
  children: any;
}

export const Navbar: React.FC<Props> = (props: Props) => {
  const openLink = () => {
    if (props.authenticated) {
      window.location.href = "/account";
    } else {
      window.location.href = "/signin";
    }
  };

  return (
    <div>
      <div className="page-wrapper with-navbar">
        <nav className="navbar">
          <a href="/" className="navbar-brand">
            <img
              src="logo_text.png"
              alt="logo"
            />
          </a>
          <ul className="navbar-nav d-none d-md-flex">
            <li className="nav-item active">
              <a href="/" className="nav-link">
                Play
              </a>
            </li>
            <li className="nav-item">
              <a href="/search" className="nav-link">
                Search
              </a>
            </li>
          </ul>
          <div className="form-inline d-none d-md-flex ml-auto">
            <button
              className="btn btn-primary"
              type="submit"
              onClick={openLink}
            >
              {props.buttonText}
            </button>
          </div>
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
                <a href="/" className="dropdown-item">
                  Play
                </a>
                <a href="/search" className="dropdown-item">
                  Search
                </a>
                <div className="dropdown-divider"></div>
                <div className="dropdown-content">
                  <button
                    className="btn btn-primary btn-block"
                    type="submit"
                    onClick={openLink}
                  >
                    {props.buttonText}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <div className="content-wrapper">{props.children}</div>
      </div>
    </div>
  );
};
