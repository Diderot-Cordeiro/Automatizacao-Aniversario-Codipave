import pandas as pd

arquivo = "dados/aniversariantes junho.xls"

dados = pd.read_excel(
    arquivo,
    sheet_name=0,
    header=None
)

clientes = []
clientes_ignorados = 0

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