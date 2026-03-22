# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "marimo",
#     "plotly",
#     "pandas",
#     "numpy",
#     "scipy"
# ]
# ///

import marimo as mo
import plotly.express as px

__generated_with = "0.19.7"
app = mo.App(width="medium")



@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px

    cell_width = 800

    @mo.cache
    def get_fundamentals():

        #path_to_csv = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/apps/public/yearly_sales_by_segment.csv"
        path_to_csv = mo.notebook_location() / "public" / "data_fundamentals.csv"
        fundies = pd.read_csv(path_to_csv)
        fundies['Order Date'] = pd.to_datetime(fundies['Order Date'])
        return fundies

    @mo.cache
    def get_yearly():

        path_to_csv = mo.notebook_location() / "public" / "yearly_sales.csv"
        yearly = pd.read_csv(path_to_csv)
        yearly['Order Date'] = pd.to_datetime(yearly['Order Date'])
        yearly['year'] = yearly['year'].astype(str)
        return yearly

    return (mo,px)

# @app.cell(hide_code=True)
# def __(mo):
#     mo.md("""
          
#         # What is data?

#         Making charts and reading charts is all about understanding data. For instance, the total dollar amount of a sale is a numeric value. We can easily compare it to other sales, add and subtract it from other sales.

#         There are two fundamental kinds of numeric data:
          
#         - Discrete Data: These are things that cannot be divided, such as the number of items that someone bought or the number of customers who purchased an item. Think of a laptop: practically speaking, half a laptop isn't a laptop any more. There's either one laptop or zero laptops.
#         - Continuous Data: These are things that can be divided into smaller and smaller units for more precision, like the weight of an item or exact instant that someone bought an item, though you don't typically see those in micrograms or nanoseconds.
          
#         The name of an item that someone bought though, is a categorical value. 
          
#         - Unordered Categorical: These aren't inherently sortable. Staplers aren't before or after monitors. We can sort these but we're using a feature of the category, like the first letter of the name or the price, rather than something inherent to the category itself.
#         - Ordered Categorical: That's something like comparing t-shirt sizes: Small, Medium, Large, Extra-Large. We may not know a number associated with these categories but we know that Small is less than Large and Extra-Large is bigger than Medium.
    
#         Understanding how these types of data differ and can be combined is important to communicating clearly about them and helping people derive insights from that data.

#         Any event has multiple kinds of data associated with it. For instance, an online sale has a time, an amount, a thing purchased, where it was sent to, shippping costs, profit to the company. 
#           All of these are part of the sale but looking at each of them individually rarely tells much about them. Data becomes meaningful when you use it to get insights. How are sales specifically to Australia changing year over year? Which category of product is growing fastest? What kinds of sales lose the most money?
#           These important questions for a business and helping to ask and answering them is why we visualize data.

#           """)
#     return



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
    _slider = mo.ui.slider(start=-20, stop=40, step=1, value=10, label="Today's Temperature (°C)", full_width=True, show_value=True)
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
def __(mo):
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

@app.cell
def _(mo):
    date_picker_filter = mo.md("{start} → {end}").batch(
        start=mo.ui.date(label="Start Date", value ="2012-01-01"),
        end=mo.ui.date(label="End Date", value ="2012-02-01")
    )
    dropdown_filter = mo.ui.dropdown(options=["All Locations", "Charlotte", "London", "New York City", "Santa Clara", "Atlanta"], label="Choose location", value="All Locations")

    mo.hstack([date_picker_filter, dropdown_filter], align="center", gap=2, widths=[.5, .5])
    
    #dropdown_filter

@app.cell
def _(mo):
    #_ = _dropdown
    fundamentals = get_fundamentals()

    filtered_df = (
        fundamentals if dropdown_filter.value == "All Locations" else fundamentals[fundamentals["City"] == dropdown_filter.value]
    )

    filtered_df = filtered_df[(filtered_df['Order Date'].dt.date > date_picker_filter['start'].value) & (filtered_df['Order Date'].dt.date < date_picker_filter['end'].value)]
    mo.ui.table(data=filtered_df, pagination=True, show_column_summaries=False, show_data_types=False, show_download=False)


@app.cell(hide_code=True)
def __(mo):
    mo.md("""
        ## Sorting
          
          This means arranging values according to one or more variables, for instance, individual sales ranked from highest dollar amount to lowest. You've seen this when you looked at the standings of teams in a league or sorted by cost at an retailers website. When you sort data, you give an ordering that it doesn't naturally contain, 
          so it's important to make sure that you know what fields you're sorting on. Putting a classroom of students in order by age is different ordering them by height or grade point average. The point of sorting is to see how one feature of the data relates
          to others.
    """)


@app.cell(hide_code=True)
def __(mo):      
    mo.ui.table(data=fundamentals, pagination=True, show_column_summaries=False, show_data_types=False, show_download=False)
          
@app.cell(hide_code=True)
def __(mo):
    mo.md("""
        ## Aggregating
          
          This goes along with filtering. Usually when we look at "sales in New York City" we say something like "all sales in New York City". Any bar chart you've ever seen is aggregating. When we aggregate, we group information about an event by one of its values to reduce what we're looking at.
          That can be simple, like adding together all the sales, or complicated, like grouping together all sales to East Asia except Korea by category to compare monitor sales to projector sales. 
          Aggregation often gets combined with other operations: find the biggest sales and sort them, find the least expensive items to ship that are consumer electronics, the average order amount in December vs April. 
          By combining different operations, we can use visualization to explore for ourselves and communicate to others.
          """)
    return

@app.cell(hide_code=True)
def __(mo):
    multiselect_aggregate = mo.ui.multiselect(options=["Charlotte", "London", "New York City", "Santa Clara", "Atlanta"], label="Choose location")
    multiselect_aggregate

@app.cell(hide_code=True)
def __(mo):
    
    count = len(fundamentals[fundamentals['City'].isin(multiselect_aggregate.value)])
    total = round(fundamentals[fundamentals['City'].isin(multiselect_aggregate.value)]["Sales"].sum())

    mo.md(
        f'''
        - **Number of Sales: {count}**
        - **Total Sales: ${total}**
        '''
        )
          
@app.cell(hide_code=True)
def __(mo):
    mo.md("""
        ## Feature Engineering
          
          Any time you've seen a line chart showing "profit" or "Annual Run Revenue" or, for NFL fans, "Quarterback Rating", you've understood this. It's a number made from other numbers.
          Often times the information about filtered or aggregated values alone isn't quite enough, sometimes we need to make up new kinds of information. An easy example is profit: purchase price minus cost to seller. Profit margin is just profit divided by sales. 
          Complex metrics like Annual Run Rate are made from aggregating and filtering data. These are new features built from existing data. Building new feature is a part of telling a story about what your data could be telling you.
    """)


@app.cell(hide_code=True)
def __(mo):

    features = fundamentals[["Order ID", "Sales", "Profit", "Quantity"]]
    features["Cost"] = round(features['Sales'] - features['Profit'], 2)

    features["Profit Ratio"] = round(features['Profit'] / features['Sales'], 2)
    features["Per Unit Profit"] = round(features['Profit'] / features['Quantity'], 2)

    mo.ui.table(data=features, pagination=True, show_column_summaries=False, show_data_types=False, show_download=False)


@app.cell(hide_code=True)
def __(mo):    
    mo.md("""            
        ## What do I need to know about these?
          
          You don't need to be a data analyst or data scientist to do data visualization well. However, understanding what people have done to create certain views into data or how insights might come from certain operations on that data is very helpful to communicate effectively.
          Data is made, not found, and knowing _how_ it's made helps you know how to use it effectively.

          """)
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md("""
          
        # Stages of data work

          Most of the time, when we're working with data we have a few different stages of doing so: we **explore**, we **diagnose**, and then we **explain**. 
          At first, we're just trying to understnad what the data is and what things we might be able to learn from it. Is the sales data complete? Can we join it with other data sources like how much stock is at our suppliers or global prices?
          These kinds of visualizations are open-ended and iterative and often involve many quick visualizations and are focused on our own learning or sharing with our team rather than communicating with an audience.
          
          Once we understand what the data is and what it might tell us, then we can diagnose whether what we think is happening is actually there. Do profits have a monthly cycle? Are orders in EMEA growing faster than in LATAM? Is the information reliable and does it communicate an insight?
          This process often involves using multiple kinds of transformations and views of the data to test a hypothesis.

          If we believe in the insight and understand the data that supports it, we should communicate that insight. We want to use the minimal number of charts to communicate our idea.  Here, the design is of paramount importance.
          Typically each visualization is focused on one single message for the audicen. We should ask ourselves, and be prepared to answer questions like: "What is the key insight?", "What evidence supports it?", "What should be done?"

          """)
    return

@app.cell
def _():
    mo.md(
        """

        # What is Data for? 
        
        Data is for _insights_

        What's the point of gathering data in the first place? Well, hopefully to tell you something informative. Did it freeze last night? Does this drug work? Can I retire?

        Visualizing data, aka making charts, is to help people to derive insights from data or to help people contextualize insights and make decisions based on them.
        
        Much like good design helps people do things, good charts help people understand things. The point of making a chart isn't to make a cool chart, it's to make an aid to understanding.

        ## Charts explain what 

        You have probably made hundreds of bar charts in your life. Maybe even thousands. But why did you make them? What was the point? Why do they work? Why are charts so useful? Moreover, what makes some more useful than others?

        This site is an attempt to demonstrate a little bit of why we visualize data, show some of the principles of what visualizing data is about, and to show examples of how different kinds of data can and should be visualized.

        Let's start with the simplest of charts, the bar chart. In a later section of this, we'll dive much more deeply into these, but for right now, they're a great place to start thinking about thinking with data.
        """
    )
    return

@app.cell()
def _(mo):

    yearly_sales = get_yearly()
    yearly_sales_fig_labeled = px.bar(yearly_sales, x='year', y='sales', labels={"year": "Financial Year","sales": "Total Sales in USD ($)"})

    tick_vals = [2011, 2012, 2013, 2014]
    yearly_sales_fig_labeled.update_xaxes(
        tickmode="array",
        tickvals=tick_vals,
        ticktext=[f"{v}" for v in tick_vals]
    )
    yearly_sales_fig_labeled.update_layout(yaxis_tickprefix = 'USD$', yaxis_tickformat = ',.')
    yearly_sales_fig_labeled.update_yaxes(tickformat=".2s") 
    mo.ui.plotly(yearly_sales_fig_labeled,config={"displayModeBar": False})
    
    return (yearly_sales, tick_vals,)

@app.cell
def _():
    mo.md("""
        The height of a bar shows the yearly sales. The point of it is to show how the different years compare to one another. The higher the bar, the more sales.
        Note that we know what we're measuring, _sales_, what units it's in, _USD_, and what sections are being used to measure, _years_.
        We've all made lots of these in our lives and they work because we humans can easily compare the heights of two things.

        The purpose of visualizing data is to tell a story. What's the story that you're trying to tell?

        Here the story is that 2014 was a stronger year than any of the previous years. We can see that easily because we can compare the heights of objects easily.

        However, if our goal is show the _trend_, then a line shows a trend better than a bar.
        """
    )
    return

@app.cell()
def _(mo, yearly_sales, tick_vals):
    
    
    yearly_sales['truncated'] = yearly_sales['sales']/1_000_000

    yearly_line = px.line(yearly_sales, x="year", y="sales", labels={"year": "Financial Year","sales": "Total Sales in Millions ($)"}, title='Sales Per Year in Millions of USD')

    yearly_line.update_traces(mode='lines+markers')

    yearly_line.update_xaxes(
        tickmode="array",
        tickvals=tick_vals,
        ticktext=[f"{v}" for v in tick_vals]
    )

    yearly_line.update_yaxes(tickformat="$,.2s")

    mo.ui.plotly(yearly_line,config={"displayModeBar": False})
    return


@app.cell
def _():
    mo.md(
        """
        Picking the right chart depends on the story that you're trying to tell but it also depends on what kinds of data transformations you can (and can't) do with the data.
        
        The bar chart and the line chart shown here both use the exact same data, there's no need to make more changes in order to show one or the other. However, getting to the point of being able to show this data is a little tricky.

        We have to answer two questions first:

        1. What are all the years in our dataset?
        2. For each year, what is the total sum of sales?

        Those operations can happen in Excel, in code, you could even do them by hand with a calculator if you felt like it. The point isn't so much how they get done as they're both what the chart is showing and what the data looked like before the chart could be created. The sales data underlying those charts looks like this:

        |   Row ID | Order ID       | Order Date   | Ship Date   | Ship Mode    | Customer ID   | Customer Name   | Segment   |   Sales |
        |---------:|:---------------|:-------------|:------------|:-------------|:--------------|:----------------|:----------|--------:|
        |    32298 | CA-2012-124891 | 7/31/12      | 7/31/12     | Same Day     | RH-19495      | Rick Hansen     | Consumer  | 2309.65 |
        |    26341 | IN-2013-77878  | 2/5/13       | 2/7/13      | Second Class | JR-16210      | Justin Ritter   | Corporate | 3709.39 |
        |    25330 | IN-2013-71249  | 10/17/13     | 10/18/13    | First Class  | CR-12730      | Craig Reiter    | Consumer  | 5175.17 |

        This might look a little overwhelming at first but to get to the data that we're interested in, we're going to ignore most of it. All we care about is the year in the Order Date column and the Sales. Everything else doesn't matter for our chart or the story we're trying to tell.

        To get to the data that we need for our bar chart, we get the date from every row (and in this dataset there are more than 50,000) and depending on the year, add it to the running total for that year. That's both what the chart shows and what the data we need is.

        This is important to understand becuase visualizing data really is manipulating it, that's actually what's going on when you make a chart. Again, that doesn't mean that you need to be a data scientist to make beautiful and meaningful visualizations. It means that if you've been reading charts, you already know how to do most of these things, conceptually speaking at least.

        Visualizing data well isn't about showing all the data or even knowing all of the data, it's about knowing what you're interested in and how to communicate that effectively to your audience.

        """
    )
    return

if __name__ == "__main__":
    app.run()
