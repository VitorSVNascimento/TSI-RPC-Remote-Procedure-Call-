
# TSI-RPC(Remote Procedure Call)

Projeto criado para a disciplina de sistemas distribuidos com o objeto de implementar operações utilizando rpc em python

## O que é RPC?
É um mecanismo que permite a execução de funções ou procedimentos em um sistema distribuído como se eles estivessem sendo chamados localmente, mesmo que estejam em máquinas remotas na rede.

A ideia fundamental por trás do RPC é fornecer uma abstração de chamada de função que permite que os desenvolvedores tratem chamadas de função em sistemas distribuídos da mesma forma que tratariam chamadas de função locais. O RPC é usado para criar uma comunicação transparente entre processos ou objetos distribuídos em sistemas distribuídos, permitindo que eles invoquem funções ou métodos uns dos outros, mesmo que estejam em máquinas diferentes.


## Atualizações 

### Atividade 1 - Criação do rpc
- Criação das classes ClienteRPC e ServerRPC 
- Criação das operações matematicas sum,sub,div,mul

### Atividade 2 - Multiprocessamento
- Criação da operação is_prime onde o servidor retorna os numeros primos de uma lista de numeros
- Implementação de multiprocessamento a essa função 
- Após os testes foi constatado que a operação com multiprocessamento funciona melhor em listas com mais numeros porém, é menos eficiente em listas pequenas.

### Atividade 3 Implementação de cache
-Implementação de um cache simples através de Dict nas operações criadas 

### Atividade 4 Implementação de cache
- Implementação de cache em disco através do arquivo dict.cache
- Sincronização do cache em memória com o cache em disco após tempo limite 
- Definição de limite de registros em disco e memória

### Atividade 5 Implementação de web scraping
- Implementação do recurso de web scrapring para a busca das noticias mais recentes do site IF Sudeste BQ
- Adição de multithread para acelerar o processo quando mais de uma página é solicitada

### Atividade 6 Consistencia e Replicação
- Adição do mecanismo de cache que aproveita os dados caso o número de notícias solicitadas seja menor que um número previamente solicitado
- Adição do mecanismo de consistencia com restrição de no máximo 5 minutos