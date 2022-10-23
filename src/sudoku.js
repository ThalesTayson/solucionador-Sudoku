import {React, useState, useEffect } from "react"
import Botao from './botao.js'
import py from './py.py'
import Pyloader from './loading.js'
import './sudoku.css';

function Sudoku(props) {
    
    let edit = [];
    for (let i = 0; i < 81; i++){
        edit.push(null);
    }
    const [valuesInputs,setValuesInputs] = useState(edit);
    const [loading, setLoading] = useState(false);
    useEffect(()=>{
        setTimeout(()=>{
            if (document.getElementById("pyscript_loading_splash")){
                setLoading(true);
            } else {
                setLoading(false);
            }
        },1000);

    },[loading]);

    return <main>
        <section className="sudoku">
            {valuesInputs.map((value, index) => {
                return <input type="number" className="Input-Number" id={`ipt${index}`} onChange={(ev)=>{
                    let edit = [...valuesInputs];
                    edit[`${index}`] = ev.target.value;
                    setValuesInputs(edit);
                }}/>;
            })}
        </section>
        <section>
            <Botao valor={valuesInputs} />
        </section>
        <section>
            <p id="retorno"></p>
            <p id="tentativas"></p>
        </section>
        <py-script defer src={py}></py-script>
        {(loading)? <Pyloader/> : <></>}
    </main>

}

export default Sudoku;