import csv
from exceptions import NoDataForExportError

def export_to_csv(data, filename: str):

    if not data:
        raise NoDataForExportError("No data provided")

    # Permite passar um único StockResponse
    if hasattr(data, "model_dump"):
        data = [data.model_dump()]

    # Permite passar lista de StockResponse
    elif hasattr(data[0], "model_dump"):
        data = [item.model_dump() for item in data]

    field_names = data[0].keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)

        writer.writeheader()
        writer.writerows(data)

#TODO: Exportar para Excel