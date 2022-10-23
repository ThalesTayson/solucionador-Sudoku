
const resolver = function(dados){
    let cnv = [];
    dados.forEach((value) => {
        if ((value === "" | value === null)){
            value = 0;
        }
        cnv = [...cnv, value];
    });
    return cnv;
}

function Botao(props){
    let sudoku = resolver(props.valor);
    return (
    <>
        <input type="hidden" value={sudoku} id="inputSudoku" />
        <input type="button" value="Resolver" id="resolver" />
    </>
    )
}

export default Botao;