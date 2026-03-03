# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
# ]
# ///
import marimo as mo
import pandas as pd
import plotly
import plotly.express as px

import numpy as np

__generated_with = "0.19.7"
app = mo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    @mo.cache
    def raw_sales():

        path_to_csv = mo.notebook_location() / "public" / "raw_sales.csv"
        raw_sales = pd.read_csv(path_to_csv)
        return raw_sales
    
    return (mo,)

@app.cell
async def _():
    import matplotlib.pyplot as plt
    
    import plotly.express as px
    import numpy as np

    import micropip

    await micropip.install("plotly")

    return (plt,)

@app.cell
def _():
    mo.md(
        """
        ## Height
        This shows how what kinds of amounts purchases are most common.
        """
    )
    return

@app.cell()
def _(mo):

    raw = raw_sales()

    fig, ax = plt.subplots()
    ax.hist(raw['Sales'], bins=30)
    ax.set_title('Static Matplotlib Plot')
    ax.legend()

    # The figure object is the last expression, so marimo displays it automatically
    fig 
    # The variables `x`, `y`, `fig`, and `ax` are now available to other cells


@app.cell
def _():
    mo.md(
        """
        ## Height
        This shows how what kinds of amounts purchases are most common.
        """
    )
    return

@app.cell()
def _(mo):

    # Compute histogram in log space
    log_x = np.log10(raw['Sales'])
    counts, log_bins = np.histogram(log_x, bins=30)

    # Convert bin edges back to original scale
    bins = 10**log_bins

    # Plot using original-scale bins
    bar = plt.bar(bins[:-1], counts, width=np.diff(bins), align='edge')

    plt.xscale('log')  # Keep axis linear

    # Set ticks at specific positions and provide custom labels
    tick_positions = [1, 10, 100, 1000, 10000, 100000]
    tick_labels = ["$1", "$10", "$100", "$1000", "$10000", "$100000"]

    plt.xticks(tick_positions, tick_labels, rotation=45) # You can also add kwargs like rotation


    plt.xlabel("Order Amount")
    plt.ylabel("Number of Orders 2011-14")
    bar
    


if __name__ == "__main__":
    app.run()