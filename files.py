import io
import re
import csv
from typing import List
from exceptions import NoDataForExportError
from io import BytesIO
from docling.document_converter import DocumentConverter
from responses import StockResponse

def read_pdf(pdf_url):
    """Lê PDF usando Docling e retorna documento estruturado."""

    converter = DocumentConverter()
    
    result = converter.convert(pdf_url)
    document = result.document  # objeto estruturado

    return document.export_to_text()

keywords = [
    # === EVENTOS ESTRUTURAIS (ALTA RELEVÂNCIA) ===
    "aquisição", "adquiriu", "adquirir", "incorporação", "incorporar",
    "fusão", "combinação de negócios",
    "joint venture", "parceria estratégica",
    "alienação", "venda de participação", "desinvestimento",
    "cisão", "spin-off",

    # === CAPITAL / SOCIETÁRIO ===
    "aumento de capital", "redução de capital",
    "follow-on", "oferta subsequente", "oferta pública",
    "ipo", "abertura de capital",
    "recompra de ações", "programa de recompra",
    "cancelamento de ações",
    "emissão de ações", "emissão de cotas",

    # === DÍVIDA / CAPTAÇÃO ===
    "emissão de debêntures", "debênture", "debêntures",
    "emissão de dívida", "captação de recursos",
    "alongamento da dívida", "reestruturação da dívida",
    "refinanciamento", "rolagem da dívida",
    "covenant", "quebra de covenant",

    # === OPERACIONAL (EVENTOS REAIS) ===
    "início de operação", "entrada em operação",
    "paralisação", "interrupção", "suspensão",
    "encerramento de operação",
    "expansão de capacidade", "entrada de unidade",
    "inauguração", "implantação",

    # === CONTRATOS / RECEITA ===
    "assinatura de contrato", "celebração de contrato",
    "renovação de contrato",
    "rescisão de contrato",
    "cancelamento de contrato",
    "novo contrato", "contrato relevante",

    # === FIIs (ESPECÍFICO E IMPORTANTE) ===
    "aquisição de imóvel",
    "venda de imóvel",
    "alienação de ativo",
    "compra de ativo",
    "vacância", "vacância física", "vacância financeira",
    "inadimplência", "default de inquilino",
    "rescisão de contrato de locação",
    "novo inquilino", "entrada de inquilino",
    "renovação de locação",
    "reajuste de aluguel",
    "revisional", "ação revisional",

    # === DIVIDENDOS / PROVENTOS ===
    "distribuição de dividendos",
    "pagamento de dividendos",
    "juros sobre capital próprio", "jcp",
    "rendimentos", "distribuição de rendimentos",
    "amortização de cotas",

    # === RESULTADOS FORA DO PADRÃO ===
    "evento não recorrente",
    "ganho não recorrente",
    "perda não recorrente",
    "baixa contábil", "impairment",
    "provisão", "reversão de provisão",

    # === RISCO / ALERTA (ALTA PRIORIDADE) ===
    "processo judicial relevante",
    "contingência", "passivo relevante",
    "autuação", "multa",
    "investigação",
    "risco material",
    "incerteza relevante",

    # === GOVERNANÇA ===
    "mudança na administração",
    "renúncia", "destituição",
    "eleição de diretoria",
    "substituição de executivo",

    # === GUIDANCE (SOMENTE SE COM NÚMEROS) ===
    "guidance", "projeção", "estimativa",
    "previsão", "expectativa",
    "meta", "planejamento"
]

def export_to_csv(stock : StockResponse | List[StockResponse]):
    """Exporta um objeto StockResponse para CSV"""

    if not stock:
        raise NoDataForExportError("No data provided")

    # Permite passar um único StockResponse
    if hasattr(stock, "model_dump"): # Verifica se o modelo pode ser convertido para dicionário
        stock_dumped = [stock.model_dump()] # type: ignore

    #TODO: Permitir passar múltiplos ticker para exportação de CSV
    # Permite passar lista de StockResponse
    # elif hasattr(stock[0], "model_dump"): # type: ignore
    #     stock_dumped = [item.model_dump() for item in stock] # type: ignore

    field_names = stock_dumped[0].keys() # type: ignore

    output = io.StringIO() # Memória temporária para armazenar o CSV gerado

    writer = csv.DictWriter(
        output,
        fieldnames=field_names
    )

    writer.writeheader()
    writer.writerow(stock_dumped[0]) 

    output.seek(0) # Volta para o início do arquivo para leitura para a response
    
    return output

pattern = re.compile(r"\b(" + "|".join(keywords) + r")\b", re.IGNORECASE)

def extract_relevant_lines(document):
    """Processa os documentos localmente com Regex mantendo somente linhas relevantes, usando algoritmo de palavras-chave + linhas com números"""
    #TODO: Ainda precisa de ajustes ao novo modelo de documentos
    
    return ...

#TODO: Exportar para Excel