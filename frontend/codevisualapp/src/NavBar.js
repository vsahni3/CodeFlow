import { Link, useMatch, useResolvedPath } from "react-router-dom";
import './NavBar.css';
import { useNavigate } from "react-router-dom";
export default function NavBar() {

    function clickFunc () {
        
        window.location.href = 'https://aparahuja.github.io';
    }
    return (
        <nav className="nav">
            <Link to="/" >
                <p className="navbar_title">CodeFlow</p>
            </Link>
            <ul>
                <CustomLink className='navbar_chat' to="/dragdrop">Upload</CustomLink>

                <CustomLink className='navbar_prompt' to="/visual">Chat Bot</CustomLink>
                <CustomLink className='navbar_visualize' onClick={clickFunc}>Visualize</CustomLink>
               

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
