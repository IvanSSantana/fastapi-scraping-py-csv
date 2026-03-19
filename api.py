import csv
from datetime import datetime
import io
from fastapi import FastAPI, Response, status
from fastapi.responses import FileResponse, StreamingResponse
from ai import generate_report, summarize_documents
from exceptions import NoDataForExportError
from scraping import search_asset, search_pdfs_asset
from files import export_to_csv, read_pdf, extract_relevant_lines
from token_count import TokenCount

app = FastAPI()

#TODO: Implementar autenticação e autorização para proteger as rotas de acesso aos dados dos ativos.

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

        output = export_to_csv(stock)

        response.status_code = status.HTTP_200_OK
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={ticker}{datetime.now().month}{datetime.now().year}.csv"
            }
        )
    except NoDataForExportError as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}
    
@app.get("/api/v1/report/{ticker}")
async def get_report(ticker: str, response: Response):
    #TODO: Salvar análise já salva de imagens do mês e redefinir banco ao virar mês
    try:
        print("Procurando relatórios")
        pdfs_urls = search_pdfs_asset(ticker)

        pdfs_raw_content = []
        print("Lendo PDFs")
        
        for url in pdfs_urls:
            pdfs_raw_content.append(read_pdf(url))
        
        print("Processando chunks localmente")

        print("Resumindo documentos")
        summarize = summarize_documents(pdfs_raw_content[1])
        
        response.status_code = status.HTTP_200_OK
        return {"urls": pdfs_urls, "content": pdfs_raw_content, "summarize": summarize} # as urls são somente para testes, por enquanto
    
    except ValueError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

#TODO: Rota POST que recebe um JSON com múltiplos tickers.
#TODO: Rota POST que recebe um CSV e tem a capacidade de atualizar dados, criar novos registros de variação de preços etc..
#TODO: Rota padrão que busca o ticker mais próximo do que o usuário digitou, caso o ticker exato não seja encontrado.