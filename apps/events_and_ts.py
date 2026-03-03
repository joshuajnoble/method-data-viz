# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
# ]
# ///
import marimo as mo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

__generated_with = "0.19.7"
app = mo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    @mo.cache
    def get_data():
        return []
    
    return (mo,)

@app.cell
async def _():
    import matplotlib.pyplot as plt
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker
    import matplotlib.dates as mdates

    import altair as alt

    import micropip

    await micropip.install("seaborn")
    await micropip.install("altair")

    import seaborn as sns

    return (plt,)

@app.cell
def _():
    mo.md(
        """
        ## Height
        The height of a bar shows the yearly sales.
        """
    )
    return


if __name__ == "__main__":
    app.run()