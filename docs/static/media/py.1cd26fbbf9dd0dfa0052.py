import js
from pyodide.ffi import create_proxy
    
class solucionaSudoku(object):
    subst={0:1,1:1,2:1,3:2,4:2,5:2,6:3,7:3,8:3}
    loc = {
            0:[[0,1,2],[0,1,2]],
            1:[[0,1,2],[3,4,5]],
            2:[[0,1,2],[6,7,8]],
            3:[[3,4,5],[0,1,2]],
            4:[[3,4,5],[3,4,5]],
            5:[[3,4,5],[6,7,8]],
            6:[[6,7,8],[0,1,2]],
            7:[[6,7,8],[3,4,5]],
            8:[[6,7,8],[6,7,8]],
        }
    def __init__(self,sudoku) -> None:
        self.sudoku=list(sudoku).copy()
        self.separa_e_armazena()
        if (not self.avaliaSeTemErro()):
            self.alteracoes = self.tenta()
            self.mostra()
        else:
            print("há erros")
            
    def separa_e_armazena(self):
        self.linhas={}
        self.colunas={}
        self.blocos={}
        self.localizacao={}
        self.numeros=[]
        for a, linha in enumerate(self.sudoku):
            for b, valor in enumerate(linha):
                n =(((self.subst[a]*3)-3)+self.subst[b])-1
                if n not in self.blocos.keys():
                    self.blocos[n]=[]
                if a not in self.linhas.keys():
                    self.linhas[a]=[]
                if b not in self.colunas.keys():
                    self.colunas[b]=[]
                if valor!=0:
                    self.blocos[n].append(valor)
                    self.colunas[b].append(valor)
                    self.linhas[a].append(valor)
                self.localizacao[(a*10)+b]={'bloco':n,'linha':a,'coluna':b}
        for n in range(1,10):
            cont=0
            for linha in self.sudoku:
                cont+=linha.count(n)
            if cont<9:
                self.numeros.append(n)
                
    def avaliaSeTemErro(self) -> bool:
        erro = False
        for bloco in self.blocos.keys():
            for valor in self.blocos[bloco]:
                if (valor != 0):
                    print(f"""
                          {self.blocos[bloco]}
                          {valor}
                          {self.blocos[bloco].count(valor)}
                          """)
                    if (self.blocos[bloco].count(valor) > 1):
                        erro = True
        for linha in self.linhas.keys():
            for valor in self.linhas[linha]:
                if (valor != 0):
                    print(f"""
                          {self.linhas[linha]}
                          {valor}
                          {self.linhas[linha].count(valor)}
                          """)
                    if (self.linhas[linha].count(valor) > 1):
                        erro = True
        for coluna in self.colunas.keys():
            for valor in self.colunas[coluna]:
                if (valor != 0):
                    print(f"""
                          {self.colunas[coluna]}
                          {valor}
                          {self.colunas[coluna].count(valor)}
                          """)
                    if (self.colunas[coluna].count(valor) > 1):
                        erro = True
        return erro
    
    def reseta_lin_col_blo(self):
        for i in range(9):
            self.blocos[i].clear()
            self.colunas[i].clear()
            self.linhas[i].clear()
        for a, linha in enumerate(self.sudoku):
            for b, valor in enumerate(linha):
                if valor!=0:
                    n =(((self.subst[a]*3)-3)+self.subst[b])-1
                    self.blocos[n].append(valor)
                    self.colunas[b].append(valor)
                    self.linhas[a].append(valor)
    def possibilidade(self) -> dict:
        possiveis=None
        possiveis={}
        for n in self.numeros:
            cont=0
            for linha in self.sudoku:
                cont+=linha.count(n)
            if (cont>=9):
                index = self.numeros.index(n)
                self.numeros.pop(index)

        for i, linha in enumerate(self.sudoku):
            if i not in possiveis:
                possiveis[i]={}
            for j, valor in enumerate(linha):
                if j not in possiveis[i]:
                    possiveis[i][j]=[]
                if valor>0:
                    possiveis[i][j].append(valor)
                else:
                    b=self.localizacao[(i*10)+j]['bloco']
                    for n in self.numeros:
                        if (self.linhas[i].count(n)==0):
                            if (self.colunas[j].count(n)==0):
                                if (self.blocos[b].count(n)==0):
                                    possiveis[i][j].append(n)
        return possiveis

    def insere_no_sudoku(self,i,j,p)->bool:
        ok=False
        b=self.localizacao[(i*10)+j]['bloco']

        if (self.linhas[i].count(p)==0):
            if (self.colunas[j].count(p)==0):
                if (self.blocos[b].count(p)==0):
                    self.sudoku[i][j]=p
                    self.colunas[j].append(p)
                    self.blocos[b].append(p)
                    self.linhas[i].append(p)
                    inputSetValue(row=i,col=j,valor=p)
                    ok=True
        return ok

    def insere_o_obvio(self)-> int:
        cont=0
        up=True
        while up==True:
            up=False
            for i, linha in enumerate(self.sudoku):
                if len(self.linhas[i])==9:
                    break
                for j, valor in enumerate(linha):
                    if len(self.colunas[j])==9:
                        break
                    if (valor==0):
                        b=self.localizacao[(i*10)+j]['bloco']
                        if len(self.blocos[b])==9:
                            break
                        possiveis = self.possibilidade()
                        if len(possiveis[i][j])==1:
                            up=True
                            p=possiveis[i][j][0]
                            if self.insere_no_sudoku(i=i,j=j,p=p)==True:
                                cont+=1
        return cont

    def unico_linha(self)-> int:
        cont=0
        up=True
        while up==True:
            up=False
            for i, linha in enumerate(self.sudoku):
                if len(self.linhas[i])==9:
                    break
                for j, valor in enumerate(linha):
                    if len(self.colunas[j])==9:
                        break
                    if (valor==0):
                        b=self.localizacao[(i*10)+j]['bloco']
                        if len(self.blocos[b])==9:
                            break
                        possiveis = self.possibilidade()
                        for p in possiveis[i][j]:
                            unico=True
                            for c in range(9):
                                if (c!=j):
                                    if (possiveis[i][c].count(p)>0):
                                        unico=False
                            if unico:                     
                                if self.insere_no_sudoku(i=i,j=j,p=p)==True:
                                    cont+=1
                                break
        return cont

    def unico_coluna(self)-> int:
        cont=0
        up=True
        while up==True:
            up=False
            possiveis = self.possibilidade()
            for i, linha in enumerate(self.sudoku):
                if len(self.linhas[i])==9:
                    break
                for j, valor in enumerate(linha):
                    if len(self.colunas[j])==9:
                        break
                    if (valor==0):
                        b=self.localizacao[(i*10)+j]['bloco']
                        if len(self.blocos[b])==9:
                            break
                        for p in possiveis[i][j]:
                            unico=True
                            for l in range(9):
                                if (l!=i):
                                    if (possiveis[l][j].count(p)>0):
                                        unico=False
                            if unico:                     
                                if self.insere_no_sudoku(i=i,j=j,p=p)==True:
                                    cont+=1
                                break
        return cont

    def tenta(self)-> int:
        anteriores=[]
        cont=0
        memoria=-1
        continua=True
        while continua:
            obvias= self.insere_o_obvio()
            linha= self.unico_linha()
            coluna= self.unico_coluna()
            alteracoes=obvias+linha+coluna
            if alteracoes==0:
                if (self.verifica_ok()==True):
                    if (self.verifica_se_concluiu()==True):
                        continua=False
                    else:
                        palpite = self.palpite_chute()
                        i=int(palpite[0])
                        j=int(palpite[1])
                        p=int(palpite[2][0])
                        memoria+=1
                        gravar=[]
                        for linha in self.sudoku:
                            gravar.append((linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8]))
                        gravar = tuple(gravar)
                        anteriores.append([gravar,0,palpite])
                        if self.insere_no_sudoku(i=i,j=j,p=p)==True:
                            cont+=1
                        else:
                            continua=False
                else:
                    if memoria<0:
                        continua=False
                    else:
                        palpite=None
                        palpite=anteriores[memoria][2]
                        anteriores[memoria][1]+=1
                        indice=int(anteriores[memoria][1])
                        if indice<len(palpite[2]):
                            self.sudoku.clear()
                            for a in range(9):
                                self.sudoku.append([])
                                for b in range(9):
                                    self.sudoku[a].append(anteriores[memoria][0][a][b])
                            self.reseta_lin_col_blo()
                            i=palpite[0]
                            j=palpite[1]
                            p=palpite[2][indice]
                            if self.insere_no_sudoku(i=i,j=j,p=p)==True:
                                cont+=1
                        else:
                            anteriores.pop(memoria)
                            memoria-=1
            cont+=alteracoes
        return cont

    def palpite_chute(self)-> tuple:
        lista={}
        possiveis = self.possibilidade()
        for a in range(9):
            bloco =len(self.blocos[a])
            coluna=len(self.colunas[a])
            linha=len(self.linhas[a])
            if bloco not in lista.keys():
                if bloco<9:
                    for i in self.loc[a][0]:
                        for j in self.loc[a][1]:
                            if (self.sudoku[i][j]==0):
                                p = possiveis[i][j]
                                lista[bloco]=[i,j,p]

            if coluna not in lista.keys():
                if coluna<9:
                    for i in range(9):
                        if (self.sudoku[i][a]==0):
                            p = possiveis[i][a]
                            lista[bloco]=[i,a,p]

            if linha not in lista.keys():
                if linha<9:
                    for j in range(9):
                        if (self.sudoku[a][j]==0):
                            p = possiveis[a][j]
                            lista[bloco]=[a,j,p]
        chave=max(lista.keys())
        return int(lista[chave][0]),int(lista[chave][1]),tuple(lista[chave][2])

    def verifica_ok(self) ->bool:
        self.reseta_lin_col_blo()
        possiveis = self.possibilidade()
        ok=True
        for i in possiveis.keys():
            for j in possiveis[i].keys():
                if len(possiveis[i][j])==0:
                    ok=False
        return ok
    
    def verifica_se_concluiu(self)->bool:
        self.reseta_lin_col_blo()
        ok=True
        for a in range(9):
            if (sum(self.linhas[a])!=45) or (sum(self.colunas[a])!=45) or (sum(self.blocos[a])!=45):
                ok=False
        return ok

    def mostra(self):
        if self.verifica_se_concluiu()==True:
            retorno = 'Sudoku Solucionado com sucesso!'
        else:
            retorno = 'Solucionador não obteve sucesso!'
        tentativas = f'->Houveram {self.alteracoes} jogadas'
        Element('retorno').element.textContent = retorno
        Element('tentativas').element.textContent = tentativas

def resolveSudoku(input_js : str):
    edit_input = input_js.split(",")
    input_sudoku = []
    i=0
    for a in range(9):
        input_sudoku.append([])
        for b in range(9):
            input_sudoku[a].append(int(edit_input[i]))
            i += 1
    task = solucionaSudoku(input_sudoku)
    
def onClick(event=None):
    resolveSudoku(Element('inputSudoku').element.value)

def inputSetValue(row,col,valor):
    loc = (row * 9) + col
    
    Element(f'ipt{loc}').element.value = valor
    
Element('resolver').element.onclick = onClick


    
    