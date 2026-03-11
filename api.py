import csv
import io

from fastapi import FastAPI, Response, status
from fastapi.responses import FileResponse, StreamingResponse
from exceptions import NoDataForExportError
from scraping import search_asset
from export import export_to_csv

app = FastAPI()

@app.get("/api/v1/{ticker}", status_code=status.HTTP_200_OK)
async def get_asset(ticker: str, response: Response):
    """Rota para buscar os dados de um ativo específico."""
    try:
        response.status_code = status.HTTP_200_OK
        return search_asset(ticker)
    except ValueError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}
    
@app.get("/api/v1/csv/{ticker}", status_code=status.HTTP_200_OK)
async def get_asset_csv(ticker: str, response: Response):
    """Rota para exportar os dados de um ativo específico em formato CSV."""
    try:
        stock = search_asset(ticker)

        output = io.StringIO() # Memória temporária para armazenar o CSV gerado

        writer = csv.DictWriter(
            output,
            fieldnames=stock.model_dump().keys()
        )

        writer.writeheader()
        writer.writerow(stock.model_dump())

        output.seek(0) # Volta para o início do arquivo para leitura para a response

        response.status_code = status.HTTP_200_OK
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={ticker}.csv"
            }
        )
    except NoDataForExportError as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}

#TODO: Rota POST que recebe um JSON com múltiplos tickers.
#TODO: Rota POST que recebe um CSV e tem a capacidade de atualizar dados, criar novos registros de variação de preços etc..
#TODO: Rota padrão que busca o ticker mais próximo do que o usuário digitou, caso o ticker exato não seja encontrado.