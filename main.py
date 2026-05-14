from fastmcp import FastMCP
import httpx, os


PORT = os.environ.get("PORT", 8000)
mcp = FastMCP("Revenant Elegy Market MCP Server")

BASE_URL = "https://revenantelegy.com/api/v1.0/market/"

@mcp.tool
def get_market_data(
    search: str | None = None,
    sort: str | None = None,
    sort_direction: str | None = None,
    page_size: int | None = None,
    extra_params: dict | None = None,
) -> dict:
    """Fetch marketplace listings from the Revenant Elegy market API.

    Parameters:
        search: Optional search term to filter items by name or description.
        sort: Field to sort results by (e.g. 'price', 'name').
        sort_direction: Sort order — 'asc' or 'desc'.
        page_size: Number of results to return per page.
        extra_params: Optional dict of additional query parameters to include.

    Returns:
        Parsed JSON response from the market API as a dict.

    Raises:
        ValueError: If the API returns a non-2xx status code.
    """
    params: dict = {}

    if search is not None:
        params["search"] = search
    if sort is not None:
        params["sort"] = sort
    if sort_direction is not None:
        params["sort_dir"] = sort_direction
    if page_size is not None:
        params["page_size"] = page_size
    if extra_params:
        params.update(extra_params)

    try:
        response = httpx.get(BASE_URL, params=params, timeout=10.0)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Market API returned {e.response.status_code}: {e.response.text}") from e
    except httpx.RequestError as e:
        raise ValueError(f"Failed to reach market API: {e}") from e

    return response.json()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
