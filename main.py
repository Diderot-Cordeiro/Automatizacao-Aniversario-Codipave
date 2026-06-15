import pandas as pd

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