from fastmcp import FastMCP
import httpx, json

mcp = FastMCP("Elegy Scammer MCP Server")

@mcp.tool
def get_market_data(search=None, sort=None, sort_direction=None, page_size=None, etc=None, etc_value=None):
    """Fetch and return revenues market data from the Revenant Elegy API.

    This MCP server tool builds a query URL from optional filter and sort parameters,
    calls the Revenant Elegy market endpoint, and returns the API response as a
    pretty-printed JSON string.

    Parameters:
        search (str | None): Optional search text for matching marketplace items.
        sort (str | None): Optional sort field, such as 'price'.
        sort_direction (str | None): Optional direction for sorting, e.g. 'asc' or 'desc'.
        page_size (int | None): Optional number of results per page.
        etc (str | None): Optional custom query parameter name to append.
        etc_value (str | None): Optional value for the custom query parameter.

    Returns:
        str: Pretty-printed JSON response from the market API.
    """
    if etc and etc_value:
        extraParameter = f"&{etc}={etc_value}"
    else:
        extraParameter = ""
    if search is not None:
        searchParams = f"&search={search}"
    else:
        searchParams = None
    if sort_direction is not None:
        sort="price"

    market_url = f"https://revenantelegy.com/api/v1.0/market/?sort={sort}&sort_dir={sort_direction}&page_size={page_size}+{searchParams}+{extraParameter}" 
    market_data_unparsed = httpx.get(market_url)
    market_data_pretty = json.dumps(market_data_unparsed.json(), indent=1)

    return market_data_pretty

if __name__=="__main__":
    mcp.run(transport='http')