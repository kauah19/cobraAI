# Sistema de Cobrança com Supabase e WhatsApp

Este é um **sistema de gerenciamento e cobrança de dívidas** em Python, utilizando **Supabase** como banco de dados e a API da **GROQ IA** para gerar mensagens automáticas. Também envia cobranças via **WhatsApp** usando a biblioteca `pywhatkit`.

---

## Funcionalidades

- Adicionar novos devedores (nome, valor, motivo e WhatsApp).  
- Visualizar lista completa de devedores.  
- Gerar mensagens automáticas de cobrança via GROQ IA.  
- Enviar mensagens de cobrança diretamente pelo WhatsApp.  
- Quitar dívidas atualizando o status no banco de dados.  
- Exportar relatório de dívidas em formato CSV.

---

## Tecnologias

- Python 3.x  
- Supabase (PostgreSQL + API REST)  
- GROQ IA (geração de mensagens automáticas)  
- pywhatkit (envio de mensagens via WhatsApp Web)  
- python-dotenv (variáveis de ambiente)  
- requests (requisições HTTP)

---

## Requisitos

- Python 3 instalado  
- Navegador logado no WhatsApp Web  
- Contas e chaves de API:  
  - **Supabase** (`SUPABASE_URL` e `SUPABASE_KEY`)  
  - **GROQ IA** (`GROQ_API_KEY`)  

---

## Instalação

1. Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>
Instale as dependências:

bash
Copiar código
pip install supabase requests pywhatkit python-dotenv
Crie um arquivo .env na raiz do projeto:

env
Copiar código
GROQ_API_KEY=sua_chave_da_groq
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase
Configure o .gitignore:

bash
Copiar código
.env
__pycache__/
*.pyc
Uso
Execute o script:

bash
Copiar código
python nome_do_script.py
Escolha a ação desejada no menu:

Adicionar devedor

Ver lista de devedores

Cobrar devedor (mensagem automática + WhatsApp)

Quitar dívida

Exportar relatório (.csv)

Sair

Observações
O envio de mensagens via WhatsApp requer WhatsApp Web logado no navegador padrão.

Mensagens automáticas são geradas pela GROQ IA e podem ter tom educado ou humorístico.

O relatório CSV pode ser usado para análises ou backups.

Exemplo de Uso
Adicionar devedor:

yaml
Copiar código
Digite o número que corresponde a sua necessidade: 1
Nome da pessoa que te deve: João
Valor da dívida: 50
Motivo da dívida: Pizza
Número do WhatsApp do devedor: +5511999999999
Sua dívida foi listada!
Cobrar devedor:

bash
Copiar código
Digite o número que corresponde a sua necessidade: 3
Devedores pendentes:
1 - João deve R$50 (Pizza)
Digite o nome do devedor que deseja cobrar: João

Mensagem gerada:
"Ei João, lembra daquela pizza? Tá na hora de quitar a dívida de R$50!"
Mensagem enviada para João (+5511999999999) via WhatsApp.