import re
import sys


FONTE = 0
BASE_APLICACOES = 1
BASE_COMPUTADORES = 27
SORVEDOURO = 37
NUM_COMPUTADORES = 10


class Aresta:
    def __init__(self, destino, indice_reversa, capacidade):
        self.destino = destino
        self.indice_reversa = indice_reversa
        self.capacidade = capacidade


class RedeFluxo:
    def __init__(self, tamanho):
        self.grafo = [[] for _ in range(tamanho)]

    def adicionar_aresta(self, origem, destino, capacidade):
        direta = Aresta(destino, len(self.grafo[destino]), capacidade)
        reversa = Aresta(origem, len(self.grafo[origem]), 0)
        self.grafo[origem].append(direta)
        self.grafo[destino].append(reversa)

    def enviar_fluxo_dfs(self, vertice_atual, sorvedouro, fluxo, visitado):
        if vertice_atual == sorvedouro:
            return fluxo

        visitado[vertice_atual] = True

        for aresta in self.grafo[vertice_atual]:
            if aresta.capacidade > 0 and not visitado[aresta.destino]:
                fluxo_enviado = self.enviar_fluxo_dfs(
                    aresta.destino,
                    sorvedouro,
                    min(fluxo, aresta.capacidade),
                    visitado,
                )

                if fluxo_enviado > 0:
                    aresta.capacidade -= fluxo_enviado
                    self.grafo[aresta.destino][aresta.indice_reversa].capacidade += fluxo_enviado
                    return fluxo_enviado

        return 0

    def ford_fulkerson(self, fonte, sorvedouro):
        fluxo_maximo = 0

        while True:
            visitado = [False] * len(self.grafo)
            fluxo_caminho = self.enviar_fluxo_dfs(fonte, sorvedouro, 10**9, visitado)

            if fluxo_caminho == 0:
                break
            fluxo_maximo += fluxo_caminho

        return fluxo_maximo


def no_aplicacao(letra):
    return BASE_APLICACOES + ord(letra) - ord("A")


def no_computador(numero):
    return BASE_COMPUTADORES + numero


def ler_caso(linhas):
    tarefas = []
    for linha in linhas:
        linha = linha.strip()
        if not re.match(r"^[A-Z][0-9] [0-9]+;$", linha):
            continue

        aplicacao = linha[0]
        demanda = int(linha[1])
        computadores = [int(ch) for ch in linha.split()[1].rstrip(";")]
        tarefas.append((aplicacao, demanda, computadores))
    return tarefas


def ler_casos(linhas):
    casos = []
    caso_atual = []

    for linha in linhas:
        if linha.strip():
            caso_atual.append(linha)
        elif caso_atual:
            casos.append(ler_caso(caso_atual))
            caso_atual = []

    if caso_atual:
        casos.append(ler_caso(caso_atual))

    return casos


def ler_linhas_manuais():
    linhas = []
    linhas_em_branco = 0

    while True:
        try:
            linha = input()
        except EOFError:
            break

        if linha.strip():
            linhas_em_branco = 0
            linhas.append(linha + "\n")
        else:
            linhas_em_branco += 1
            linhas.append("\n")
            if linhas_em_branco == 2:
                break

    return linhas


def resolver_caso(tarefas):
    rede = RedeFluxo(SORVEDOURO + 1)
    demanda_total = 0

    for aplicacao, demanda, computadores in tarefas:
        demanda_total += demanda
        rede.adicionar_aresta(FONTE, no_aplicacao(aplicacao), demanda)
        for computador in computadores:
            rede.adicionar_aresta(no_aplicacao(aplicacao), no_computador(computador), 1)

    for computador in range(NUM_COMPUTADORES):
        rede.adicionar_aresta(no_computador(computador), SORVEDOURO, 1)

    if rede.ford_fulkerson(FONTE, SORVEDOURO) != demanda_total:
        return "!"

    resposta = ["_"] * NUM_COMPUTADORES
    for aplicacao, _, _ in tarefas:
        origem = no_aplicacao(aplicacao)
        for aresta in rede.grafo[origem]:
            if BASE_COMPUTADORES <= aresta.destino < BASE_COMPUTADORES + NUM_COMPUTADORES:
                fluxo_usado = rede.grafo[aresta.destino][aresta.indice_reversa].capacidade
                if fluxo_usado > 0:
                    resposta[aresta.destino - BASE_COMPUTADORES] = aplicacao

    return "".join(resposta)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as arquivo:
            linhas = arquivo.readlines()
    elif sys.stdin.isatty():
        linhas = ler_linhas_manuais()
    else:
        linhas = sys.stdin.readlines()

    for caso in ler_casos(linhas):
        print(resolver_caso(caso))


if __name__ == "__main__":
    main()
