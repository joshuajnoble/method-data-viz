import marimo as mo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

__generated_with = "0.19.7"
app = mo.App(width="medium")

cell_width = 800

@app.cell
def _():
    import marimo as mo
    import pandas as pd

    cell_width = 800

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
        ## Why
        The purpose of visualizing data is to tell a story. What's the story that you're trying to tell?

        Here the story is that 2014 was a stronger year:
        """
    )
    return

@app.cell()
def _(mo):

    ss = get_superstore()

    yearly_sales = ss.groupby(ss["Order Date"].dt.year)["Sales"].sum()
    sales = pd.DataFrame({"year":ss["Order Date"].dt.year.unique(), "sales":yearly_sales})

    alt.Chart(sales).mark_bar().encode(
        alt.Y('sales'),
        alt.X('year:N', title='Year'),
        color=alt.condition(
            alt.datum.year == 2014,  # If the Year is 2020,
            alt.value("#4e8ae9"),
            alt.value("#90b6f4")   # And grey for the rest of the bars
        ),
        #tooltip=[alt.Tooltip('Year:N', title='Anno'), alt.Tooltip('Value', format=',', title='Immatricolazioni')]     
    ).properties(
        width=cell_width,
        height=400
    )

@app.cell
def _():
    mo.md(
        """
        Adding a trend line shows that story even more clearly:
        """
    )
    return

@app.cell()
def _(mo):

    sales['year_diff'] = sales['year'] - 2011

    chart = alt.Chart(sales).mark_bar().encode(
        alt.Y('sales'),
        alt.X('year:N', title='Year'),
        color=alt.condition(
            alt.datum.year == 2014,  # If the Year is 2020,
            alt.value("#4e8ae9"),
            alt.value("#90b6f4")   # And grey for the rest of the bars
        ),
    ).properties(
        width=cell_width,
        height=400
    )

    chart + chart.transform_regression('year', 'sales').mark_line().encode(color=alt.value('magenta'))

@app.cell
def _():
    mo.md(
        """
        Of course, other types of visualization can show this more clearly. A line shows a trend better than a bar.
        """
    )
    return

@app.cell()
def _(mo):

    sales['truncated'] = sales['sales']/1_000_000

    alt.Chart(sales).mark_line(point=True).encode(
        alt.Y('truncated', axis=alt.Axis(labelExpr='"$"+datum.value+"M"'), title="Sales in Millions of USD"),
        alt.X('year:N', title='Year')    
    ).properties(
        width=cell_width,
        height=400
    )

    #line_chart + line_chart.transform_regression('year', 'sales').mark_line().encode(alt.Color("Regression:N"))
    #line_chart + line_chart.transform_regression('year', 'truncated').mark_line().transform_fold(["Trend"], as_=["Regression", "y"]).encode(alt.Color("Regression:N", scale=alt.Scale(range=["magenta"])))


@app.cell
def _():
    mo.md(
        """
        Multiple lines make it easier to compare trends than multiple bars.
        """
    )
    return

@app.cell()
def _(mo):

    yearly_sales_by_segment = (
        ss.groupby([pd.Grouper(key="Order Date", freq="YE"), "Segment"], as_index=False).agg(sales=("Sales", "sum"))
    )
    yearly_sales_by_segment["Order Date"] = pd.to_datetime(yearly_sales_by_segment["Order Date"])
    yearly_sales_by_segment['year'] = yearly_sales_by_segment["Order Date"].dt.year

    yearly_sales_by_segment['truncated'] = yearly_sales_by_segment['sales']/1_000_000


    alt.Chart(yearly_sales_by_segment).mark_line(point=True).encode(
        alt.Y('truncated', axis=alt.Axis(labelExpr='"$"+datum.value+"M"'), title="Sales in Millions of USD"),
        alt.X('year:N', title='Year'),
        color='Segment:N',  
    ).properties(
        width=cell_width,  # Set the width to 600 pixels
        height=400  # Set the height to 400 pixels
    )

    #line_chart + line_chart.transform_regression('year', 'sales').mark_line().encode(alt.Color("Regression:N"))
    #line_chart + line_chart.transform_regression('year', 'truncated').mark_line().transform_fold(["Trend"], as_=["Regression", "y"]).encode(alt.Color("Regression:N", scale=alt.Scale(range=["magenta"])))


@app.cell
def _():
    mo.md(
        """
        However, it's difficult to compare at a given point. If we want to make sure that users can compare values at given
        point in time, we need to provide a different affordance. There are a number of ways to do that, one is through interaction.
        """
    )
    return

@app.cell()
def _(mo):

    weekly_sales_by_segment = (
        ss.groupby([pd.Grouper(key="Order Date", freq="W-MON"), "Segment"], as_index=False).agg(sales=("Sales", "sum"))
    )
    weekly_sales_by_segment["Order Date"] = pd.to_datetime(weekly_sales_by_segment["Order Date"])
    #weekly_sales_by_segment['week'] = weekly_sales_by_segment["Order Date"].dt.week

    weekly_sales_by_segment['truncated'] = weekly_sales_by_segment['sales']/1_000
    weekly_sales_by_segment['truncated'] = weekly_sales_by_segment['truncated'].round()

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection_point(nearest=True, on="pointerover", fields=["Order Date"], empty=False)

    # The basic line
    line = alt.Chart(weekly_sales_by_segment).mark_line().encode(
        x="Order Date",
        y=alt.Y('truncated:Q', axis=alt.Axis(labelExpr='"$"+datum.value+"K"'), title="Weekly Sales in USD"),
        color="Segment:N",
        opacity=alt.value(0.5)
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(weekly_sales_by_segment).mark_point().encode(x="Order Date", opacity=alt.value(0)).add_params( nearest )
    when_near = alt.when(nearest)

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(opacity=when_near.then(alt.value(1)).otherwise(alt.value(0)))

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align="left", dx=5, dy=-5, fontWeight='bolder').encode(
        text=when_near.then(alt.Text("sales:Q", format="$.2~s")).otherwise(alt.value(" ")), color=alt.value("black")
    )

    # text = line.mark_text(align="left", dx=5, dy=-5, fontWeight='bolder').encode(
    #     text=when_near.then(alt.expr("'$' + format(datum.truncated) + 'K'")).otherwise(alt.value(" ")), color=alt.value("black")
    # )

    text_background = text.mark_text(
        align='left',
        dx=5,dy=-5,
        stroke='white',
        strokeWidth=5,
        strokeJoin='round'
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(weekly_sales_by_segment).mark_rule(color="gray").encode(
        x="Order Date",
    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data
    alt.layer( line, selectors, points, rules, text_background, text ).properties( width=cell_width, height=400 )

if __name__ == "__main__":
    app.run()