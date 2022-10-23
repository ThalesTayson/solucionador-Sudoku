import './App.css';
import Sudoku from './sudoku.js';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Solucionador de Sudoku - App feito usando React e Python</h1>
      </header>
      <Sudoku/>
      <footer> &copy; Desenvolvido por Thales </footer>
    </div>
  );
}

export default App;
