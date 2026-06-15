Trabalho Prático 3 – Fluxo Máximo em Redes

UVA 259 – Software Allocation

Link do problema:
https://onlinejudge.org/external/2/259.pdf

Link da apresentação:
https://youtu.be/CVBkSehx4jQ

Integrantes

* Lucas Bezerra
* Davi Cysne
* Gabriel Trajano
* Thiago Holanda
* Artur da Ponte

Linguagem utilizada

Python 3

Como executar

python trabalho_grafos.py < entrada.txt

ou

python3 trabalho_grafos.py < entrada.txt

Resumo do problema

O problema apresenta um conjunto de aplicações que precisam ser executadas em computadores.

Existem 10 computadores, numerados de 0 a 9, e até 26 aplicações identificadas pelas letras A até Z.

Cada aplicação informa:

* Quantas instâncias precisam ser executadas;
* Em quais computadores ela pode rodar.

Cada computador pode executar no máximo uma aplicação.

O objetivo é verificar se todas as aplicações podem ser alocadas respeitando essas restrições.

Caso exista uma alocação válida, devemos indicar qual aplicação foi atribuída a cada computador. Caso contrário, devemos imprimir !.

⸻

Modelagem como Rede de Fluxo

Transformamos o problema em uma rede de fluxo composta por quatro camadas.

Origem
   ↓
Aplicações
   ↓
Computadores
   ↓
Sorvedouro

Vértices

Origem (S)

Representa todas as demandas das aplicações.

É dela que partem as unidades de fluxo que precisam ser alocadas.

Aplicações (A…Z)

Representam as aplicações que precisam ser executadas.

Computadores (0…9)

Representam os recursos disponíveis para execução.

Sorvedouro (T)

Representa as alocações concluídas.

Quando uma unidade de fluxo chega ao sorvedouro, significa que uma aplicação foi atribuída com sucesso a um computador.

⸻

Arestas e Capacidades

Origem → Aplicação

Capacidade igual à quantidade de usuários da aplicação.

Exemplo:

A4 01234;

gera:

S → A (4)

Significando que quatro instâncias da aplicação A precisam ser alocadas.

⸻

Aplicação → Computador

Capacidade igual a 1.

A aresta só existe se aquele computador for compatível com a aplicação.

Exemplo:

A → 0
A → 1
A → 2
A → 3
A → 4

⸻

Computador → Sorvedouro

Capacidade igual a 1.

Isso garante que cada computador execute no máximo uma aplicação.

0 → T (1)
1 → T (1)
...
9 → T (1)

⸻

Algoritmo Utilizado

Ford-Fulkerson

Foi utilizado o algoritmo Ford-Fulkerson para encontrar o fluxo máximo da rede.

A escolha foi feita porque todos os caminhos aumentantes do problema possuem a mesma estrutura:

S → Aplicação → Computador → T

Como todos possuem o mesmo comprimento, não existe vantagem significativa em utilizar Edmonds-Karp para procurar caminhos mais curtos através de BFS.

O Ford-Fulkerson encontra caminhos aumentantes utilizando DFS até que não exista mais caminho possível entre a origem e o sorvedouro.

⸻

Grafo Residual

Após cada aumento de fluxo, o algoritmo atualiza o grafo residual.

O grafo residual armazena:

* Capacidades ainda disponíveis;
* Arestas reversas.

As arestas reversas permitem desfazer decisões anteriores caso seja necessário encontrar uma alocação melhor.

Esse mecanismo garante que o fluxo máximo encontrado seja correto.

⸻

Como a resposta é obtida

Após o término do algoritmo, observamos as arestas entre aplicações e computadores.

Se uma aresta:

Aplicação → Computador

recebeu fluxo igual a 1, significa que aquele computador foi atribuído àquela aplicação.

Com essas informações montamos a string de saída.

Exemplo:

AAAA_QPPPP

Significa:

0 → A
1 → A
2 → A
3 → A
4 → livre
5 → Q
6 → P
7 → P
8 → P
9 → P

Se o fluxo máximo encontrado for menor que a demanda total das aplicações, a saída será:

!

⸻

Complexidade

Tempo

Ford-Fulkerson:

O(E × F)

Onde:

* E = número de arestas;
* F = valor do fluxo máximo.

Neste problema:

F ≤ 10

Portanto o desempenho é totalmente adequado.

⸻

Memória

A implementação utiliza:

* Lista de adjacência;
* Arestas residuais;
* Arestas reversas.

Complexidade:

O(V + E)

⸻

Casos Especiais

* Fluxo máximo igual à demanda total → existe solução;
* Fluxo máximo menor que a demanda total → imprime !;
* Aplicações sem computadores compatíveis;
* Total de aplicações maior que a capacidade disponível;
* Vários casos de teste separados por linha em branco.

⸻

Exemplo

Entrada

A4 01234;
Q1 5;
P4 56789;

Saída

AAAA_QPPPP

O fluxo máximo encontrado é 9, exatamente igual à demanda total das aplicações.

Portanto existe uma alocação válida.

⸻

Evidência de Submissão

A imagem da submissão aceita encontra-se na pasta:

evidencias/accepted.jpeg