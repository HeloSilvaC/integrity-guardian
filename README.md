# Guardião de Integridade

Monitor de integridade de arquivos que usa SHA-256 para detectar arquivos **modificados**, **novos** e **removidos** em um diretório, com automação via Shell Script.

> Trabalho 2 da disciplina de **Sistemas Operacionais (BCC5002)**, Bacharelado em Ciência da Computação, UTFPR, Campus Campo Mourão.
> Prof. Dr. Rodrigo Hübner, semestre 2026/2.

## Integrantes

| Nome | GitHub |
|---|---|
| Heloísa da Silva Contrera | [@HeloSilvaC](https://github.com/HeloSilvaC) |
| Paola Miyuki Ukuma Precinotto | [@Paola-Miyuki](https://github.com/Paola-Miyuki) |

---

## Sobre

O Guardião funciona em duas etapas:

1. **Cadastro:** percorre recursivamente um diretório, calcula o hash SHA-256 de cada arquivo e salva uma **referência** com nome, caminho relativo e hash.
2. **Verificação:** recalcula os hashes e compara com a referência salva, informando o que mudou.

Cada verificação é registrada em um **log** com data, horário e resultado.

---

## Requisitos

- Linux
- Python 3._X_ ou superior
- Bash

---

## Instalação

```bash
git clone https://github.com/HeloSilvaC/guardiao-integridade.git
cd guardiao-integridade
chmod +x guardiao guardiao.sh
```

---

## Uso

### Pela aplicação diretamente

```bash
# Cria a referência inicial
./guardiao cadastrar <diretorio>

# Verifica a integridade em relação à referência
./guardiao verificar <diretorio>
```

### Pelo Shell Script

```bash
./guardiao.sh <diretorio>
```

O script executa a verificação, interpreta o código de saída e exibe a mensagem correspondente.

### Exemplo de saída

```
Verificação concluída.

Arquivos analisados: 10
Arquivos modificados: 1
Arquivos novos: 2
Arquivos removidos: 1

Alterações detectadas!
```

---

## Códigos de saída

| Código | Significado |
|:---:|---|
| `0` | Execução concluída **sem alterações** |
| `1` | **Alterações detectadas** (arquivos modificados, novos ou removidos) |
| `2` | **Erro** durante a execução |

> Esses códigos ficam definidos em `src/codigos.py` e são usados de forma consistente pela aplicação e pelo `guardiao.sh`.

---

## Estrutura do projeto

```
guardiao-integridade/
├── guardiao            # Ponto de entrada (CLI)
├── guardiao.sh         # Script de automação
├── src/
│   ├── __init__.py
│   ├── varredura.py    # Percorre o diretório recursivamente
│   ├── hashing.py      # Calcula o SHA-256 dos arquivos
│   ├── referencia.py   # Salva e carrega a referência
│   ├── comparacao.py   # Compara o estado atual com a referência
│   ├── relatorio.py    # Formata e exibe os resultados
│   ├── log.py          # Registra as execuções
│   └── codigos.py      # Códigos de saída
├── testes/
│   └── arquivos/       # Diretório de testes
└── README.md
```

---

## Armazenamento

| Item | Local | Formato |
|---|---|---|
| Referência | _a definir_ | _a definir (JSON? CSV?)_ |
| Log | _a definir_ | _a definir_ |

---

## Tratamento de erros

| Situação | Comportamento |
|---|---|
| Diretório inexistente | _a definir_ |
| Arquivo sem permissão de leitura | _a definir_ |
| Referência não encontrada ao verificar | _a definir_ |
| Argumentos inválidos | _a definir_ |

---

## Testes

Os testes usam o diretório `testes/arquivos/`, sem tocar em arquivos do sistema.

```bash
# 1. Cadastrar a referência
./guardiao cadastrar testes/arquivos

# 2. Modificar um arquivo
echo "alteração" >> testes/arquivos/<arquivo>

# 3. Criar um arquivo novo
touch testes/arquivos/novo.txt

# 4. Remover um arquivo
rm testes/arquivos/<arquivo>

# 5. Verificar
./guardiao.sh testes/arquivos

# 6. Testar um erro
./guardiao verificar pasta_que_nao_existe
```

---

## Limitações de segurança

O hash detecta mudanças no **conteúdo** dos arquivos, mas **não protege a própria referência**: se alguém alterar o arquivo de referência, o Guardião passa a confiar em dados falsos.

_Discussão e medidas adotadas pela dupla: a definir._

---

## Progresso

- [ ] **Parte 1:** varredura recursiva + cálculo de hash
- [ ] **Parte 2:** `cadastrar` (salvar a referência)
- [ ] **Parte 3:** `verificar` (comparação + relatório)
- [ ] **Parte 4:** códigos de saída, log, tratamento de erros, `guardiao.sh`
- [ ] **Parte 5:** testes finais e ensaio da apresentação
