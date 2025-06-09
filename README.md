# BlockSignPQC

**BlockSignPQC** é um benchmark modular e extensível para avaliação de 
algoritmos de assinatura digital pós-quântica (PQC) em sistemas blockchain.
Ele permite medições diretas de desempenho criptográfico e simulações realistas
de redes blockchain por meio da integração com o simulador BlockSim.

## Objetivos

- Comparar algoritmos clássicos (como ECDSA) e pós-quânticos (como Dilithium, Falcon, SPHINCS+).
- Integrar novos algoritmos de forma contínua e modular.
- Simular o impacto sistêmico dos algoritmos em ambientes blockchain.


## Estrutura da Ferramenta

A ferramenta é dividida em três módulos principais:

1. **`sign_python`**: executa os algoritmos e mede tempo de assinatura, verificação e geração de chaves.
2. **`blocksim`**: simula redes blockchain usando os tempos coletados.
3. **`visualization`**: gera gráficos a partir dos dados dos dois módulos anteriores.

## Diretórios
```bash
├── algorithms/ # Implementações dos algoritmos PQC

```

## Pré-requisitos

- Python 3.11.2
- [liboqs](https://github.com/open-quantum-safe/liboqs)
- [liboqs-python](https://github.com/open-quantum-safe/liboqs-python)
- Bibliotecas Python: `cryptography`, `matplotlib`, `pandas`, `numpy`

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

Antes de executar o BockSignPQC, é preciso ativar o ambiente virtual.

Ativar o ambiente virtual.
```bash
source venv/bin/activate
```

Desativar o ambiente virtual.
```bash
deactivate
```

## Execução

Consulte os argumentos disponíveis utilizando a opção `--help`.

```bash
python main.py --help
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
python main.py --sign ecdsa mldsa sphincs-shake-f falcon --runs <number_of_executions> --warp-up <number_of_executions> --levels <levels_list>
```

**Exemplo**
```bash
python main.py --sig ecdsa mldsa falcon sphincs-sha-s sphincs-shake-f --runs 5 --warm-up 5 --levels 1 3 5
```
