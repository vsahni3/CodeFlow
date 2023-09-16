import './App.css';
import DragDropFiles from "./components/DragDropFiles";
import CodeVisualizer from './components/CodeVisualizer';

const App = () => {
    return (
        <div className="container">
            <DragDropFiles />
            <CodeVisualizer />
        </div>
    )
};

export default App;
