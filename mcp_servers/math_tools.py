from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math Tools")

@mcp.tool()
def add(a: int, b: int):
    """Add tool."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int):
    """Multiply tool."""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")