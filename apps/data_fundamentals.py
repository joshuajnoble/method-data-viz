# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "marimo",
#     "plotly",
#     "pandas",
#     "numpy",
#     "scipy",
#     "itables",
#     "anywidget"
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(
    width="medium",
    css_file="custom.css",
    html_head_file="head.html",
)


@app.cell
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
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    from itables.widget import ITable

    cell_width = 800

    df_format_mapping = {
        "Order Date": "{:%Y-%m-%d}",
        "Sales": "${:,.2f}",
        "Profit": "${:,.2f}",
        "Cost": "${:,.2f}",
        "Profit Ratio (Calculated)": "{:.1%}",
        "Per Unit Profit (Calculated)": "${:,.2f}",
        "Items In Order": "{:,.0f}",
    }
    return df_format_mapping, mo, pd, px


@app.cell
def _(mo):
    mo.md(r"""
    # What is data?

    Making charts and reading charts is all about understanding data. For instance, the total dollar amount of a sale is a numeric value. We can easily compare it to other sales, add and subtract it from other sales.

    There are two fundamental kinds of numeric data:
    """)
    return


@app.cell
def _(mo):
    _img = mo.Html("<div style='font-size:2.12rem;'>💻 💻 💻 💻 💻</div>")
    mo.hstack([_img,mo.md("**Discrete Data**: These are things that cannot be divided, such as the number of items that someone bought or the number of customers who purchased an item. Think of a laptop: practically speaking, half a laptop isn't a laptop any more. There's either one laptop or zero laptops.")], align="center", widths=[.25,1],gap = 2)
    return


@app.cell
def _(mo):
    _slider = mo.ui.slider(start=-20.0, stop=40.0, step=.1, value=10.3, label="Today's Temperature (°C)", full_width=True, show_value=True)
    mo.hstack([_slider,mo.md("**Continuous Data**: These are things that can be divided into smaller and smaller units for more precision, like the weight of an item or exact instant that someone bought an item, though you don't typically see those in micrograms or nanoseconds.")],align="center", gap=2, justify="center",widths=[.25,1])
    return


@app.cell
def _(mo):
    mo.md(r"""
    The name of an item that someone bought though, is a categorical value.
    """)
    return


@app.cell
def _(mo):
    _img = mo.Html("<div style='font-size:2.12rem; text-align:center;'>🍎 🥝 🍇 🍊 🍉</div>")
    mo.hstack([_img,mo.md("**Unordered Categorical:** These aren't inherently sortable. Staplers aren't before or after monitors. We can sort these but we're using a feature of the category, like the first letter of the name or the price, rather than something inherent to the category itself.")],align="center", gap=2, justify="center",widths=[.25,1])
    return


@app.cell
def _(mo):
    _img = mo.Html("<div style='font-size:2.12rem; font-weight:bold; text-align:center;'>S→M→L→XL</div>")
    mo.hstack([_img,mo.md("**Ordered Categorical:** That's something like comparing t-shirt sizes: Small, Medium, Large, Extra-Large. We may not know a number associated with these categories but we know that Small is less than Large and Extra-Large is bigger than Medium.")],align="center", gap=2, justify="start",widths=[.25,1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Working with data

      Most of the time visualizations are meant to highlight the result of some operation on a set of data. Most of these operations are done before you visualize data, but many can be feature of dashboards or interactive visualizations. The point of visualizing data is to make these operations easier to understand.
      If humans could automatically parse the cells in an Excel, we'd never use charts, but that's just not how our brains work. There are many many kinds of things that people do with data but it's important to understand the most common because that's what most of us need to communicate and to understand.

      One nice thing about living in a world of charts is that most of these things are really familiar to us, even if the terms aren't. You've already seen these dozens of times because you've already seen and perfectly understood charts that use them.

      **If you can read a chart, you can mentally do the data work that went into making it.**

      When we work with data, usually we are picking one field of some data and using to inform our view of other fields. When a sale happened can be as informative and what it purchased or how the total sale amount.

    ## Filtering

      This means looking at something like "sales in New York City" or "all computer purchases on Jan 12, 2025". Almost any chart you've ever seen does this. You filter out items to try to find insights about a specific category of items or range of numeric or temporal values. This can be static, "here are sales from Asia", or interactive, "select which region you want to see sales from".
    """)
    return


@app.cell
def _(mo):
    date_picker_filter = mo.md("{start} → {end}").batch(
        start=mo.ui.date(label="Start Date", value ="2012-01-01"),
        end=mo.ui.date(label="End Date", value ="2012-01-08")
    )
    dropdown_filter = mo.ui.dropdown(options=["All locations", "Charlotte", "London", "New York City", "Santa Clara", "Atlanta"], label="Choose Location", value="All locations")

    mo.hstack([date_picker_filter, dropdown_filter], align="center", gap=2, widths=[.5, .5])    
    #dropdown_filter
    return date_picker_filter, dropdown_filter


@app.cell
async def _(date_picker_filter, dropdown_filter, mo, my_utils, pd):
    #_ = _dropdown
    fundamentals = await my_utils.gh_pages_read_csv_into_df("data_fundamentals.csv")
    fundamentals['Order Date'] = pd.to_datetime(fundamentals['Order Date'])
    fundamentals = fundamentals.rename({"Quantity":"Items In Order"}, axis=1)
    fundamentals = fundamentals.reset_index()
    filtered_df = (
        fundamentals if dropdown_filter.value == "All locations" else fundamentals[fundamentals["City"] == dropdown_filter.value]
    )

    filtered_df = filtered_df[["Order ID", "Order Date", "Ship Mode", "Region", "Category", "Sub-Category", "Product ID", "Sales"]]

    filtered_df = filtered_df[(filtered_df['Order Date'].dt.date > date_picker_filter['start'].value) & (filtered_df['Order Date'].dt.date < date_picker_filter['end'].value)]

    # mo.ui.table(data=filtered_df, pagination=True, show_column_summaries=False, show_data_types=False, show_download=False, selection=None)
    mo.md(filtered_df.to_markdown())
    #ITable(filtered_df)
    return (fundamentals,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Sorting

      This means arranging values according to one or more variables, for instance, individual sales ranked from highest dollar amount to lowest. You've seen this when you looked at the standings of teams in a league or sorted by cost at an retailers website. When you sort data, you give an ordering that it doesn't naturally contain,
      so it's important to make sure that you know what fields you're sorting on. Putting a classroom of students in order by age is different ordering them by height or grade point average. The point of sorting is to see how one feature of the data relates
      to others.
    """)
    return


@app.cell
def _(mo):
    name_up = mo.ui.run_button(label="Name ⬆️", full_width=True)
    name_down = mo.ui.run_button(label="Name ⬇️", full_width=True)

    sales_up = mo.ui.run_button(label="Sales ⬆️", full_width=True)
    sales_down = mo.ui.run_button(label="Sales  ⬇️", full_width=True)
    return name_down, name_up, sales_down, sales_up


@app.cell
def _(mo, my_utils, name_down, name_up, sales_down, sales_up):
    #my_utils.callout_neutral("Click the field headers to sort the table below")

    buttons = mo.vstack([name_up, name_down, sales_up, sales_down])

    mo.hstack([my_utils.callout_neutral("The buttons to the right sort the table below. Sorting names is done alphabetically, sorting numbers is done numerically."), buttons],gap=1,align="center")
    return


@app.cell(hide_code=True)
def _(fundamentals, mo, name_down, name_up, sales_down, sales_up):
    sorting_df = fundamentals[["Customer Name", "Order Date", "Ship Mode", "Product ID", "Sales"]].copy()

    if name_up.value:
        sorting_df = sorting_df.sort_values(by='Customer Name', ascending=True)
    elif name_down.value:
        sorting_df = sorting_df.sort_values(by='Customer Name', ascending=False)
    elif sales_up.value:
        sorting_df = sorting_df.sort_values(by='Sales', ascending=True)
    elif sales_down.value:
        sorting_df = sorting_df.sort_values(by='Sales', ascending=False)

    sorting_df['Sales'] = "$" + sorting_df['Sales'].round(2).astype(str)

    #ITable(sorting_df, classes="display nowrap", style="table-layout:auto;width:100%;float:left", ordering=False, layout={'topEnd': None})
    mo.md(sorting_df.to_markdown())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Aggregating

    This goes along with filtering. Usually when we look at "sales in New York City" we say something like "all sales in New York City". Any bar chart you've ever seen is aggregating. When we aggregate, we group information about an event by one of its values to reduce what we're looking at. That can be simple, like adding together all the sales, or complicated, like grouping together all sales to East Asia except Korea by category to compare monitor sales to projector sales. Aggregation often gets combined with other operations:

    - **Find the biggest sales and sort them.**
    - **Find the least expensive items to ship that are consumer electronics.**
    - **Find the average order amount in December vs April.**

    By combining different operations, we can use visualization to explore for ourselves and communicate what we've learned to others.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    multiselect_aggregate = mo.ui.multiselect(options=["Charlotte", "London", "New York City", "Santa Clara", "Atlanta"], label="Choose location(s)")
    multiselect_aggregate
    return (multiselect_aggregate,)


@app.cell(hide_code=True)
def _(fundamentals, mo, multiselect_aggregate):
    count = len(fundamentals[fundamentals["City"].isin(multiselect_aggregate.value)])
    total = fundamentals[fundamentals["City"].isin(multiselect_aggregate.value)]["Sales"].sum()

    mo.md(
        f"""
        ##**Aggregated Number of Sales:** {count}
        ##**Aggregated Total Sales:** ${total:,.0f}
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Feature Engineering

      Any time you've seen a line chart showing "profit" or "Annual Run Revenue" or, for NFL fans, "Quarterback Rating", you've understood this. It's a number made from other numbers.
      Often times the information about filtered or aggregated values alone isn't quite enough, sometimes we need to make up new kinds of information. An easy example is profit: purchase price minus cost to seller. Profit margin is just profit divided by sales.
      Complex metrics like Annual Run Rate are made from aggregating and filtering data. These are new features built from existing data. Building new feature is a part of telling a story about what your data could be telling you.

      In the table below there are 2 new "features" (aka values) being calculated:

    - **Profit Ratio** which is just `Profit` divided by `Sales`
    - **Per Unit Profit** which is just `Profit` divided by `Items In Order`

     These sorts of features help us use our data to tell a story about what's important: which orders have the highest profit ratio and thus might be interesting to a business needing to make money, and which orders might seem to have a profit but actually are just lots of small profits on many items added up.
    """)
    return


@app.cell(hide_code=True)
def _(df_format_mapping, fundamentals, mo):
    fundamentals.reset_index(inplace=True)
    features = fundamentals[["Order ID", "Sales", "Profit", "Items In Order"]]
    features["Cost"] = round(features['Sales'] - features['Profit'], 2)
    features.insert(2, 'Cost', features.pop("Cost"))

    features["Profit Ratio (Calculated)"] = round(features['Profit'] / features['Sales'], 3)
    features["Per Unit Profit (Calculated)"] = round(features['Profit'] / features['Items In Order'], 2)
    features.insert(4, 'Profit Ratio\n(Calculated)', features.pop("Profit Ratio (Calculated)"))
    features.insert(6, 'Per Unit Profit\n(Calculated)', features.pop("Per Unit Profit (Calculated)"))

    def style_cell(_rowId, _columnName, value):
        if "(Calculated)" in _columnName:
            return {"backgroundColor": "#D9DCFA"}
        else:
            return {}

    mo.ui.table(
        data=features.reset_index(drop=True),
        pagination=True,
        show_column_summaries=False,
        show_data_types=False,
        show_download=False,
        selection=None,
        format_mapping=df_format_mapping,
        style_cell=style_cell
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Distributions

    A distribution shows the range of values for a variable and how often they occur. For instance, imagine that you're looking at the heights of 11 year old students in a classroom in centimeters. Just looking at the numbers isn't all that helpful:

        147,164,139,155,141,141,143,150,150,151,153,156,157,148,159,163,167,171

    You could sort them so you can see the highest and lowest:

        139,141,141,143,147,148,150,150,151,153,155,156,157,159,163,164,167,171

    That's helpful. We could find the average height:

        153

    But that kind of misses that most students are in the middle and a few are much shorter and a few much taller. You might group the heights into ranges and see how the heights are _distributed_.

    - 135-145 = 4 students
    - 145-155 = 7 students
    - 155-165 = 5 students
    - 165-175 = 2 students

    That's called a distribution and it shows how a range of all the values and how likely they are to occur.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## What do I need to know about these?

      You don't need to be a data analyst or data scientist to do data visualization well. However, understanding what people have done to create certain views into data or how insights might come from certain operations on that data is very helpful to communicate effectively.
      Data is made, not found, and knowing _how_ it's made helps you know how to use it effectively.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Stages of data work

      Most of the time, when we're working with data we have a few different stages of doing so: we **explore**, we **diagnose**, and then we **explain**.
      At first, we're just trying to understand what the data is and what things we might be able to learn from it. Is the sales data complete? Can we join it with other data sources like how much stock is at our suppliers or global prices?
      These kinds of visualizations are open-ended and iterative and often involve many quick visualizations and are focused on our own learning or sharing with our team rather than communicating with an audience.

      Once we understand what the data is and what it might tell us, then we can diagnose whether what we think is happening is actually there. Do profits have a monthly cycle? Are orders in EMEA growing faster than in LATAM? Is the information reliable and does it communicate an insight?
      This process often involves using multiple kinds of transformations and views of the data to test a hypothesis.

      If we believe in the insight and understand the data that supports it, we should communicate that insight. We want to use the minimal number of charts to communicate our idea.  Here, the design is of paramount importance.
      Typically each visualization is focused on one single message for the audicen. We should ask ourselves, and be prepared to answer questions like: "What is the key insight?", "What evidence supports it?", "What should be done?"
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    # What is Data for?

    Data is for _insights_

    What's the point of gathering data in the first place? Well, hopefully to tell you something informative. Did it freeze last night? Does this drug work? Can I retire?

    Visualizing data, aka making charts, is to help people to derive insights from data or to help people contextualize insights and make decisions based on them.

    Much like good design helps people do things, good charts help people understand things. The point of making a chart isn't to make a cool chart, it's to make an aid to understanding.

    ## Charts tell a story

    You have probably made hundreds of bar charts in your life. Maybe even thousands. But why did you make them? What was the point? Why do they work? Why are charts so useful? Moreover, what makes some more useful than others?

    This site is an attempt to demonstrate a little bit of why we visualize data, show some of the principles of what visualizing data is about, and to show examples of how different kinds of data can and should be visualized.

    Let's start with the simplest of charts, the bar chart. In a later section of this, we'll dive much more deeply into these, but for right now, they're a great place to start thinking about thinking with data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sales Per Year (Bar Chart)
    """)
    return


@app.cell
async def _(mo, my_utils, px):

    yearly_sales = await my_utils.gh_pages_read_csv_into_df("yearly_sales.csv")
    yearly_sales.sort_values("year", inplace=True)
    yearly_sales['year'] = yearly_sales['year'].astype('str')
    yearly_sales_fig_labeled = px.bar(yearly_sales, x='year', y='sales', labels={"year": "Financial Year","sales": "Total Sales in USD ($)"})

    yearly_sales_fig_labeled = px.bar(yearly_sales, x='year', y='sales', labels={"year": "Financial Year","sales": "Total Sales in USD"})

    yearly_sales_fig_labeled.update_layout(yaxis_tickprefix = '$', yaxis_tickformat = ',.2s')
    yearly_sales_fig_labeled.update_yaxes(tickformat=".2s") 
    mo.ui.plotly(yearly_sales_fig_labeled,config={"displayModeBar": False})
    return (yearly_sales,)


@app.cell
def _(mo):
    mo.md("""
    The height of a bar shows the yearly sales. The point of it is to show how the different years compare to one another. The higher the bar, the more sales.
    Note that we know what we're measuring, _sales_, what units it's in, _USD_, and what sections are being used to measure, _years_.
    We've all made lots of these in our lives and they work because we humans can easily compare the heights of two things.

    The purpose of visualizing data is to tell a story. What's the story that you're trying to tell?

    Here the story is that 2014 was a stronger year than any of the previous years. We can see that easily because we can compare the heights of objects easily.

    However, if our goal is show the _trend_, then a line shows a trend better than a bar.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sales Per Year (Line Chart)
    """)
    return


@app.cell
def _(mo, px, yearly_sales):

    yearly_line = px.line(yearly_sales, x="year", y="sales", labels={"year": "Financial Year","sales": "Total Sales in Millions ($)"}, title='Sales Per Year in Millions of USD')
    yearly_line.update_traces(mode='lines+markers')
    yearly_line.update_yaxes(tickformat="$,.2s")

    mo.ui.plotly(yearly_line,config={"displayModeBar": False})
    return


@app.cell
def _(mo):
    mo.md("""
    Picking the right chart depends on the story that you're trying to tell but it also depends on what kinds of data transformations you can (and can't) do with the data.

    The bar chart and the line chart shown here both use the exact same data, there's no need to make more changes in order to show one or the other. However, getting to the point of being able to show this data is a little tricky.

    We have to answer two questions first:

    > 1. What are all the years in our dataset?
    > 2. For each year, what is the total sum of sales?

    Those operations can happen in Excel, in code, you could even do them by hand with a calculator if you felt like it. The point isn't so much how they get done as they're both what the chart is showing and what the data looked like before the chart could be created. The sales data underlying those charts looks like this:

    |   Row ID | Order ID       | Order Date   | Ship Date   | Ship Mode    | Customer ID   | Customer Name   | Segment   |   Sales |
    |---------:|:---------------|:-------------|:------------|:-------------|:--------------|:----------------|:----------|--------:|
    |    32298 | CA-2012-124891 | 7/31/12      | 7/31/12     | Same Day     | RH-19495      | Rick Hansen     | Consumer  | $2,309.65 |
    |    26341 | IN-2013-77878  | 2/5/13       | 2/7/13      | Second Class | JR-16210      | Justin Ritter   | Corporate | $3,709.39 |
    |    25330 | IN-2013-71249  | 10/17/13     | 10/18/13    | First Class  | CR-12730      | Craig Reiter    | Consumer  | $5,175.17 |

    This might look a little overwhelming at first but to get to the data that we're interested in, we're going to ignore most of it. All we care about is the year in the Order Date column and the Sales. Everything else doesn't matter for our chart or the story we're trying to tell.

    To get to the data that we need for our bar chart, we get the date from every row (and in this dataset there are more than 50,000) and depending on the year, add it to the running total for that year. That's both what the chart shows and what the data we need is.

    This is important to understand becuase visualizing data really is manipulating it, that's actually what's going on when you make a chart. Again, that doesn't mean that you need to be a data scientist to make beautiful and meaningful visualizations. It means that if you've been reading charts, you already know how to do most of these things, conceptually speaking at least.

    Visualizing data well isn't about showing all the data or even knowing all of the data, it's about knowing what you're interested in and how to communicate that effectively to your audience.
    """)
    return


if __name__ == "__main__":
    app.run()
