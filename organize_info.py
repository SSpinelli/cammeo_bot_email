import csv
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime


inputed_date = input(
    "Escolha a data de início do seu formulário: (AAAA/MM/DD)"
)


def create_comments(dict_by_sector):
    for sector, data in dict_by_sector.items():
        with open(f"comments/{sector}.txt", "w") as file:
            for row in data:
                if row["comentario_adicional"] != "":
                    file.write(row["comentario_adicional"] + "\n")


def create_charts(dict_by_sector):
    for sector in dict_by_sector:
        sector_data = dict_by_sector[sector]
        with PdfPages(f"reports/{sector}.pdf") as pdf:
            for field in [
                "interesse_atendente",
                "clareza_atendente",
                "tempo_de_espera",
                "conhecimento_equipe",
                "cortesia_atendente",
            ]:
                values = [data[field] for data in sector_data]
                if values:
                    sns.countplot(x=values)
                    plt.title(f"{field} in {sector}")
                    plt.xlabel(field)
                    plt.ylabel("Count")
                    plt.tight_layout()
                    pdf.savefig()
                    plt.clf()


def organize_csv_file():
    with open("./formulario-atual/form-jan-2023.csv") as file:
        document = csv.reader(file, delimiter=",", quotechar='"')

        _, *data = document

        dict_data = []

        for new_input in data:
            if new_input[0] != "":
                date_obj = datetime.strptime(new_input[0], "%d/%m/%Y %H:%M:%S")
                date_parsed = date_obj.strftime("%Y/%m/%d")

                if date_parsed > inputed_date:
                    dict_data.append(
                        {
                            "data_hora": new_input[0],
                            "setores": new_input[1],
                            "interesse_atendente": new_input[2],
                            "clareza_atendente": new_input[3],
                            "tempo_de_espera": new_input[4],
                            "conhecimento_equipe": new_input[5],
                            "cortesia_atendente": new_input[6],
                            "comentario_adicional": new_input[7],
                            "identificacao_cliente": new_input[9],
                        }
                    )

        dict_by_sector = {
            "Recepção": [],
            "Inscrição": [],
            "Cobrança": [],
            "Fiscalização": [],
            "Administração": [],
            "Secretaria": [],
            "Ética": [],
            "Comunicação": [],
            "Contabilidade": [],
            "Delegacia Petrolina": [],
            "Delegacia Caruaru": [],
            "Delegacia Serra Talhada": [],
            "Ouvidoria": [],
            "Procuradoria Jurídica": [],
            "Whatsapp": [],
        }

        for data in dict_data:
            sectors = data["setores"].split(",")
            for i in range(len(sectors)):
                dict_by_sector[sectors[i].strip()].append(data)

    print(dict_by_sector)
    return dict_by_sector


create_charts(organize_csv_file())
create_comments(organize_csv_file())
