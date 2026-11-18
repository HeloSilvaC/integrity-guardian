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
- Python 3.8 ou superior (só biblioteca padrão, não precisa instalar nada)
- Bash

> No Windows, rode pelo **WSL** (`wsl --install` no PowerShell como administrador). Se os arquivos foram editados no Windows, converta as quebras de linha antes de rodar: `sed -i 's/\r$//' guardiao guardiao.sh testes/demo.sh src/*.py`

---

## Instalação

```bash
git clone https://github.com/HeloSilvaC/integrity-guardian.git
cd integrity-guardian
chmod +x guardiao guardiao.sh testes/demo.sh
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

Para recadastrar por cima de uma referência que já existe:

```bash
./guardiao cadastrar <diretorio> --forcar
```

### Pelo Shell Script

```bash
# Verifica
./guardiao.sh <diretorio>
./guardiao.sh verificar <diretorio>     # mesma coisa, escrito por extenso

# Cadastra
./guardiao.sh cadastrar <diretorio>

# Recadastra por cima da referência existente
./guardiao.sh cadastrar <diretorio> --forcar
```

O script chama o `guardiao`, interpreta o código de saída e exibe a mensagem correspondente.

### Exemplo de saída

```
Verificação concluída.

Arquivos analisados: 19
Arquivos modificados: 2
Arquivos novos: 1
Arquivos removidos: 1

Modificados:
  ~ documentos/notas.txt
      tamanho: 24 -> 44 bytes
      modificado em: 17/11/2026 14:51:26 -> 17/11/2026 14:51:28
      @@ -3 +3,2 @@
       linha 3
      +nova linha no final
  ~ dados/binario.bin
      tamanho: 2048 -> 2050 bytes
      modificado em: 17/11/2026 14:51:26 -> 17/11/2026 14:51:28
      (arquivo binário ou grande, não dá para mostrar o conteúdo)

Novos:
  + novo.txt

Removidos:
  - vazio.txt

Alterações detectadas!
```

### Vendo o que mudou

Para cada arquivo **modificado**, o relatório mostra:

- o **tamanho** antes e agora;
- a **data da última modificação** antes e agora;
- para arquivos de **texto** (até 1 MB), as **linhas que mudaram**: `-` é a linha que saiu, `+` é a que entrou, e as linhas com espaço são só contexto. O `@@ -3 +3,2 @@` diz em que linha fica a mudança (no arquivo antigo e no novo).

Para conseguir mostrar as linhas, o `cadastrar` guarda uma cópia dos arquivos de texto em `.guardiao/copias/`. Arquivos binários ou grandes mostram só o tamanho e a data.

> Um link simbólico aparece como modificado quando o arquivo para onde ele aponta muda, porque o hash é calculado sobre o conteúdo do destino.

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
integrity-guardian/
├── guardiao            # Ponto de entrada (CLI)
├── guardiao.sh         # Script de automação
├── src/
│   ├── __init__.py
│   ├── varredura.py    # Percorre o diretório recursivamente
│   ├── hashing.py      # Calcula o SHA-256 dos arquivos
│   ├── referencia.py   # Salva e carrega a referência
│   ├── comparacao.py   # Compara o estado atual com a referência
│   ├── relatorio.py    # Formata e exibe os resultados
│   ├── diferencas.py   # Mostra o que mudou em cada arquivo modificado
│   ├── log.py          # Registra as execuções
│   └── codigos.py      # Códigos de saída
├── testes/
│   ├── demo.sh         # Roteiro da demonstração
│   └── arquivos/       # Diretório de testes
└── README.md
```

---

## Armazenamento

| Item | Local | Formato |
|---|---|---|
| Referência | `.guardiao/referencia.json` (na pasta do projeto) | JSON com o diretório, a data do cadastro e, para cada arquivo, o caminho relativo, o nome, o hash, o tamanho e a data de modificação |
| Hash da referência | `.guardiao/referencia.json.sha256` | Texto com o SHA-256 do `referencia.json` |
| Cópias dos arquivos de texto | `.guardiao/copias/` | Cópia dos arquivos de texto (até 1 MB), usada só para mostrar as linhas que mudaram |
| Log | `.guardiao/guardiao.log` | Uma linha por execução: `[data hora] comando diretorio -> resultado` |

A pasta `.guardiao/` é ignorada na varredura, então dá para monitorar até a pasta do próprio projeto.

Exemplo de referência:

```json
{
  "diretorio": "/home/aluno/guardiao/testes/arquivos",
  "data": "17/11/2026 14:47:53",
  "arquivos": {
    "documentos/notas.txt": {
      "nome": "notas.txt",
      "hash": "9f86d081884c7d65...",
      "tamanho": 24,
      "modificado_em": "17/11/2026 14:47:50"
    }
  }
}
```

Exemplo de log:

```
[17/11/2026 14:47:53] cadastrar testes/arquivos -> referência cadastrada (19 arquivos)
[17/11/2026 14:47:53] verificar testes/arquivos -> ALTERAÇÕES DETECTADAS: 1 modificado(s), 1 novo(s), 1 removido(s)
[17/11/2026 14:47:54] verificar nao_existe -> ERRO: diretório 'nao_existe' não encontrado.
```

---

## Tratamento de erros

| Situação | Comportamento |
|---|---|
| Diretório inexistente | Mensagem de erro, código `2` |
| Pasta sem permissão de leitura | No `verificar`: os arquivos dela aparecem como **inacessíveis** (não contam como removidos); uma pasta nova sem permissão aparece como `pasta/`. Mesmos códigos da linha abaixo. No `cadastrar`: a referência **não** é salva e o código é `2` |
| Arquivo sem permissão de leitura (ou link quebrado) | No `verificar`: aparece no relatório como **inacessível** (não conta como removido). Se só tiver isso, código `2`; se também houver alterações, código `1`. No `cadastrar`: a referência **não** é salva e o código é `2` |
| Referência não encontrada ao verificar | Pede para rodar `cadastrar` antes, código `2` |
| Referência já existe ao cadastrar | Recusa sobrescrever sem `--forcar`, código `2` |
| Referência cadastrada para outro diretório | Mensagem de erro, código `2` |
| Referência alterada ou corrompida | Mensagem de erro, código `2` (ver Limitações de segurança) |
| Argumentos faltando ou comando inválido | Mostra o uso, código `2` |
| Qualquer outra falha inesperada | Mensagem de erro, código `2` |

Todos os erros também são registrados no log.

---

## Testes

Os testes usam o diretório `testes/arquivos/`, sem tocar em arquivos do sistema.

> **Rode como usuário comum, não como root nem com `sudo`.** O root consegue ler qualquer arquivo, então os testes de "sem permissão" (`chmod 000`) não geram erro nenhum.

### Demonstração automática

O `testes/demo.sh` copia `testes/arquivos/` para `/tmp/guardiao-demo` e roda o guardião de verdade nessa cópia, mostrando cada comando e o código de saída.

```bash
./testes/demo.sh            # para entre as etapas (Enter para seguir)
./testes/demo.sh --direto   # roda tudo de uma vez
```

| Etapa | O que faz | Código esperado |
|---|---|:---:|
| 1 | Cadastra a referência inicial | `0` |
| 2 | Verifica sem mudar nada | `0` |
| 3 | Modifica `documentos/notas.txt` | `1` |
| 4 | Cria `novo.txt` | `1` |
| 5 | Remove `vazio.txt` | `1` |
| 6 | Verifica um diretório que não existe | `2` |
| 7 | Recadastra e tira a permissão de `dados/vendas.csv` | `0` e `2` |
| 8 | Altera a referência sem recalcular o hash dela | `2` |
| 9 | Mostra o log | |

Depois de rodar, dá para conferir os arquivos em `/tmp/guardiao-demo` (no Windows: `\\wsl$\Ubuntu\tmp\guardiao-demo`).

> O demo recadastra com `--forcar`, então substitui a referência que já existir em `.guardiao/`. Não use uma pasta do Windows (`/mnt/c/...`) como diretório de teste: lá o `chmod 000` não tem efeito.

### Passo a passo manual

```bash
# 0. Fazer uma cópia para não estragar os arquivos de teste
cp -r testes/arquivos /tmp/demo

# 1. Cadastrar a referência (--forcar caso já exista uma)
./guardiao.sh cadastrar /tmp/demo --forcar

# 2. Verificar sem mudar nada (código 0)
./guardiao.sh /tmp/demo

# 3. Modificar, criar e remover um arquivo
echo "alteração" >> /tmp/demo/documentos/notas.txt
touch /tmp/demo/novo.txt
rm /tmp/demo/vazio.txt

# 4. Verificar de novo (código 1)
./guardiao.sh /tmp/demo

# 5. Testar erros (código 2)
./guardiao verificar pasta_que_nao_existe
./guardiao cadastrar /tmp/demo          # já existe referência (sem --forcar)
chmod 000 /tmp/demo/dados/vendas.csv && ./guardiao verificar /tmp/demo

# 6. Ver o log
cat .guardiao/guardiao.log
```

---

## Limitações de segurança

O hash detecta mudanças no **conteúdo** dos arquivos, mas **não protege a própria referência**: se alguém alterar o arquivo de referência, o Guardião passa a confiar em dados falsos.

Medidas que adotamos:

1. **Referência somente leitura:** depois do cadastro, `referencia.json` fica com permissão `444`.
2. **Hash da referência:** no cadastro salvamos o SHA-256 da própria referência em `referencia.json.sha256`. Antes de verificar, o Guardião recalcula e compara; se for diferente (ou o arquivo `.sha256` sumir), ele se recusa a continuar.
3. **Não sobrescreve sem querer:** `cadastrar` só substitui uma referência existente com `--forcar`.

As cópias em `.guardiao/copias/` servem **só para mostrar** as diferenças. Quem decide se um arquivo mudou é sempre o hash da referência protegida.

Mesmo assim, isso **não é proteção completa**: quem tiver permissão de escrita na pasta pode alterar a referência *e* recalcular o `.sha256`. Isso só pega alterações acidentais ou feitas por alguém que não conhece o Guardião. Para uma proteção de verdade seria preciso, por exemplo, guardar a referência em outro lugar (mídia somente leitura, outra máquina), deixar ela com dono `root`, ou assinar com uma chave que o atacante não tenha.

---

## Progresso

- [x] **Parte 1:** varredura recursiva + cálculo de hash
- [x] **Parte 2:** `cadastrar` (salvar a referência)
- [x] **Parte 3:** `verificar` (comparação + relatório)
- [x] **Parte 4:** códigos de saída, log, tratamento de erros, `guardiao.sh`
- [ ] **Parte 5:** testes finais e ensaio da apresentação
  - [x] pasta sem permissão aparece como inacessível (não como removida)
  - [x] `guardiao.sh` aceita `--forcar`
  - [x] roteiro da demonstração (`testes/demo.sh`)
  - [ ] ensaio da apresentação