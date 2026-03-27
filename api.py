from datetime import datetime
from fastapi import FastAPI, Response, status
from fastapi.responses import StreamingResponse
from ai import summarize_documents_to_events, generate_report
from chunking import batch_chunks, chunk
from exceptions import NoDataForExportError
from scraping import search_asset, search_pdfs_asset
from files import export_to_csv, read_pdf

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

        print("Lendo PDFs")
        all_summaries = []
        
        for url in pdfs_urls:
            if url != pdfs_urls[4]: # -> para debug manual, mais rápido
                continue
            
            print(f"URL: {url}")
            doc = read_pdf(url)

            print("Chunkeando os documentos")
            chunks = chunk(doc)
            print("Batcheando os documentos")

            for i, batch in enumerate(batch_chunks(chunks)):
                print(f"Batch {i}")
                # Chamada da IA
                summary = summarize_documents_to_events(batch)
                print(f"RESUMO {i}: {summary}") # PARA DEBUG

                all_summaries.append(summary)

        print("Resumindo documentos")
        summarize = summarize_documents_to_events(all_summaries)

        print("Gerando relatório final")
        final_report = generate_report(content=summarize) # type: ignore
        
        response.status_code = status.HTTP_200_OK
        return {"urls": pdfs_urls, "summarize": summarize, "report": final_report} # As urls são somente para testes, por enquanto
    
    except ValueError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

#TODO: Rota POST que recebe um JSON com múltiplos tickers.
#TODO: Rota POST que recebe um CSV e tem a capacidade de atualizar dados, criar novos registros de variação de preços etc..
#TODO: Rota padrão que busca o ticker mais próximo do que o usuário digitou, caso o ticker exato não seja encontrado.