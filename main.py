import pandas as pd

arquivo = "dados/aniversariantes junho.xls"

dados = pd.read_excel(
    arquivo,
    sheet_name=0,
    header=None
)

print("\nProcurando clientes...\n")

for indice, linha in dados.iterrows():
    valor = str(linha[0]).strip()
    if(
        len(valor) >= 9
        and valor[:6].isdigit()
        and valor[6:9] == " - "
    ):
        codigo = valor[:6]
        nome = valor[9:]
        print(
            f"Código: {codigo}"
        )
        print(
            f"Nome: {nome}"
        )
        print("-" * 40)