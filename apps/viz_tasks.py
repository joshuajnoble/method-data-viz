# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "plotly",
#     "pandas",
#     "numpy"
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

    # set plotly default template and disable mode bar (copied from 'comparing_groups')
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

    def _callout(kind: str, content: str):
        css_class = "callout-danger" if kind == "danger" else "callout-info"
        return mo.Html(f"<div class='{css_class}'>{content}</div>")

    def callout_info(content: str):
        return _callout("info", content)

    def callout_danger(content: str):
        return _callout("danger", content)


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
    def get_weekly_sales():
        #path_to_csv = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/apps/public/weekly_sales_by_segment.csv"
        path_to_csv = mo.notebook_location() / "public" / "weekly_sales.csv"
        centers = pd.read_csv(path_to_csv)
        return centers
    
    return ()

@app.cell
def _():
    mo.md(
        """
        # Visualization Tasks

        Making visualizations is about telling a story but that story needs a _point_, a "why are we hearing this?". Those points have typologies, just like movies can be a comedy, horror, action, etc, data stories tend to have a broad type.

        ## The Snapshot

        One of those kinds of stories could be framed as "How are things going right now?".

        """
    )
    return



@app.cell
def _():
    mo.md(
        """
        ## The Breakdown

        Another story is "What is this made out of?" 
        
        (grouped bar chart for composition)

        """
    )
    return


@app.cell
def _():
    mo.md(
        """
        ## Fortune-teller

        We all love a "where are things going?" story. We can tell this is a popular story because of how common the 'up and to the right' line-chart is our visual culture.

        """
    )
    return


@app.cell
def _():
    
    forecasts = get_sales_forecasts()
    weeklies = get_weekly_sales()

    forecast_fig = go.Figure()

    forecast_fig.add_trace(go.Scatter(
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

    forecast_fig.add_trace(go.Scatter(
        x=weeklies['Order Date'][-26:],
        y=weeklies['sales'][-26:],
        mode='lines',
        line=dict(color='black'),
        name='Actuals'
    ))

    forecast_fig.update_traces(hovertemplate="<b>Sales:</b> %{y:$.2f}")

    return (forecasts, weeklies)

@app.cell
def _():
    mo.md(
        """

        One of the challenges of forecasting though is that you can make a prediction, but you know that there's a chance it may not be right. To express this, we often use confidcence intervals to say how likely it is that the true number will be within a range.

        In this chart we're saying that there's an 80% chance that the actual sales will be within the 80% range and a 50% chance that it will be within the 50% range.
        The median forecast is just the middle, it's not the most likely per se, it's just the middle of our forecasts.

        """
    )
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

    forecast_w_prob_fig.update_traces(hovertemplate="<b>Sales:</b> %{y:$.2f}")


@app.cell
def _():
    mo.md(
        """
        ## Causal Stories

        Let's think of this story as: "which of these things cause one another?"

        """
    )
    return

@app.cell
def _():
    return

@app.cell
def _():
    mo.md(
        """
        ## The Grouping

        Yet another story is "Which of these things are like one another?" 

        Let's take our shopper data and find some clusters of customers. We'll say that we have 4:

        * High Profit Buyers - these are customers who make the company money and don't worry too much about shopping for discounts. 'High value'
        * Bargain Hunters - these are customers who pop in for the sales, but won't buy without one.
        * The Reliable Middle - these shoppers are mid-profit, mid-frequency, and like a bargain but buy what they need even if it's not on sale.
        * Frugal Frequent Buyers - these shoppers buy often but don't make the company much profit and love a discount.

        To visualize these clusters, we'll use a scatterplot with circles around the center of the clusters. First, show how the Profit vs Number of Orders breaks down:

        """
    )
    return


@app.cell
def _():

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

    return (clusters, centers, color_map)

@app.cell
def _():
    mo.md(
        """
        Next we'll use a second scatterplot with our clusters to show how the Profit vs Percentage of Discounts breaks down:

        """
    )
    return

@app.cell
def _(clusters, centers, color_map):

    profit_x_discounts = px.scatter(clusters, 
                    x='Profit', 
                    y='Discounts', 
                    color='ClusterName',
                    opacity=0.5,
                    title='Customer Types',
                    color_discrete_map=color_map,
                    width=1000, height=600)

    for _, row2 in centers.iterrows():
        profit_x_discounts.add_trace(
            go.Scatter(
                x=[row2["Profit"]],
                y=[row2["Discounts"]],
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

    profit_x_discounts.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                                     font=dict(size=14),
                                     margin=dict(t=100, b=50, l=50, r=50),
                                     legend_title_text="Cluster Name")
    mo.ui.plotly(profit_x_discounts, config={"displayModeBar": False})
          
@app.cell
def _():
    mo.md(
        """
        
        The cluster + center combo tells the truth about our buyers, which is that they have rough categories but also there are outliers in each category. In some ways their behaviors overlap and in others each group is pretty distinct. 

        """
    )
    return


if __name__ == "__main__":
    app.run()