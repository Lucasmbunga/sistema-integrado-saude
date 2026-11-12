# Sistema Integrado de Informação - Direção Provincial da Saúde do Uíge

---

## Sobre o Projeto

Este projeto foi desenvolvido no âmbito da disciplina de **Linguagem de Programação V (Python)**, do 3.º ano do curso de **Engenharia Informática**, sob orientação do docente **Atungulu Kabakaba**.

O sistema responde ao desafio proposto pela **Direção Provincial da Saúde do Uíge**, visando resolver problemas de fragmentação de informação através de uma solução centralizada que promove a **interoperabilidade** entre hospitais, centros de saúde e postos médicos da província, permitindo a consulta unificada do histórico clínico dos utentes.

---

## Funcionalidades Principais

O sistema funciona via consola (CLI) com arquitetura orientada a objetos (POO) e oferece operações completas de **CRUD** (*Create, Read, Update, Delete*) para todas as entidades:

* **Gestão de Unidades de Saúde:** Registo, listagem, atualização e eliminação de hospitais e centros de saúde da província (com proteção de integridade referencial).
* **Gestão de Utentes / Pacientes:** Cadastro único de pacientes, pesquisa por ID ou nome, atualização de dados demográficos e remoção controlada.
* **Histórico Clínico Partilhado (Interoperabilidade):** Registo de atendimentos, diagnósticos e prescrições médicas associados a um utente e a uma unidade específica, acessíveis a partir de qualquer ponto da rede.
* **Persistência de Dados Automática:** Armazenamento local em formato `JSON` (`dados_saude_uige.json`), garantindo que nenhuma informação se perde após o encerramento da aplicação.
* **Validação e Tratamento de Erros:** Verificação de formatos de data (`DD/MM/AAAA`), prevenção de campos obrigatórios vazios e recuperação automática caso o ficheiro de dados esteja corrompido.

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3.8+
* **Bibliotecas Nativas:** `json` (persistência de dados) e `os` (gestão de ficheiros do sistema). *Não requer instalação de pacotes externos.*

---

## Estrutura do Projeto

```text
sistema-integrado-saude         #Pasta raíz
   ├── sistema_saude.py         # Código-fonte principal com as classes e menus CLI
   ├── dados_saude_uige.json    # Base de dados local gerada automaticamente na 1.ª execução
   └── README.md                # Documentação do repositório
```

---

## Como Executar o Projeto

### Pré-requisitos
Certifique-se de que tem o **Python 3** instalado na sua máquina:
```bash
python --version
```

### Passo a Passo
1. Clone este repositório para o seu computador:
   ```bash
   git clone https://github.com/seu-utilizador/sistema-integrado-saude-uige.git
   ```
2. Aceda à pasta do projeto:
   ```bash
   cd sistema-integrado-saude-uige
   ```
3. Execute o script principal:
   ```bash
   python sistema_saude.py
   ```

---

## Dados Iniciais de Teste

Na primeira execução, o sistema gera automaticamente o ficheiro `dados_saude_uige.json` com registos iniciais para facilitar os testes:
* **Unidades:** `HGU01` (Hospital Geral do Uíge) e `CS02` (Centro de Saúde do Mangue).
* **Utente:** `P001` (Mário Kanjila).
* **Registo Clínico:** `R001` associado ao utente `P001`.

---

## Autor e Contexto Académico

* **Curso:** Engenharia Informática (3.º Ano)
* **Disciplina:** Linguagem de Programação V (Python)
* **Docente:** Atungulu Kabakaba
* **Questão Atribuída:** Questão 3 — Sistema Integrado de Informação