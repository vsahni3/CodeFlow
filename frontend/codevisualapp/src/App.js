import './App.css';
import DragDropFiles from "./components/DragDropFiles";
import CodeVisualizer from './components/CodeVisualizer';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"; // Import Routes
import NavBar from './NavBar';

const App = () => {
    return (
        <Router>
            <div className="App">
                <NavBar/>
                <div className='Content'>
                    <Routes> 
                        <Route path='/dragdrop' element={<DragDropFiles />} /> 
                        <Route path='/visual' element={<CodeVisualizer />} /> 
                    </Routes>
                </div>
            </div>
        </Router>
    )
};

export default App;

