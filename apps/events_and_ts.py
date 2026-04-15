# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "plotly",
#     "pandas",
#     "numpy"
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium", css_file="custom.css")


@app.cell(hide_code=True)
async def setup_wasm():
    import sys
    import types
    import importlib.util
    from pathlib import Path

    module_name = "my_utils"

    if sys.platform == "emscripten":
        from pyodide.http import pyfetch

        print("WASM detected: Fetching local modules...")
        # needs to be ../public because of how the assets dir is created during build
        response = await pyfetch("../public/my_utils.py")
        if not response.ok:
            print("Attempted to fetch:", response.url)
            raise RuntimeError(f"Failed to load my_utils.py. Status: {response.status}")

        source = await response.text()
        module = types.ModuleType(module_name)
        module.__file__ = "/virtual/my_utils.py"
        exec(compile(source, module.__file__, "exec"), module.__dict__)
        sys.modules[module_name] = module
        my_utils = module
        print("Successfully loaded my_utils.py!")
    else:
        # Local Python: load from apps/public/my_utils.py
        module_path = Path("./apps/public/my_utils.py").resolve()
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load module spec from {module_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        my_utils = module
        print("Local Python environment detected. Loaded my_utils.py from public/.")

    my_utils.run_plotly_defaults()
    return (my_utils,)


@app.cell
async def _(my_utils):
    import pandas as pd

    # import data
    superstore_df = await my_utils.gh_pages_read_csv_into_df("superstore.csv")

    weekly_sales_df = await my_utils.gh_pages_read_csv_into_df("weekly_sales.csv")
    weekly_sales_df['Order Date'] = pd.to_datetime(weekly_sales_df['Order Date'])

    daily_df = await my_utils.gh_pages_read_csv_into_df("daily_sales.csv")
    daily_df['Order Date'] = pd.to_datetime(daily_df['Order Date'])

    events_df = await my_utils.gh_pages_read_csv_into_df("events_2014.csv")
    events_df['Order Date'] = pd.to_datetime(events_df['Order Date'])

    weekly_sales_by_segment_df = await my_utils.gh_pages_read_csv_into_df("weekly_sales_by_segment.csv")
    weekly_sales_by_segment_df['Order Date'] = pd.to_datetime(weekly_sales_by_segment_df['Order Date'])
    return daily_df, events_df, pd, superstore_df, weekly_sales_df


@app.cell
def _(mo):
    mo.md("""
    # Time and Flows

    Ah, the most philosohpical of our charting sections: what does time mean and how do things flow from one state to another? If you're a project manager, this section is for you, because we are going to talk about Gantt charts.

    Time is a data feature that naturally lends itself to grouping or filtering and because of that, it's a powerful tool for creating aggregate views.
    For instance: all sales in 2012 or the aggregated sales on the first day of a month. It's also potentially very confusing.

    Not all data that includes time is the same. For instance, if your data has irregular time stamps like tracking when earthquakes happen,
    then that's event data. If your data has regular time stamps, like tracking the temperature inside your house every hour, then that's a
    time series. Because they're pretty different types of data, they should use different sorts of visualization.

    ## Time Series

    First lets look at time series data. The sum of weekly sales has a regular interval and it's easy to measure one reading (weekly sales) against another.
    In this case, a line graph shows how the trend is changing over time.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo, weekly_sales_df):
    import plotly.express as px

    mask_2014 = weekly_sales_df["Order Date"].dt.year == 2014
    line_fig = px.line(weekly_sales_df.loc[mask_2014], x="Order Date", y="sales")
    mo.ui.plotly(line_fig, config={"displayModeBar": False})
    return mask_2014, px


@app.cell
def _(mo):
    mo.md("""
    We can also take the weekly change to see how one week compares to another. This is called 'differencing' and it can clearly show trends.
    In our dataset there is no clear trend in the weekly amount of sales. That's helpful to know!
    """)
    return


@app.cell
def _(mask_2014, mo, px, weekly_sales_df):

    weekly_sales_df['Difference'] = weekly_sales_df['sales'].diff()
    bar_fig = px.bar(weekly_sales_df.loc[mask_2014], x="Order Date", y="Difference")
    mo.ui.plotly(bar_fig, config={"displayModeBar": False})
    return


@app.cell
def _(mo):
    mo.md("""
    A different strategy to show how readings in a time series differ from one another is to use a heatmap. This is helpful if you believe there
    are patterns that exist day to day and across days of the month. For instance, companies might buy supplies on the 1st, consumer spending may
    spike on the 15th. A heatmap allows you to compare horizontally and vertically.
    """)
    return


@app.cell
def _(daily_df, mo):
    import plotly.graph_objects as go
    import numpy as np
    import calendar

    heatmap = go.Figure(data=go.Heatmap(
            z=daily_df["sales"],
            y=daily_df["Order Date"].dt.month,
            x=daily_df["Order Date"].dt.day,
            colorscale='Viridis'
        ))

    months = list(calendar.month_name)[1:]

    heatmap.update_layout(
        title='Daily Total Sales',
        xaxis=dict(title='Day'),
        yaxis=dict(title='Month', tickmode='array', tickvals=np.arange(1,13), ticktext=months)
    )

    mo.ui.plotly(heatmap, config={"displayModeBar": False})
    return (go,)


@app.cell
def _(mo):
    mo.md("""
    ## Events

    An event has a timestamp, just like a time series, but they aren't regular readings, they're just recording when something happened. This means that
    putting them into a line chart just won't work. We can group them by week or month in order to create time series data from them, but then we lose some of the precision about the event itself.

    Visualizing events is all about finding what information is meaningful. Maybe that's the spacing between events, a sequence, or simply a filtered subset of events. If we look at every sales event, it's far too dense to be readable or useful:
    """)
    return


@app.cell
def _(events_df, mo, px):

    scatter_fig = px.scatter(events_df, x="Order Date", y="Sales", opacity=0.2)
    mo.ui.plotly(scatter_fig, config={"displayModeBar": False})
    return


@app.cell
def _(mo):
    mo.md("""
    Instead, think of finding what events are relevant to reduce the chart density and guide the readers of the chart to what's most useful.
    Check out how much more legible this chart becomes with a filter for the lower bound.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
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
def _(chart_slider, events_df, mo, px):

    _min = chart_slider.value

    scatter_fig_filtered = px.scatter(events_df[events_df["Sales"] > _min], x="Order Date", y="Profit", color="Segment", size="Sales", opacity=0.3)
    scatter_fig_filtered.update_yaxes(range=[-4500, 4500])
    mo.ui.plotly(scatter_fig_filtered, config={"displayModeBar": False})
    return


@app.cell
def _(mo):
    mo.md("""
    ## Sequences

    Time is also a key component of sequences, that is, some kind of event that has a start timestamp and an end timestamp.
    If you've ever seen a project plan, you've seen a Gantt chart, and thus you've understood a sequence. The Gantt chart is usually meant to be read from top to bottom (typically the y-axis in a project planning Gantt chart sorts by start date) and left to right.
    The x-axis is the date and that's applied to both the start and the end date. The width of a band shows the relative duration of an event as well as the relative ordering of the begining and ending of events.
    What we get from a Gantt chart is an view of sequences and their relationships to one another in time.

    In the below Gantt chart we can see how Josh and Ben worked on this project (although, caveats, the data is not real).
    """)
    return


@app.cell
def _(mo, pd, px):

    gantt_data = pd.DataFrame([
        dict(Task="Planning and Initial Script", Start='2025-01-15', Finish='2025-02-15', Resource="Josh"),
        dict(Task="Script Review and Refinement", Start='2025-02-01', Finish='2025-02-28', Resource="Ben"),
        dict(Task="Design Definition", Start='2025-02-15', Finish='2025-02-28', Resource="Ben"),
        dict(Task="Technical Architecture", Start='2025-01-15', Finish='2025-02-28', Resource="Josh"),
        dict(Task="Visualization Development", Start='2025-03-05', Finish='2025-05-30', Resource="Ben"),
        dict(Task="Visualization Development", Start='2025-04-01', Finish='2025-05-30', Resource="Josh"),
        dict(Task="Workshop Prep, Ben", Start='2025-06-01', Finish='2025-06-08', Resource="Ben"),
        dict(Task="Workshop Prep, Josh", Start='2025-06-01', Finish='2025-06-08', Resource="Josh")
    ])

    gantt_data = gantt_data.sort_values("Start")

    fig = px.timeline(gantt_data, x_start="Start", x_end="Finish", y="Task", color="Resource")

    fig.update_layout(yaxis={'categoryorder': 'array', 'categoryarray': gantt_data["Task"].unique()[::-1]})

    # Display the figure
    mo.ui.plotly(fig, config={"displayModeBar": False})
    return


@app.cell
def _(mo):
    mo.md("""
    ## Flows

    A flow is sort of like the set of sequences we see in a Gantt chart (sort of) and it's often represented in a Sankey chart. That name might not be familiar to you, but there's a very good chance that you've seen one before.

    Technically a Sankey chart is weighted directed graph. The dataset is usually what is called an "edge list" and it contains nodes and edges along with a weight list for each edge.

    You may have seen these in maps of energy sources. In fact the "Sankey" graph is named after a fellow with the last name Sankey who invented them to visualize energy efficiency in steam engines.
    They're an excellent fit for a situation where a flow transitions into multiple sub-flows. For instance, how energy flowing through a system, or how company revenue turns into salaries for workers, taxes, and profits to shareholders. That's a form of process mapping.
    It's that "turns into" that gives the Sankey its distinctive shape and they do certainly look cool.

    There are some caveats to the Sankey though: they're not appropriate when precise comparisons need to be made and they very quickly become visually overwhelming and uninformative.
    They can become bad enough to inspire a whole [article](https://sciolisticramblings.wordpress.com/2018/11/23/sankey-charts-the-new-pie-chart/) and that's testament to how good they are when used well and unhelpful they are when used poorly.
    """)
    return


@app.cell
def _(go, pd, superstore_df):

    seg_cat = (superstore_df.groupby(["Segment", "Category"])["Sales"].sum().reset_index())
    cat_sub = (superstore_df.groupby(["Category", "Sub-Category"])["Sales"].sum().reset_index())

    nodes = list(pd.concat([
        seg_cat["Segment"],
        seg_cat["Category"],
        cat_sub["Sub-Category"]
    ]).unique())

    node_index = {name: i for i, name in enumerate(nodes)}

    sources = seg_cat["Segment"].map(node_index)
    targets = seg_cat["Category"].map(node_index)
    values  = seg_cat["Sales"]

    sources2 = cat_sub["Category"].map(node_index)
    targets2 = cat_sub["Sub-Category"].map(node_index)
    values2  = cat_sub["Sales"]

    sources = pd.concat([sources, sources2])
    targets = pd.concat([targets, targets2])
    values  = pd.concat([values, values2])

    sankey_fig = go.Figure(go.Sankey(
        node=dict(
            label=nodes,
            pad=20,
            thickness=20
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    ))

    sankey_fig.update_layout(title="Superstore Flow")
    sankey_fig
    return


@app.cell
def _(mo):
    mo.md("""
    Sankey charts teach us something important to remember about really cool kinds of charts: they often get in the way of what a chart or visualization is supposed to do. The same is true for alluvial charts, network graphs, word-clouds and many other kinds of visually complex but difficult to understand visualizations.
    Communicating information clearly and concisely might not seem spectacular, but it is impressive because it is hard to do. A good visualization very much follows an 'outcomes over outputs' philosophy.
    If the reader of a visualization can understand what to _do_ with that information, then the output is impressive because it leads to the right outcome.
    """)
    return


if __name__ == "__main__":
    app.run()
