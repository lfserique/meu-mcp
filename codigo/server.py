"""Meu primeiro servidor MCP: Assistente do Campus."""
import sys
from datetime import date

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("assistente-campus")

CARDAPIO = {
    "segunda": "Arroz, feijão, frango grelhado e salada",
    "terca": "Macarronada à bolonhesa e salada verde",
    "quarta": "Feijoada, couve e laranja",
    "quinta": "Strogonoff de carne, arroz e batata palha",
    "sexta": "Peixe assado, purê e legumes",
}


@mcp.tool()
def cardapio_do_dia(dia: str) -> str:
    """Retorna o cardápio da cantina para um dia útil (segunda a sexta)."""
    chave = dia.strip().lower().replace("ç", "c").replace("-feira", "")
    return CARDAPIO.get(chave, f"Não há cardápio cadastrado para '{dia}'.")


@mcp.tool()
def calcular_media(notas: list[float], media_minima: float = 6.0) -> dict:
    """Calcula a média de uma lista de notas e informa se o aluno foi aprovado."""
    if not notas:
        return {"erro": "Informe ao menos uma nota."}
    media = round(sum(notas) / len(notas), 2)
    print(f"[log] media calculada: {media}", file=sys.stderr)  # log vai para stderr
    return {"media": media, "situacao": "Aprovado" if media >= media_minima else "Reprovado"}


@mcp.resource("campus://regulamento")
def regulamento() -> str:
    """Regras básicas de avaliação da turma."""
    return "Média mínima 6,0. Frequência mínima 75%. Prova substitutiva para quem faltar à prova."


@mcp.prompt()
def plano_de_estudos(disciplina: str) -> str:
    """Gera um pedido de plano de estudos semanal para uma disciplina."""
    return f"Monte um plano de estudos de 5 dias para {disciplina}, a partir de {date.today():%d/%m}."


if __name__ == "__main__":
    mcp.run()  # transporte padrão: stdio
