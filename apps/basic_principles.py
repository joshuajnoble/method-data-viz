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
    def get_yearly():

        path_to_csv = mo.notebook_location() / "public" / "yearly_sales.csv"
        yearly_by_segment = pd.read_csv(path_to_csv)
        return yearly_by_segment

    @mo.cache
    def get_yearly_by_segment():

        path_to_csv = mo.notebook_location() / "public" / "yearly_sales_by_segment.csv"
        yearly_by_segment = pd.read_csv(path_to_csv)
        return yearly_by_segment
    
    @mo.cache
    def get_weekly_by_segment():

        path_to_csv = mo.notebook_location() / "public" / "weekly_sales_by_segment.csv"
        weekly_sales_by_segment = pd.read_csv(path_to_csv)
        return weekly_sales_by_segment
    
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
        The height of a bar shows the yearly sales. The point of it is to show how the different years compare to one another.
        """
    )
    return

@app.cell()
def _(mo):

    yearly_sales = get_yearly()

    alt.Chart(yearly_sales).mark_bar().encode(
        alt.Y('sales'),
        alt.X('year:N', title='Year'),
    ).properties(
        width=600,  # Set the width to 600 pixels
        height=400  # Set the height to 400 pixels
    )

@app.cell
def _():
    mo.md(
        """
        ## Labels
        Proper labels show units and specific values.
        """
    )
    return

@app.cell()
def _(mo):

    yearly_sales['truncated'] = yearly_sales['sales']/1_000_000

    alt.Chart(yearly_sales).mark_bar().encode(
        alt.Y('truncated', axis=alt.Axis(labelExpr='"$"+datum.value+"M"'), title="Sales in Millions of USD"),
        alt.X('year:N', title='Sales Year'),
    ).properties(
        width=600,  # Set the width to 600 pixels
        height=400  # Set the height to 400 pixels
    )

@app.cell()
def _(mo):
    mo.md(
        """
        ## Color
        Highlighting one value with color draws the eye to that value.
        """
    )

@app.cell()
def _(mo):

    alt.Chart(yearly_sales).mark_bar().encode(
        alt.Y('sales'),
        alt.X('year:N', title='Year'),
        color=alt.condition(
            alt.datum.year == 2014,  # If the Year is 2020,
            alt.value("#4e8ae9"),     # highlight a bar with green.
            alt.value('lightgrey')   # And grey for the rest of the bars
        ),
    ).properties(
        width=600,  # Set the width to 600 pixels
        height=400  # Set the height to 400 pixels
    )

@app.cell()
def _(mo):
    mo.md(
        """
        
        Color also lets us show complex data easily.
        """
    )

@app.cell()
def _(mo):

    yearly_sales_by_segment = get_yearly_sales_by_segment()

    alt.Chart(yearly_sales_by_segment).mark_bar().encode(
        alt.Y('sales'),
        alt.X('year:N', title='Year'),
        color='Segment',
        xOffset='Segment'
    ).properties(
        width=500,  # Set the width to 600 pixels
        height=400  # Set the height to 400 pixels
    )

@app.cell()
def _(mo):
    mo.md(
        """
        Color alone isn't always enough though. Stacked bar charts are good for showing relative composition but hard for comparison.
        """
    )

@app.cell()
def _(mo):

    alt.Chart(yearly_sales_by_segment).mark_bar().encode(
        alt.Y('sum(sales)'),
        alt.X('year:N', title='Year'),
        color='Segment'
        #tooltip=[alt.Tooltip('year:N', title='Year'), alt.Tooltip('Value', format=',', title='sales')]     
    ).properties(
        width=500,  # Set the width to 600 pixels
        height=400  # Set the height to 400 pixels
    )

@app.cell()
def _(mo):
    mo.md(
        """
        ## Filters
        Adding filters makes comparing across a stacked bar chart easier but always visually help the user keep track of what is selected.
        """
    )

@app.cell()
def _(mo):

    selection = alt.selection_point(fields=['Segment'], bind='legend')

    alt.Chart(yearly_sales_by_segment).mark_bar().transform_calculate(
        site_order=f"if({selection.name}.Segment && indexof({selection.name}.Segment, datum.Segment) !== -1, 0, 1)"
    ).encode(
        alt.Y('sum(sales)'),
        alt.X('year:N', title='Year'),
        color='Segment',
        order='site_order:N',
        opacity=alt.when(selection).then(alt.value(0.9)).otherwise(alt.value(0.2))
    ).add_params(
        selection
    )

if __name__ == "__main__":
    app.run()