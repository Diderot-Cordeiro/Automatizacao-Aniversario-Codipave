import pandas as pd
from datetime import datetime
import os

from config.config import(
    MENSAGEM,
    CAMINHO_IMAGEM,
    MODO_TESTE,
    LIMITE_ENVIO
)

arquivo = "dados/aniversariantes junho.xls"

dados = pd.read_excel(
    arquivo,
    sheet_name=0,
    header=None
)

clientes = []
clientes_ignorados = 0

telefone_invalido = 0

for indice, linha in dados.iterrows():
    valor = str(linha[0]).strip()
    if(
        len(valor) >= 9
        and valor[:6].isdigit()
        and valor[6:9] == " - "
    ):
        codigo = valor[:6]
        nome = valor[9:]
        celular = str(linha[7]).strip()
        celular = (
            celular
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "")
            .replace("-", "")
        )
        if(
            celular == "nan"
            or not celular.isdigit()
            or len(celular) < 9
        ):
            telefone_invalido +=1

            continue
        nascimento = str(linha[9]).strip()
        if "(FALECIDO)" not in nome.upper():
            clientes.append(
                {
                    "Codigo": codigo,
                    "nome": nome,
                    "celular": celular,
                    "nascimento": nascimento
                }
            )
        else:
            clientes_ignorados +=1 
print(f"\nClientes encontrados: {len(clientes)}")
print("\nPrimeiros registros:\n")
for cliente in clientes[:5]:
    print(cliente)
print(
    f"\nClientes ignorados (falecidos): {clientes_ignorados}"
)
print(
    f"Clientes ignorados (telefone inváido): {telefone_invalido}"
)

clientes_df = pd.DataFrame(clientes)
clientes_df.to_csv(
    "saida/clientes_limpo.csv",
    index=False,
    encoding="utf-8-sig"
)

dia_hoje = datetime.now().strftime("%d/%m")
clientes_hoje = []
for cliente in clientes:
    if cliente["nascimento"][:5] == dia_hoje:
        clientes_hoje.append(cliente)
print(
    f"\nAniversariantes de hoje: {len(clientes_hoje)}"
)
for cliente in clientes_hoje[:5]:
    print(
        cliente["nome"]
    )

fila_df = pd.DataFrame(clientes_hoje)
fila_df.to_csv(
    "saida/fila_envio.csv",
    index=False,
    encoding="utf-8-sig"
)
print(
    "\nFila de envio criada."
)

if not os.path.exists(
    "saida\log_envios.csv"
):
    log_df = pd.DataFrame(
        columns=[
            "codigo",
            "data_envio",
            "status"
        ]
    )
    log_df.to_csv(
        "saida\log_envios.csv",
        index=False,
        encoding="utf-8-sig"
    )
    print(
        "\nLog criado."
    )
else:
    print(
        "\nLog já existente"
    )

print("\nConfig carregada:")
print(f"\nModo teste: {MODO_TESTE} | Limite: {LIMITE_ENVIO}")

print("\nPrévia das mensagens:\n")
if MODO_TESTE:
    clientes_envio = clientes_hoje[:LIMITE_ENVIO]
else:
    clientes_envio = clientes_hoje
for cliente in clientes_envio:
    primeiro_nome = (
        cliente["nome"]
        .split()[0]
        .title()
    )
    mensagem = MENSAGEM.format(
        primeiro_nome=primeiro_nome
    )
    print("----------------")
    print(mensagem)

    status = {
        "codigo": str(cliente["Codigo"]).zfill(6),
        "data_envio": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "status": "pendente",
        "nome": cliente["nome"],
        "celular": cliente["celular"]
}

    if os.path.exists("saida/log_envios.csv"):
        log_df = pd.read_csv(
        "saida/log_envios.csv"
    )
else:
    log_df = pd.DataFrame(
        columns=[
            "codigo",
            "data_envio",
            "status",
            "nome",
            "celular"
        ]
    )
    novo_status = pd.DataFrame(
        [status]
    )
    log_df = pd.concat(
        [log_df, novo_status],
        ignore_index=True
    )
    log_df.to_csv(
        "saida/log_envios.csv",
        index=False,
        encoding="utf-8-sig"
    )