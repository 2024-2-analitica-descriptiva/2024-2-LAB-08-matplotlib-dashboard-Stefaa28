# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""


def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
import os
import pandas as pd
import matplotlib.pyplot as plt
import shutil

# Crear la carpeta 'docs' en la raíz del repo
output_dir = os.path.join("..", "docs")  
os.makedirs(output_dir, exist_ok=True)

# Carga los datos del archivo CSV.
def load_data():
        df = pd.read_csv("files/input/shipping-data.csv")
        return df

 # Crea el gráfico de envíos por bloque del almacén.
def create_visual_for_shipping_per_warehouse(df):
        df = df.copy()
        plt.figure()
        counts = df["Warehouse_block"].value_counts()
        counts.plot.bar(
            title="Shipping per Warehouse",
            xlabel="Warehouse Block",
            ylabel="Record Count",
            color="tab:blue",
            fontsize=8,
        )
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.savefig("docs/shipping_per_warehouse.png")
    
# Crea el gráfico de modo de envío.
def create_visual_for_mode_of_shipment(df):
        df = df.copy()
        plt.figure()
        counts = df["Mode_of_Shipment"].value_counts()
        counts.plot.pie(
            title="Mode of Shipment",
            wedgeprops=dict(width=0.35),
            ylabel="",
            colors=["tab:blue", "tab:orange", "tab:green"],
        )
        plt.savefig("docs/mode_of_shipment.png")
        
 # Crea el gráfico de calificación promedio del cliente.
def create_visual_for_average_customer_rating(df):
        df = df.copy()
        plt.figure()
        df = (
            df[["Mode_of_Shipment", "Customer_rating"]]
            .groupby("Mode_of_Shipment")
            .describe()
        )
        df.columns = df.columns.droplevel()
        df = df[["mean", "min", "max"]]

        plt.barh(
            y=df.index.values,
            width=df["max"].values - 1,
            left=df["min"].values,
            height=0.9,
            color="lightgray",
            alpha=0.8,
        )
        colors = [
            "tab:green" if value >= 3.0 else "tab:orange" for value in df["mean"]
        ]
        plt.barh(
            y=df.index.values,
            width=df["mean"].values - 1,
            left=df["min"].values,
            color=colors,
            height=0.5,
            alpha=1.0,
        )
        plt.title("Average Customer Rating")
        plt.gca().spines["left"].set_color("gray")
        plt.gca().spines["bottom"].set_color("gray")
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.savefig("docs/average_customer_rating.png")

# Crea el gráfico de distribución de peso.
def create_visual_for_weight_distribution(df):
        df= df.copy()
        plt.figure()
        df["Weight_in_gms"].plot.hist(
            title="Shipping Weight Distribution",
            color="tab:orange",
            edgecolor="white",
        )
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.savefig("docs/weight_distribution.png")


# Cargar los datos
df = load_data()

# Crear visualizaciones
create_visual_for_shipping_per_warehouse(df)
create_visual_for_mode_of_shipment(df)
create_visual_for_average_customer_rating(df)
create_visual_for_weight_distribution(df)

# Crear archivo HTML
with open("docs/index.html", "w") as f:
        f.write(
            """
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Shipping Dashboard</title>
                </head>
                <body>
                    <h1>Shipping Dashboard Example</h1>
                    <div style="width:45%;float:left;">
                        <img src="shipping_per_warehouse.png" alt="Fig 1">
                        <img src="mode_of_shipment.png" alt="Fig 2">
                    </div>
                    <div style="width:45%;float:left;">
                        <img src="average_customer_rating.png" alt="Fig 3">
                        <img src="weight_distribution.png" alt="Fig 4">
                    </div>
                </body>
            </html>
            """
        )

# Lista de archivos a mover
files_to_move = [
    "shipping_per_warehouse.png",
    "mode_of_shipment.png",
    "average_customer_rating.png",
    "weight_distribution.png",
    "index.html",
]

# Mover los archivos a la carpeta 'docs'
for file_name in files_to_move:
    if os.path.exists(file_name):  # Verifica que el archivo exista
        shutil.move(file_name, os.path.join(output_dir, file_name))  # Mueve el archivo

print(f"Todos los archivos se han movido a la carpeta '{output_dir}'.")