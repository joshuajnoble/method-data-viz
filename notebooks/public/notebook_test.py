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
app = mo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    @mo.cache
    def get_superstore():

        #path_to_csv = mo.notebook_location() / "public" / "superstore.csv"
        path_to_csv = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/superstore.csv"
        superstore = pd.read_csv(path_to_csv)
        superstore['Order Date'] = pd.to_datetime(superstore['Order Date'])
        return superstore
    
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
        # Loading a CSV file and using an imported library to render static charts.
        """
    )
    return

@app.cell(get_superstore)
def _(mo):

    ss = get_superstore()

    daily_sales = (
        ss.groupby("Order Date", as_index=False).agg(Sales=("Sales", "sum"))
    )
    daily_sales["Order Date"] = pd.to_datetime(daily_sales["Order Date"])


    fig = plt.subplots(figsize=(10, 5))
    ax = sns.lineplot(daily_sales, x="Order Date", y='Sales')

    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    # TODO: improve styling
    ax.set_title('Daily Sales')
    ax.set_ylabel('Total Sales in $USD')

    ax.tick_params(axis='x', labelrotation=45)

    ax

@app.cell
def _():
    mo.md(
        """
        # Rendering an Altair chart
        """
    )
    return

@app.cell
def _():

    # Create interactive chart
    chart = mo.ui.altair_chart(
        (
            alt.Chart(daily_sales)
            .mark_circle()
            .encode(x="Order Date", y='Sales', size=alt.value(100), color=alt.value("steelblue"))
            .properties(height=400, title="Interactive Scatter Plot")
        )
    )
    chart
    return chart

if __name__ == "__main__":
    app.run()