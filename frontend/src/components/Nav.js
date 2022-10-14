import logo from "../hypeeats_logo.png";
import ContactFormPopup from "./ContactFormPopUp";

function Nav(props) {
  return (
    <div className="nav">
      <header className="app-header">
        <img class="h-11" src={logo} alt="hypeeats logo" />
        <ContactFormPopup />
      </header>
    </div>
  );
}

export default Nav;
