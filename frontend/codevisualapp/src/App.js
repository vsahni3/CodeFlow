import './App.css';
import DragDropFiles from "./components/DragDropFiles";
import CodeVisualizer from './components/CodeVisualizer';
// import { Route, Routes, useNavigate, Link, Navigate } from "react-router-dom";

const App = () => {
    return (
        <div className="container">
            {/* <DragDropFiles /> */}
            <CodeVisualizer />
        </div>
        // <div>
        //     <Routes>
        //         <Route path="/dragdrop" element={<DragDropFiles/>} />
        //         <Route path="/visual" element={<CodeVisualizer/>} />
        //     </Routes>
        // </div>
    )
};

export default App;
