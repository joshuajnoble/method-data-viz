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
app = mo.App(width="medium", css_file="custom.css")

with app.setup(hide_code=True):
    # imports
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import marimo as mo
    import plotly.io as pio
    import numpy as np
    from pathlib import Path

    COLOR_PALETTE = [
        "#4442e3", # 1. Brand Blue
        "#ffb60c", # 2. Brand Yellow
        "#ff584e", # 3. Brand Coral
        "#10b981", # 4. Method Green
        "#8b89f5", # 5. Vibrant Periwinkle
        "#2b298c", # 6. Deep Navy
        "#0ea5e9", # 7. Electric Teal
        "#f97316", # 8. Vibrant Orange
        "#ff9e99", # 9. Soft Melon
        "#4e4e4e"  # 10. Method Slate
    ]

    # set plotly default template and disable mode bar
    pio.templates.default = "plotly_white"
    pio.templates["plotly_white"].layout.margin = dict(t=0, b=0)
    pio.templates["plotly_white"].layout.font.family = "var(--marimo-text-font)"
    pio.templates["plotly_white"].layout.title.font.family = "var(--marimo-text-font)"
    for renderer_name in pio.renderers.default.split("+"):
        renderer_name = renderer_name.strip()
        if not renderer_name:
            continue
        if renderer_name not in pio.renderers:
            continue
        renderer = pio.renderers[renderer_name]
        if hasattr(renderer, "config") and renderer.config is not None:
            renderer.config["displayModeBar"] = False


@app.cell
def _():

    @mo.cache
    def get_weekly():

        path_to_csv = mo.notebook_location() / "public" / "weekly_sales.csv"
        weekly = pd.read_csv(path_to_csv)
        weekly['Order Date'] = pd.to_datetime(weekly['Order Date'])
        return weekly

    @mo.cache
    def get_daily_sales():

        path_to_csv = mo.notebook_location() / "public" / "daily_sales.csv"
        daily = pd.read_csv(path_to_csv)
        daily['Order Date'] = pd.to_datetime(daily['Order Date'])
        return daily

    @mo.cache
    def get_event_data():

        path_to_csv = mo.notebook_location() / "public" / "events_2014.csv"
        events = pd.read_csv(path_to_csv)
        events['Order Date'] = pd.to_datetime(events['Order Date'])
        return events
    
    @mo.cache
    def get_weekly_by_segment():

        path_to_csv = mo.notebook_location() / "public" / "weekly_sales_by_segment.csv"
        weekly_sales_by_segment = pd.read_csv(path_to_csv)
        weekly_sales_by_segment['Order Date'] = pd.to_datetime(weekly_sales_by_segment['Order Date'])
        return weekly_sales_by_segment
    
    return ()


@app.cell
def _():
    mo.md(
        """
        # Data with time
        
        Not all data that includes time is the same. For instance, if your data has irregular time stamps like tracking when earthquakes happen, 
        then that's event data. If your data has regular time stamps, like tracking the temperature inside your house every hour, then that's a 
        time series. Because they're pretty different types of data, they should different sorts of visualization.

        ## Time Series 
        
        First lets look at time series data. The sum of weekly sales has a regular interval and it's easy to measure one reading (weekly sales) against another. 
        In this case, a line graph shows how the trend is changing over time.

        """
    )
    return

@app.cell
def _():

    weekly = get_weekly()
    mask_2014 = weekly["Order Date"].dt.year == 2014
    line_fig = px.line(weekly.loc[mask_2014], x="Order Date", y="sales")
    mo.ui.plotly(line_fig, config={"displayModeBar": False})
    return

@app.cell
def _():
    mo.md(
        """
        
        We can also take the weekly change to see how one week compares to another. This is called 'differencing' and it can clearly show trends.
        In our dataset there is no clear trend:

        """
    )
    return

@app.cell
def _():

    weekly['Difference'] = weekly['sales'].diff()
    bar_fig = px.bar(weekly.loc[mask_2014], x="Order Date", y="Difference")
    mo.ui.plotly(bar_fig, config={"displayModeBar": False})
    return


@app.cell
def _():

    daily = get_daily_sales()

    # A simple example using random data for demonstration
    heatmap = go.Figure(data=go.Heatmap(
            z=daily["sales"],
            y=daily["Order Date"].dt.month,
            x=daily["Order Date"].dt.day,
            colorscale='Viridis'
        ))

    # If you have raw datetime objects in x/y, Plotly handles them automatically:
    # fig = go.Figure(data=go.Heatmap(z=my_z_data, x=my_date_list_x, y=my_date_list_y))

    heatmap.update_layout(title='Datetime Heatmap Example')
    mo.ui.plotly(heatmap, config={"displayModeBar": False})

    return

@app.cell
def _():
    mo.md(
        """



        ## Events
        
        If we look at every sales event, it's far too dense to be readable or useful:

        """
    )
    return

@app.cell
def _():

    event_df = get_event_data()
    scatter_fig = px.scatter(event_df, x="Order Date", y="Sales", opacity=0.2)
    mo.ui.plotly(scatter_fig, config={"displayModeBar": False})
    return

@app.cell
def _():
    mo.md(
        """
        
        Instead, think of finding what events are relevant to reduce the chart density and guide the readers of the chart to what's most useful.

        """
    )
    return

@app.cell(hide_code=True)
def _():
    chart_slider = mo.ui.slider(
        start=1000,
        stop=5000,
        value=1000,
        label="Sales greater than",
        show_value = True,
    )

    mo.center(chart_slider)
    return (chart_slider,)

@app.cell(hide_code=True)
def _(chart_slider, event_df):

    _min = chart_slider.value

    scatter_fig_filtered = px.scatter(event_df[event_df["Sales"] > _min], x="Order Date", y="Profit", color="Segment", size="Sales", opacity=0.3)
    mo.ui.plotly(scatter_fig_filtered, config={"displayModeBar": False})

    return

# @app.cell
# def _():

#     scatter_fig_plotting = px.scatter(event_df.query("Segment == 'Consumer'"), x="Order Date", y="Sales", size="Profit", opacity=0.1)
#     mo.ui.plotly(scatter_fig_plotting, config={"displayModeBar": False})
#     return


if __name__ == "__main__":
    app.run()