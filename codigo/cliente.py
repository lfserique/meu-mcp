"""Cliente MCP mínimo: conecta ao servidor via stdio, lista e chama tools."""
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

servidor = StdioServerParameters(command=sys.executable, args=["server.py"])


async def main():
    async with stdio_client(servidor) as (leitura, escrita):
        async with ClientSession(leitura, escrita) as sessao:
            await sessao.initialize()

            tools = await sessao.list_tools()
            print("Tools disponíveis:", [t.name for t in tools.tools])

            r = await sessao.call_tool("cardapio_do_dia", {"dia": "quarta"})
            print("Cardápio:", r.content[0].text)

            r = await sessao.call_tool("calcular_media", {"notas": [7, 5.5, 8]})
            print("Média:", r.content[0].text)


asyncio.run(main())
