import { Link, useMatch, useResolvedPath } from "react-router-dom";
import './NavBar.css';

export default function NavBar() {
    return (
        <nav className="nav">
            <Link to="/" >
                <p className="navbar_title">CodeFlow</p>
            </Link>
            <ul>
                <CustomLink className='navbar_chat' to="/dragdrop">Upload</CustomLink>
                <CustomLink className='navbar_prompt' to="/visual">Chat Bot</CustomLink>
                <CustomLink className='navbar_visualize' onClick={redirectToWebsite}>Visualize</CustomLink>
                <a href="C:\\Users\\12254\\Documents\\GitHub\\HackTheNorth\\app\\func_graph.html">Redirect to Html page</a>
            </ul>
        </nav>
    );
}

function CustomLink({ to, children, ...props }) {
    const resolvedPath = useResolvedPath(to);
    const isActive = useMatch({ path: resolvedPath.pathname, end: true });

    return (
        <li className={isActive ? "active" : ""}>
            <Link to={to} {...props}>
                {children}
            </Link>
        </li>
    );
}

const redirectToWebsite = () =>{
    console.log("1")
    window.location.href= '..\\..\\app\\func_graph.html'
};
