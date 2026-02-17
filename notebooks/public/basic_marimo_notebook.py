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
        superstore = pd.read_csv("superstore.csv")
        superstore['Order Date'] = pd.to_datetime(superstore['Order Date'])
        return superstore
    
    return (mo,)

@app.cell
def _():
    import matplotlib.pyplot as plt
    import matplotlib.pyplot as plt
    import seaborn as sns
    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker
    import matplotlib.dates as mdates

    return (plt,)

@app.cell(get_superstore)
def _(mo):

    ss = get_superstore()

    daily_sales = (
        ss.groupby("Order Date", as_index=False).agg(Sales=("Sales", "sum"))
    )
    daily_sales["Order Date"] = pd.to_datetime(daily_sales["Order Date"])


    fig = plt.subplots(figsize=(10, 5))
    ax = sns.lineplot(data=daily_sales, x="Order Date", y='Sales')

    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    # TODO: improve styling
    ax.set_title('Daily Sales')
    ax.set_ylabel('Total Sales in $USD')

    ax.tick_params(axis='x', labelrotation=45)

    ax


if __name__ == "__main__":
    app.run()