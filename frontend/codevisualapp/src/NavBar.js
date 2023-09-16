import {Link} from "react-router-dom";

const NavBar = () => {
    return(
        <ul>
          <li><Link to="/dragdrop">Upload Folder/File</Link></li>
          <li><Link to="/visual">Visual</Link></li>
        </ul>
    )
}

export default NavBar