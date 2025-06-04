# BlockSignPQC

## Instalação da `liboqs` e do `liboqs-python`

Conceda permissão de execução ao arquivo de instalação usando o comando
```bash
chmod +x install.sh
```

Execute o comando abaixo para instalar o `liboqs` e o `liboqs-python`.
```bash
./install.sh
```

>Recomenda-se utilizar a mesma versão do `liboqs` e do `liboqs-python`. Por padrão, estamos utilizando a versão `0.12.0`, definida nas variáveis no início do arquivo [install.sh](./install.sh).

## Ambiente virtual

Antes de executar os algoritmos, é preciso ativar o ambiente virtual.

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
python main.py --list-sig --levels <levels_list>
```

### Execução dos algoritmos de assinatura digital

```bash
python main.py --sig ecdsa mldsa sphincs-shake-f falcon --runs <number_of_executions> --warp-up <number_of_executions> --levels <levels_list>
```

### Exemplo

```bash
source venv/bin/activate
```

```bash
python main.py --sig ecdsa mldsa falcon sphincs-sha-s sphincs-shake-f --runs 5 --warm-up 5 --levels 1 3 5
```
