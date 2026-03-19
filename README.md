# fastapi-scraping-py-csv
Uma API escrita em Python com FastAPI que faz um scraping do site investidor10.com.br e tem a capacidade de exportar para arquivos CSV relatórios sobre ativos.

## Planos:
1. Criar front-end React para consumo da API.
2. Integrar IA para ler relatórios gerenciais de fundos imobiliários e gerar resumos + predição.

## Atual Pipeline:
1. API recebe o ticker;
2. Scraping busca principais indicadores e os últimos relatórios;
3. Código lê bytes do PDF;
4. Função extrai os dados a partir dos bytes;
5. Conversão dos elementos do PDF para Chunks
6. LLM de Visão interpreta imagens como gráficos e tabelas;
7. IA final gera um relatório com os dados dos indicadores, relatórios e seus gráficos.
