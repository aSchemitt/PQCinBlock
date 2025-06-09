# BlockSignPQC

**BlockSignPQC** é um benchmark modular e extensível para avaliação de 
algoritmos de assinatura digital pós-quântica (PQC) em sistemas blockchain.
Ele permite medições diretas de desempenho criptográfico e simulações realistas
de redes blockchain por meio da integração com o simulador BlockSim.

## Índice

- [Objetivos](#objetivos)
- [Estrutura da Ferramenta](#estrutura-da-ferramenta)
- [Diretórios](#diretórios)
- [Pré-requisitos](#pré-requisitos)
- [Ambiente Virtual](#ambiente-virtual)
- [Lista de Parâmetros](#lista-de-parâmetros)
- [Execução](#execução)
- [Simulação](#simulação)
- [Adicionando Novos Algoritmos](#adicionando-novos-algoritmos)
- [Reprodução dos Experimentos](#reprodução-dos-experimentos-descritos-no-artigo)
- [Publicação](#publicação)


## Objetivos

- Comparar algoritmos clássicos (como ECDSA) e pós-quânticos (como Dilithium, Falcon, SPHINCS+).
- Integrar novos algoritmos de forma contínua e modular.
- Simular o impacto sistêmico dos algoritmos em ambientes blockchain.

## Estrutura da Ferramenta

A ferramenta é dividida em três módulos principais:

1. **`sign_python`**: Executa os algoritmos e mede tempo de assinatura, verificação e geração de chaves.
2. **`blocksim`**: Simula redes blockchain usando os tempos coletados.
3. **`visualization`**: Gera gráficos a partir dos dados dos dois módulos anteriores.

## Diretórios
```bash
BlockSignPQC
├── algorithms/ # Implementações dos algoritmos PQC
├── visualization/ # Gera gráfico
├── save.py # Responsável por salvar saídas
├── utils.py 
├── simulation.py # Executa o simulador BlockSim
└── main.py # Função principal de controle
```

## Pré-requisitos

- [Python 3.11.2](https://www.python.org/downloads/release/python-3112/)
- [liboqs](https://github.com/open-quantum-safe/liboqs)
- [liboqs-python](https://github.com/open-quantum-safe/liboqs-python)

### Instalando pré-requisitos:

Conceda permissão de execução ao script de instalação usando o comando
```bash
chmod +x install.sh
```
Execute o comando abaixo para instalar os pré-requisitos.
```bash
./install.sh
```

>Recomenda-se utilizar a mesma versão do `liboqs` e do `liboqs-python`. Por padrão, estamos utilizando a versão `0.12.0`, definida nas variáveis no início do arquivo [install.sh](./install.sh).

## Ambiente virtual

Antes de executar o BlockSignPQC, é preciso ativar o ambiente virtual.

Ativar o ambiente virtual.
```bash
source venv/bin/activate
```

Desativar o ambiente virtual.
```bash
deactivate
```

## Lista de Parâmetros  

Descrição dos argumentos do BlockSignPQC

| Parâmetro          | Descrição                                            |
| ------------------ | ---------------------------------------------------- |
| `--sign`           | Lista de algoritmos de assinatura digital a serem avaliados. Suporta múltiplos valores, incluindo algoritmos clássicos (*e.g. *ECDSA*) e pós-quânticos (*e.g.* *Dilithium*, *Falcon*, *SPHINCS+*). |
| `--runs`           | Número de execuções de cada algoritmo para coleta de métricas.                                                  |
| `--warm-up`        | Número de execuções de aquecimento (*warm-up*) antes da medição principal, para estabilização de desempenho.    |
| `--levels`         | Define os níveis de segurança do *NIST* (1 a 5) dos algoritmos a serem testados. Pode receber múltiplos valores.|
| `--runs-simulator` | Número de execuções da simulação no *BlockSim*.                                                                 |
| `--list-sign`      | Exibe todos os algoritmos de assinatura disponíveis na ferramenta.                                              |
| `--help`           |  Exibe a mensagem de ajuda com a descrição de todos os argumentos disponíveis e instruções de uso da ferramenta.|


## Execução

Consulte os argumentos disponíveis utilizando a opção `--help`.

```bash
python main.py --help
```

```text
usage: main.py [-h]
               [--sign {sphincs-sha-f,mldsa,cross-rsdpg-balanced,cross-rsdp-fast,ecdsa,cross-rsdpg-fast,sphincs-sha-s,falcon,falcon-padded,cross-rsdp-balanced,mayo,sphincs-shake-f,cross-rsdp-small,cross-rsdpg-small,dilithium,sphincs-shake-s} [{sphincs-sha-f,mldsa,cross-rsdpg-balanced,cross-rsdp-fast,ecdsa,cross-rsdpg-fast,sphincs-sha-s,falcon,falcon-padded,cross-rsdp-balanced,mayo,sphincs-shake-f,cross-rsdp-small,cross-rsdpg-small,dilithium,sphincs-shake-s} ...]]
               [--levels {1,2,3,4,5} [{1,2,3,4,5} ...]] [--runs RUNS] [--warm-up WARM_UP] [--list-sign] [--runs-simulator RUNS_SIMULATOR]

BlockSignPQC

options:
  -h, --help            show this help message and exit
  --sign {sphincs-sha-f,mldsa,cross-rsdpg-balanced,cross-rsdp-fast,ecdsa,cross-rsdpg-fast,sphincs-sha-s,falcon,falcon-padded,cross-rsdp-balanced,mayo,sphincs-shake-f,cross-rsdp-small,cross-rsdpg-small,dilithium,sphincs-shake-s} [{sphincs-sha-f,mldsa,cross-rsdpg-balanced,cross-rsdp-fast,ecdsa,cross-rsdpg-fast,sphincs-sha-s,falcon,falcon-padded,cross-rsdp-balanced,mayo,sphincs-shake-f,cross-rsdp-small,cross-rsdpg-small,dilithium,sphincs-shake-s} ...]
                        Input list of digital signature algorithms (default: None)
  --levels {1,2,3,4,5} [{1,2,3,4,5} ...], -l {1,2,3,4,5} [{1,2,3,4,5} ...]
                        Nist levels (default: range(1, 6))
  --runs RUNS, -r RUNS  Number of executions (default: 1)
  --warm-up WARM_UP, -wp WARM_UP
                        Number of executions warm up (default: 0)
  --list-sign           List of variants digital signature algorithms (default: False)
  --runs-simulator RUNS_SIMULATOR
                        Number of simulator runs (default: 0)
```
### Lista de variantes dos algoritmos de assinatura digital

```bash
python main.py --list-sign
```
ou
```bash
python main.py --list-sign --levels <levels_list>
```

### Execução dos algoritmos de assinatura digital

```bash
python main.py --sign ecdsa mldsa sphincs-shake-f falcon --runs <number_of_executions> --warm-up <number_of_executions> --levels <levels_list>
```

**Exemplo**
```bash
python main.py --sign ecdsa mldsa falcon sphincs-sha-s sphincs-shake-f --runs 5 --warm-up 5 --levels 1 3 5
```

### Simulação

Use o argumento `---runs-simulator`

## Adicionando Novos Algoritmos
```python
import pandas as pd
ALGORITHMS = {
    "algortihm_name": {
        <level_1>: "variant_name",
        <level_2>: "variant_name",
        ...
        <level_5>: "variant_name", 
    }, ...
}

def time_evaluation(variant: str, runs: int):
    # Implementação do benchmark
    return pd.DataFrame({
        'variant': [variant] * runs,
        'sign': time_sign,
        'verify': time_verify
    })
```

## Reprodução dos Experimentos Descritos no Artigo

Clone esse repositório.
```bash
git clone https://github.com/PQC-PQS/BlockSignPQC.git
```
Conceda permissão de execução para os scripts `install.sh` e `run.sh`.
```bash
chmod +x install.sh run.sh
```
Execute os experimentos descritos no artigo com o comando:
```bash
./run.sh
```

## Publicação

Esta ferramenta foi apresentada no SBSeg 2025, como parte do artigo:

> BlockSignPQC: um benchmark para avaliação de algoritmos de assinatura digital pós-quântica em blockchains.
