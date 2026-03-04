import marimo as mo
import pandas as pd

async def gh_pages_read_csv_into_df(filename: str) -> pd.DataFrame:
    filepath = mo.notebook_location() / "public" / filename
    if "http" not in str(mo.notebook_location()):
        return pd.read_csv(
            filepath, 
            index_col=0
        )
    from pyodide.http import pyfetch
    from io import StringIO
    response = await pyfetch(filepath)
    data = await response.text()
    return pd.read_csv(StringIO(data))