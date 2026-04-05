# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "plotly",
#     "pandas",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium", css_file="custom.css")

async with app.setup(hide_code=True):
    # imports
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import marimo as mo
    import numpy as np
    from pathlib import Path
    import sys
    import types
    import importlib.util

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


@app.cell
def _():

    @mo.cache
    def get_cluster_results():
        #path_to_csv = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/apps/public/superstore.csv"
        path_to_csv = mo.notebook_location() / "public" / "clusters.csv"
        clusters = pd.read_csv(path_to_csv)
        return clusters

    @mo.cache
    def get_cluster_centers():
        #path_to_csv = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/apps/public/weekly_sales_by_segment.csv"
        path_to_csv = mo.notebook_location() / "public" / "centers.csv"
        centers = pd.read_csv(path_to_csv)
        return centers

    @mo.cache
    def get_sales_forecasts():
        #path_to_csv = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/apps/public/weekly_sales_by_segment.csv"
        path_to_csv = mo.notebook_location() / "public" / "sales_forecasts.csv"
        centers = pd.read_csv(path_to_csv)
        return centers


    @mo.cache
    def raw_sales():

        #path_to_csv = mo.notebook_location() / "public" / "raw_sales.csv"
        path_to_csv = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/apps/public/raw_sales.csv"
        raw_sales = pd.read_csv(path_to_csv)
        return raw_sales

    @mo.cache
    def get_weekly_sales():
        #path_to_csv = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/apps/public/weekly_sales_by_segment.csv"
        path_to_csv = mo.notebook_location() / "public" / "weekly_sales.csv"
        centers = pd.read_csv(path_to_csv)
        return centers


    return (
        get_cluster_centers,
        get_cluster_results,
        get_sales_forecasts,
        get_weekly_sales,
        raw_sales,
    )


@app.cell
def _():
    mo.md("""
    # Visualization Tasks

    Making visualizations is about telling a story but that story needs a _point_, a "why are we hearing this?". Those points have typologies, just like movies can be a comedy, horror, action, etc, data stories tend to have a broad type.

    ## The Snapshot

    One of those kinds of stories could be framed as "How are things going right now?".
    """)
    return


@app.cell
def _():
    mo.md("""
    ## The Breakdown

    Another story is "What is this made out of?"
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Another way of "breaking things down" is to use a distribution. With the sales data, we might want to see how often different sale amounts occur. Do customers tend to make larger purchases or smaller purchases? We'll use a bar chart to visualize this but each bar will represent a range of values, for instance, 'all sales between $1 and $100'.
    """)
    return


@app.cell
def _(raw_sales):
    raw = raw_sales()

    lin_counts, lin_bins = np.histogram(raw, bins=50)

    # Compute bin centers and widths
    lin_bin_centers = (lin_bins[:-1] + lin_bins[1:]) / 2
    lin_bin_widths = lin_bins[1:] - lin_bins[:-1]

    lin_bin_fig = go.Figure()

    # Stack bin edges for hover info
    lin_bin_ranges = np.stack([lin_bins[:-1], lin_bins[1:]], axis=-1)

    lin_bin_fig.add_trace(go.Bar(
        x=lin_bin_centers,
        y=lin_counts,
        width=lin_bin_widths,
        customdata=lin_bin_ranges
    ))

    #sales_hist = px.histogram(raw, x="Sales", nbins=100)

    lin_bin_fig.update_layout(
        title="Amount of Sales",
        xaxis_title="Amount of sale",
        yaxis_title="Number of sales",
        showlegend=False
    )

    lin_bin_fig.update_traces(hovertemplate="<b>%{y}</b> Sales between $%{customdata[0]:.2f} and $%{customdata[1]:.2f}<extra></extra>")
    mo.ui.plotly(lin_bin_fig, config={"displayModeBar": False})
    return (raw,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Now, that's sort of helpful, most of our sales are small and a few are very large (people often refer to this as a 'long-tail' distribution). It's also really hard to read. We might want to just change how our groups are structured. For instance, instead of $1 - $250 and then $250-$750 we could do $1 - $10 and then $10 - $100 and then $100-1000.
    """)
    return


@app.cell
def _(raw):

    # Compute histogram in log space
    log_x = np.log10(raw['Sales'])
    counts, log_bins = np.histogram(log_x, bins=30)

    # Convert bin edges back to original scale
    bins = 10**log_bins

    # Compute bin centers and widths
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_widths = bins[1:] - bins[:-1]

    log_bin_fig = go.Figure()

    # Stack bin edges for hover info
    bin_ranges = np.stack([bins[:-1], bins[1:]], axis=-1)

    log_bin_fig.add_trace(go.Bar(
        x=bin_centers,
        y=counts,
        width=bin_widths,
        customdata=bin_ranges
    ))

    log_bin_fig.update_xaxes(
        type="log",
        title="Sales"
    )

    log_bin_fig.update_yaxes(
        title="Count"
    )

    log_bin_fig.update_layout(
        title="Histogram of Sales with Log-Spaced Bins"
    )

    tick_vals = [1, 10, 100, 1000, 10000, 100000]

    log_bin_fig.update_xaxes(
        tickmode="array",
        tickvals=tick_vals,
        ticktext=[f"${v:,}" for v in tick_vals]
    )

    log_bin_fig.update_traces(hovertemplate="<b>%{y}</b> Sales between $%{customdata[0]:.2f} and $%{customdata[1]:.2f}<extra></extra>")


    mo.ui.plotly(log_bin_fig, config={"displayModeBar": False})
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Distributions are a way of understanding how widely varied something is. If all of our sales were between $100 and $200, that would be really good to know.
    If no one ever spent more than $500, that's a story worth telling our audience and visualizing the distribution will help you tell it.
    """)
    return


@app.cell
def _():
    mo.md("""
    ## The Fortune-teller

    We all love a "where are things going?" story. We can tell this is a popular story because of how common the 'up and to the right' line-chart is our visual culture. The line chart is a perfect representation of how things _have been going_. For instance, here are weekly sales in our store:
    """)
    return


@app.cell
def _(get_weekly_sales):
    weeklies = get_weekly_sales()

    historical_fig = go.Figure()

    historical_fig.add_trace(go.Scatter(
        x=weeklies['Order Date'][-26:],
        y=weeklies['sales'][-26:],
        mode='lines',
        line=dict(color='black'),
        name='Actuals'
    ))

    historical_fig.update_xaxes(
        title="Week"
    )

    historical_fig.update_yaxes(
        title="Aggregated Sales in US$"
    )

    mo.ui.plotly(historical_fig, config={"displayModeBar": False})
    return (weeklies,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    We might work with someone who says: we should predict what's going to happen. They might give us a 'forecast' of future weekly sales based on a machine learning model or statistical analysis of some kind. We'd want to make sure that the actual weekly and the forecast weekly sales are visually distinct from one another. To that, add a dividing line and use two different colors for the lines:
    """)
    return


@app.cell
def _(get_sales_forecasts, weeklies):

    forecasts = get_sales_forecasts()

    forecast_fig = go.Figure()

    forecast_fig.add_trace(go.Scatter(
        x=forecasts['ds'],
        y=forecasts['p50'],
        mode='lines',
        line=dict(color='blue', width=2),
        name='Forecast',
        hoverlabel=dict(
            bgcolor="blue", # Set the background color
            font=dict(
                color="white" # Set the font color
            )
        )
    ))

    forecast_fig.add_trace(go.Scatter(
        x=weeklies['Order Date'][-26:],
        y=weeklies['sales'][-26:],
        mode='lines',
        line=dict(color='black'),
        name='Actuals'
    ))

    forecast_fig.update_xaxes(
        title="Week"
    )

    forecast_fig.update_yaxes(
        title="Aggregated Sales in US$"
    )

    forecast_fig.update_traces(hovertemplate="<b>Sales:</b> %{y:$.2f}")
    forecast_fig.add_vline(x=weeklies['Order Date'].max(), line_width=2, line_dash="dash", line_color="orange")

    mo.ui.plotly(forecast_fig, config={"displayModeBar": False})
    return (forecasts,)


@app.cell
def _():
    mo.md("""
    One of the challenges of forecasting though is that you can make a prediction, but you know that there's a chance it may not be right. To express this, we often use confidcence intervals to say how likely it is that the true number will be within a range.

    In this chart we're saying that there's an 80% chance that the actual sales will be within the 80% range and a 50% chance that it will be within the 50% range. The wider the likelihood, the wider the possible values. It's like guessing how tall an newborn boy might be when as an adult. There's a 80% chance they'll be between 5'6 and 6'4, there's a 50% chance they'll be between 5'9 and 6'2. The narrower the range, the less likely they'll land within it. If we're guessing how tall that infant might be in 1 year, we can narrow our range more comfortably.

    The median forecast is just the middle, it's not the most likely per se, it's just the middle of our forecasts.
    As we go further in time, our forecasts become more and more uncertain, which makes sense. I can usually guess what the weather will be tomorrow but it's much harder to guess what it will be in a month or in 5 years.
    The uncertainty range helps us express that and tell the story of our forecasts and how they should be understood.
    """)
    return


@app.cell
def _(forecasts, weeklies):

    forecast_w_prob_fig = go.Figure()

    forecast_w_prob_fig.add_trace(go.Scatter(
        x=forecasts['ds'],
        y=forecasts['p90'],
        mode = 'lines',
        fillcolor='rgba(0, 0, 255, 0.1)',
        line=dict(color="blue", width=0),
        showlegend=False,
        name='80% probability',
            hoverlabel=dict(
            bgcolor="lightblue", # Set the background color
            font=dict(
                color="black" # Set the font color
            )
        )
    ))

    forecast_w_prob_fig.add_trace(go.Scatter(
        x=forecasts['ds'],
        y=forecasts['p10'],
        fill='tonexty',
        fillcolor='rgba(0, 0, 255, 0.1)',
        line=dict(color="blue", width=0),
        mode = 'lines',
        name='80% probability',
            hoverlabel=dict(
            bgcolor="lightblue", # Set the background color
            font=dict(
                color="black" # Set the font color
            )
        )
    ))

    forecast_w_prob_fig.add_trace(go.Scatter(
        x=forecasts['ds'],
        y=forecasts['p75'],
        mode = 'lines',
        fillcolor='rgba(0, 0, 255, 0.1)',
        line=dict(color="blue", width=0),
        showlegend=False,
        name='50% probability',
        hoverlabel=dict(
            bgcolor="lightblue", # Set the background color
            font=dict(
                color="black" # Set the font color
            )
        )
    ))

    forecast_w_prob_fig.add_trace(go.Scatter(
        x=forecasts['ds'],
        y=forecasts['p25'],
        mode = 'lines',
        fill='tonexty',
        fillcolor='rgba(0, 0, 255, 0.1)',
        line=dict(color="blue", width=0),
        name='50% probability',
        hoverlabel=dict(
            bgcolor="lightblue", # Set the background color
            font=dict(
                color="black" # Set the font color
            )
        )
    ))

    forecast_w_prob_fig.add_trace(go.Scatter(
        x=forecasts['ds'],
        y=forecasts['p50'],
        mode='lines',
        line=dict(color='blue', width=2),
        name='Median forecast',
        hoverlabel=dict(
            bgcolor="blue", # Set the background color
            font=dict(
                color="white" # Set the font color
            )
        )
    ))

    forecast_w_prob_fig.add_trace(go.Scatter(
        x=weeklies['Order Date'][-26:],
        y=weeklies['sales'][-26:],
        mode='lines',
        line=dict(color='black'),
        name='Actuals'
    ))

    forecast_w_prob_fig.update_xaxes(
        title="Week"
    )

    forecast_w_prob_fig.update_yaxes(
        title="Aggregated Sales in US$"
    )

    forecast_w_prob_fig.add_vline(x=weeklies['Order Date'].max(), line_width=2, line_dash="dash", line_color="orange")
    forecast_w_prob_fig.update_traces(hovertemplate="<b>Sales:</b> %{y:$.2f}")

    mo.ui.plotly(forecast_w_prob_fig, config={"displayModeBar": False})
    return


@app.cell
def _():
    return


@app.cell
def _():
    mo.md("""
    ## The Grouping

    Yet another story is "Which of these things are like one another?"

    Let's take our shopper data and find some clusters of customers. We'll say that we have 4:

    * High Profit Buyers - these are customers who make the company money and don't worry too much about shopping for discounts. 'High value'
    * Bargain Hunters - these are customers who pop in for the sales, but won't buy without one.
    * The Reliable Middle - these shoppers are mid-profit, mid-frequency, and like a bargain but buy what they need even if it's not on sale.
    * Frugal Frequent Buyers - these shoppers buy often but don't make the company much profit and love a discount.

    To visualize these clusters, we'll use a scatterplot with circles around the center of the clusters. First, show how the Profit vs Number of Orders breaks down:
    """)
    return


@app.cell
def _():
    toggle_cluster_centers = mo.ui.switch(label="Toggle cluster centers", value=False)
    x_dropdown = mo.ui.dropdown(options=['Order Count', 'Sales', 'Profit', 'Discounts'], label="X Value", value="Sales")
    y_dropdown = mo.ui.dropdown(options=['Order Count', 'Sales', 'Profit', 'Discounts'], label="Y Value", value="Profit")
    return toggle_cluster_centers, x_dropdown, y_dropdown


@app.cell
def _(toggle_cluster_centers):
    _message = my_utils.callout_neutral("Drawing the cluster centers is an easy way to show how the clusters are similar from one another and similar.")

    mo.hstack([_message,toggle_cluster_centers],gap=2,align="center",widths=[2,.75])
    return


@app.cell
def _(get_cluster_centers, get_cluster_results, toggle_cluster_centers):

    clusters = get_cluster_results()
    centers = get_cluster_centers()

    cluster_colors = px.colors.qualitative.D3
    cluster_ids = clusters["ClusterName"].unique()

    color_map = {cid: cluster_colors[i] for i, cid in enumerate(cluster_ids)}

    profit_x_orders = px.scatter(clusters, 
                    x='Profit', 
                    y='Order Count', 
                    color='ClusterName',
                    title='Customer Types',
                    opacity=0.5,
                    color_discrete_map=color_map,
                    width=1000, height=600)

    if toggle_cluster_centers.value:
        for _, row in centers.iterrows():
            profit_x_orders.add_trace(
                go.Scatter(
                    x=[row["Profit"]],
                    y=[row["Order Count"]],
                    mode="markers",
                    marker=dict(
                        color=color_map[row["ClusterName"]],
                        size=100,
                        opacity=0.2,
                        symbol="circle"
                    ),
                    name=f"Center {row['ClusterName']}",
                    showlegend=False
                )
            )

    profit_x_orders.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                                    font=dict(size=14),
                                    margin=dict(t=100, b=50, l=50, r=50),
                                    legend_title_text="Cluster Name")

    mo.ui.plotly(profit_x_orders, config={"displayModeBar": False})
    return centers, clusters, color_map


@app.cell
def _():
    mo.md("""
    When you have too much data, it's important to pick what tells the story, what's informative, and what isn't. Some of our clusters look similar when comparing their number of orders to profit but very different when comparing their profit to total sales value.
    """)
    return


@app.cell
def _(x_dropdown, y_dropdown):
    mo.hstack([x_dropdown,y_dropdown],gap=1,align="center")
    return


@app.cell
def _(centers, clusters, color_map, x_dropdown, y_dropdown):

    x_y_scatter = px.scatter(clusters, 
                    x=x_dropdown.value, 
                    y=y_dropdown.value, 
                    color='ClusterName',
                    opacity=0.5,
                    title='Customer Types',
                    color_discrete_map=color_map,
                    width=1000, height=600)

    for _, row2 in centers.iterrows():
        x_y_scatter.add_trace(
            go.Scatter(
                x=[row2[x_dropdown.value]],
                y=[row2[y_dropdown.value]],
                mode="markers",
                marker=dict(
                    color=color_map[row2["ClusterName"]],
                    size=100,
                    opacity=0.2,
                    symbol="circle"
                ),
                name=f"Center {row2['ClusterName']}",
                showlegend=False
            )
        )

    x_y_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                                     font=dict(size=14),
                                     margin=dict(t=100, b=50, l=50, r=50),
                                     legend_title_text="Cluster Name")
    mo.ui.plotly(x_y_scatter, config={"displayModeBar": False})
    return


@app.cell
def _():
    mo.md(r"""
    The cluster + center combo tells the truth about our buyers, which is that they have rough categories but also there are outliers in each category. In some ways their behaviors overlap and in others each group is pretty distinct.

    These kinds of complex charts should be used with care, they can be hard to read and usually need some story-telling to make them make sense, but they're powerful tools to tease apart complicated topics.

    One strategy might be to use callout sections from this chart, another might be to follow it up with simpler charts or infographics that show the clusters without the busy-ness scatterplot points. Always do what helps you tell your story and the reader or listener understand it.
    """)
    return


@app.cell
def _():
    mo.Html("<hr>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## The Survey Results

    A common type of data story in design consulting is sharing the results of a user survey. Whether it's a quantitative survey or qualitative interviews, results might be presented in a scale like "Going well", "Not going well", and "Undecided". The goal of the visualization is to show how different research categories are doing across these scale options. Readers might want to compare what's going "most well" across all categories but they also might want to quickly understand how an individual category is doing.
    """)
    return


@app.cell
def _():
    toggle_stacked_bar_labels = mo.ui.switch(label="Toggle bar labels", value=False)
    return (toggle_stacked_bar_labels,)


@app.cell
def _(toggle_stacked_bar_labels):
    _message = my_utils.callout_neutral("At first glance, it might be easy to get a relative idea of the composition of each research category without bar labels, but are you able to easily compare values of the \"Undecided\" scale level? <b>How does adding bar labels change how you read this chart?</b> How does it impact your ability to <b>quickly gather insights?</b>")

    mo.hstack([_message,toggle_stacked_bar_labels],gap=2,align="center",widths=[2,.75])
    return


@app.cell
def _(toggle_stacked_bar_labels):
    _research_phases = [
        "Strategy & Intake",
        "Analysis & Requirements",
        "Development",
        "Quality & Testing",
        "Deployment & Release",
        "Operate & Measure"
    ]

    _research_rng = np.random.default_rng(42)
    _research_going_well = _research_rng.uniform(0.50, 0.70, size=len(_research_phases))
    _research_remaining = 1 - _research_going_well
    _research_undecided_share = _research_rng.uniform(0.45, 0.55, size=len(_research_phases))
    _research_undecided = _research_remaining * _research_undecided_share
    _research_not_going_well = _research_remaining - _research_undecided

    research_df = pd.DataFrame(
        {
            "Phase": _research_phases,
            "Going well": _research_going_well,
            "Undecided": _research_undecided,
            "Not going well": _research_not_going_well,
        }
    )

    research_color_map = {
        "Going well": "#4442e3",
        "Undecided": "#D2D2D2",
        "Not going well": "#ff584e",
    }

    _research_fig = go.Figure()

    for _research_status in ["Going well", "Undecided", "Not going well"]:
        _research_fig.add_trace(
            go.Bar(
                y=research_df["Phase"],
                x=research_df[_research_status],
                name=_research_status,
                orientation="h",
                marker=dict(color=research_color_map[_research_status]),
                text=research_df[_research_status] if toggle_stacked_bar_labels.value else None,
                texttemplate="%{text:.1%}" if toggle_stacked_bar_labels.value else None,
                textposition="inside" if toggle_stacked_bar_labels.value else None,
                textfont=dict(size=14) if toggle_stacked_bar_labels.value else None,
                insidetextanchor="middle",
                hovertemplate=(
                    "Phase=%{y}<br>"
                    + _research_status
                    + "=%{x:.1%}"
                    + "<extra></extra>"
                ),
            )
        )

    _research_fig.update_layout(
        barmode="stack",
        bargap=0.25,
        height=450,
        xaxis_title=None,
        yaxis_title=None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            title="",
            xanchor="left",
            x=-.02,
            font=dict(size=16,weight="bold"),
            traceorder="normal"
        ),
    )

    _research_fig.update_xaxes(
        tickformat="1%",
        range=[0, 1],
        gridcolor="#888888"
    )

    _research_fig.update_yaxes(
        ticksuffix="   ",
        tickfont=dict(size=14,weight="bold"),
        automargin=True
    )

    mo.ui.plotly(_research_fig, config={"displayModeBar": False})
    return research_color_map, research_df


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Now compare the chart above to the "faceted" version below, where each status category gets its own facet or subchart. Thanks to the left-alignment of all columns, our eyes are immediately drawn to larger values and we can more easily gather insights about the "Undecided" level of the scale. **Compared to the version above, this version provides enhanced vertical scanning but has reduced emphases on composition.** Both versions are helpful depending on the data you're trying to highlight!
    """)
    return


@app.cell
def _(research_color_map, research_df):
    from plotly.subplots import make_subplots

    status_order = ["Going well", "Undecided", "Not going well"]

    status_facets_fig = make_subplots(
        rows=1,
        cols=len(status_order),
        shared_yaxes=True,
        horizontal_spacing=0.06,
        subplot_titles=status_order,
        column_widths=[3, 1, 1],
    )

    _phase_count = len(research_df["Phase"])

    for i, status_name in enumerate(status_order, start=1):
        status_facets_fig.add_trace(
            go.Bar(
                y=research_df["Phase"],
                x=research_df[status_name],
                orientation="h",
                marker=dict(color=research_color_map[status_name]),
                text=research_df[status_name],
                texttemplate="%{text:.1%}",
                textposition="outside",
                textfont=dict(size=14),
                cliponaxis=False,
                hovertemplate=(
                    "Status=" + status_name + "<br>"
                    + "Phase=%{y}<br>"
                    + "Share=%{x:.1%}"
                    + "<extra></extra>"
                ),
                showlegend=False,
            ),
            row=1,
            col=i,
        )

    # line separators
    for _sep in range(_phase_count - 1):
        status_facets_fig.add_shape(
            type="line",
            x0=0,
            x1=1,
            xref="paper",
            y0=_sep + 0.5,
            y1=_sep + 0.5,
            yref="y",
            line=dict(color="#D9D9D9", width=.75),
            layer="below",
        )

    status_facets_fig.update_xaxes(visible=False)

    status_facets_fig.update_yaxes(
        title=None,
        ticksuffix="   ",
        automargin=True,
        tickfont=dict(size=14, weight="bold"),
    )

    status_facets_fig.update_layout(
        height=475,
        bargap=0.25,
        margin=dict(t=30, b=0),
        showlegend=False,
    )

    status_facets_fig.update_annotations(font_size=16, font_weight="bold")

    mo.ui.plotly(status_facets_fig, config={"displayModeBar": False})
    return


if __name__ == "__main__":
    app.run()
