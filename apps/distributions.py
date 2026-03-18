# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "plotly",
#     "pandas",
#     "numpy",
#     "scipy"
# ]
# ///
import marimo as mo
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

import numpy as np

__generated_with = "0.19.7"
app = mo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    @mo.cache
    def raw_sales():

        #path_to_csv = mo.notebook_location() / "public" / "raw_sales.csv"
        path_to_csv = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/apps/public/raw_sales.csv"
        raw_sales = pd.read_csv(path_to_csv)
        return raw_sales
    
    return (mo,)

@app.cell
async def _():
    import matplotlib.pyplot as plt
    
    import plotly.express as px
    import numpy as np
    import plotly.graph_objects as go

    return (plt,)


@app.cell
def _():
    mo.md(
        """
        # Distributions
        
        A distribution shows the range of values for a variable and how often they occur. 
        For instance, imagine that you're looking at the heights of 11 year old students in centimeters. 
        You might group the heights into ranges and see how the heights are distributed.

        """
    )
    return

@app.cell
def _():
    path_to_img = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/apps/public/distribution_frame.png"
    mo.image(path_to_img)
    return

@app.cell
def _():
    mo.md(
        """
        A few are shorter. Most students are in the middle. A few are taller.

        That distribution is usually shown in a histogram like so:
        """
    )
    return

@app.cell
def _():
    #hist_plot = mo.notebook_location() / "public" / 'newplot.png'
    #mo.image(hist_plot)
    
    from scipy.stats import gaussian_kde
    df = pd.DataFrame({"value":[139,141,141,143,147,148,150,150,151,153,155,156,157,159,163,164,167,171]})

    # Create the base histogram
    demo_fig = px.histogram(df, x="value", histnorm='probability density', nbins=10)
    demo_fig.update_traces(marker_color='rgba(76, 114, 176, 0.5)', marker_line_width=1, marker_line_color="black")

    # Kernel Density Estimate
    kde = gaussian_kde(df['value'])
    x_range = np.linspace(min(df['value']), max(df['value']), 100)
    y_density = kde(x_range)

    # KDE as trace
    curve = go.Scatter(
        x=x_range,
        y=y_density,
        mode='lines',
        name='Density Estimate',
        line=dict(color='red', width=2),
        line_shape='spline' # Optional: can apply slight smoothing to the line itself
    )
    demo_fig.add_trace(curve)

    # Update layout for clarity
    demo_fig.update_layout(
        title="Heights of students",
        xaxis_title="Heights",
        yaxis_title="Density",
        showlegend=True
    )

    mo.ui.plotly(demo_fig, config={"displayModeBar": False})

    return

@app.cell
def _():
    mo.md(
        """
        ## Histogram of Sales Data

        This shows how what purchases amounts are the most common. The problem is that it's very difficult to see how the amounts of sales are distributed.
        """
    )
    return

@app.cell()
def _(mo):

    raw = raw_sales()
    fig = px.histogram(raw, x="Sales", nbins=100)
    
    fig.update_layout(
        title="Amount of Sales",
        xaxis_title="Amount of sale",
        yaxis_title="Number of sales",
        showlegend=True
    )

    # fig.show()

    # fig, ax = plt.subplots()
    # ax.hist(raw['Sales'], bins=30)
    # ax.set_title('Static Matplotlib Plot')
    # ax.legend()

    fig 
    return

@app.cell
def _():
    mo.md(
        """
        ## Height
        This shows how what kinds of amounts purchases are most common on a log scale. That means the x-axis increases from in jumps of 10x: 1, 10, 100, 1000, and so on. This helps us see that most purchases are less than $100, 
        but a few are very large. In a linear scale, it would be harder to see this distribution.
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

    # Compute bin centers and widths
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_widths = bins[1:] - bins[:-1]

    log_bin_fig = go.Figure()

    log_bin_fig.add_trace(go.Bar(
        x=bin_centers,
        y=counts,
        width=bin_widths,
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

    mo.ui.plotly(log_bin_fig, config={"displayModeBar": False})
    


if __name__ == "__main__":
    app.run()