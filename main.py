from supabase import create_client
import requests
import pywhatkit as kit
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "llama-3.3-70b-versatile",  # modelo excelente e gratuito
    "messages": [
        {"role": "user", "content": "Gere uma mensagem educada de cobrança para João que me deve 50 reais."}
    ]
}

res = requests.post(url, headers=headers, json=data)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
#resposta = supabase.table("devedores").select("*").execute()
#print(resposta.data)

#MENU PRINCIPAL
print("1 - Adicionar devedor")
print("2 - Ver lista de devedores")
print("3 - Cobrar devedor")
print("4 - Quitar dívida")
print("5 - Exportar relatório (.csv)")
print("6 - Sair")

u = int(input("Digite o número que corresponde a sua necessidade:"))

#ADICIONAR DEVEDOR
if u == 1:
    n = str(input("Nome da pessoa que te deve: "))
    v = float(input("Valor da dívida: "))
    m = str(input("Motivo da dívida: "))
    numero = input("Número do whatsapp do devedor (ex: +5511912345678): ").strip()
    data_hoje = datetime.now().isoformat()

    supabase.table("contatos").insert({
        "nome": n,
        "valor": v,
        "motivo": m,
        "whatsapp": numero,
        "pago": False,
        "data": data_hoje
    }).execute()
    
    print("Sua divida foi listada!")

#VER LISTA DE DEVEDORES
elif u == 2:
    resposta = supabase.table("contatos").select("*").order("id", desc=False).execute()

    if not resposta.data:
        print("Nenhuma dívida cadastrada.")
    else:
        print("\nLista de dívidas:\n")
        for item in resposta.data:
            status = "Pago" if item.get("pago") else "Pendente"
            print(f"{item['id']} - {item['nome']} deve R${item['valor']} ({item['motivo']}) - {status}")

#COBRAR DEVEDOR
elif u == 3:
    
    #BUSCAR DEVEDORES NÃO PAGOS
    resposta = supabase.table("contatos").select("*").eq("pago", False).execute()

    if not resposta.data:
        print("Nenhum devedor pendente. Tudo quitado!!!")
    else:
        print("\nDevedores pendentes:\n")
        for item in resposta.data:
            print(f"{item['id']} - {item['nome']} deve R${item['valor']} ({item['motivo']})")

        #SELECIONAR DEVEDOR PELO NOME
        devedor_nome = input("Digite o nome do devedor que deseja cobrar: ").strip()
        devedor = next((d for d in resposta.data if d['nome'].lower() == devedor_nome.lower()), None)

        if not devedor:
            print("Devedor não encontrado.")
        else:
            #GERAR MENSAGEM AUTOMÁTICA VIA GROQ IA
            prompt = f"Gere uma mensagem bem zoeira com o motivo de cobrança para{devedor['nome']} que deve R${devedor['valor']} e não coloque 'meu nome' no final."
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}]
            }
            
            #REQUISIÇÃO À API DA GROQ
            res = requests.post(url, headers=headers, json=data)
            res_json = res.json()

            mensagem = res_json["choices"][0]["message"]["content"]

            print("\nMensagem gerada:")
            print(mensagem)

            #PEGAR O NÚMERO DO WPP DIRETAMENTE DO BANCO DE DADOS
            numero_raw = devedor.get("whatsapp", "").strip()
            if not numero_raw:
                print("Número de WhatsApp não cadastrado para esse devedor.")
            else:
                #REMOVER ESPAÇOS E CARACTERES DESNECESSÁRIOS
                numero_clean = "".join(c for c in numero_raw if c.isdigit() or c == "+")
                
                #GARANTIR PREFIXO INTERNACIONAL +55
                if numero_clean.startswith("+"):
                    numero_formatado = numero_clean
                elif numero_clean.startswith("55"):
                    numero_formatado = "+" + numero_clean
                else:
                    numero_formatado = "+55" + numero_clean

                #ENVIAR VIA PYWHATKIT (WPP WEB PRECISA ESTAR LOGADO)
                try:
                    kit.sendwhatmsg_instantly(numero_formatado, mensagem)
                    print(f"\nMensagem enviada para {devedor['nome']} ({numero_formatado}) via WhatsApp.")
                except Exception as e:
                    print("Erro ao tentar enviar pelo WhatsApp:", e)
                    print("Obs: verifique se o navegador está logado no WhatsApp web e se pywhatkit está instalado.")
            

#QUITAR DÍVIDA
elif u == 4:
    resposta = supabase.table("contatos").select("*").or_("pago.eq.false,pago.is.null").execute()

    if not resposta.data:
        print("Nenhuma dívida pendente para quitar.")
    else:
        print("Dívidas pendentes:")
        for item in resposta.data:
            print(f"{item['id']} - {item['nome']} deve R${item['valor']} ({item['motivo']})")

        try:
            id_divida = int(input("Digite o ID do devedor que deseja quitar: "))
            
            #ATUALIZAR O CAMPO "PAGO" NO BANCO
            supabase.table("contatos").update({"pago": True}).eq("id", id_divida).execute()
            print("Dívida quitada com sucesso!")
        except ValueError:
            print("ID inválido. Tente novamente.")

elif u == 5:
    import csv

    resposta = supabase.table("contatos").select("*").execute()
    with open("relatorio_dividas.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Nome", "Valor", "Motivo", "Pago", "Data"])
        for item in resposta.data:
            writer.writerow([
                item["id"],
                item["nome"],
                item["valor"],
                item["motivo"],
                "Pago" if item["pago"] else "Pendente",
                item.get("data", "")
            ])
    print("Relatório exportado como 'relatorio_dividas.csv'!")

#SAIR
elif u == 6:
    print("Saindo...")

else:
    print("Opção inválida.")
