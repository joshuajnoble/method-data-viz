# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "altair==5.4.1",
#     "marimo",
#     "vega-datasets==0.9.0",
# ]
# ///

import marimo as mo

__generated_with = "0.19.7"
app = mo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    
    return (mo,)

@app.cell(hide_code=True)
def __(mo):
    mo.md("""
          
        # What is data?

        Making charts and reading charts is all about understanding data. For instance, the total dollar amount of a sale is a numeric value. We can easily compare it to other sales, add and subtract it from other sales.

        There are two fundamental kinds of numeric data:
          
        - Discrete Data: These are things that cannot be divided, such as the number of items that someone bought or the number of customers who purchased an item. Think of a laptop: practically speaking, half a laptop isn't a laptop any more. There's either one laptop or zero laptops.
        - Continuous Data: These are things that can be divided into smaller and smaller units for more precision, like the weight of an item or exact instant that someone bought an item, though you don't typically see those in micrograms or nanoseconds.
          
        The name of an item that someone bought though, is a categorical value. 
          
        - Unordered Categorical: These aren't inherently sortable. Staplers aren't before or after monitors. We can sort these but we're using a feature of the category, like the first letter of the name or the price, rather than something inherent to the category itself.
        - Ordered Categorical: That's something like comparing t-shirt sizes: Small, Medium, Large, Extra-Large. We may not know a number associated with these categories but we know that Small is less than Large and Extra-Large is bigger than Medium.
    
        Understanding how these types of data differ and can be combined is important to communicating clearly about them and helping people derive insights from that data.

        Any event has multiple kinds of data associated with it. For instance, an online sale has a time, an amount, a thing purchased, where it was sent to, shippping costs, profit to the company. 
          All of these are part of the sale but looking at each of them individually rarely tells much about them. Data becomes meaningful when you use it to get insights. How are sales specifically to Australia changing year over year? Which category of product is growing fastest? What kinds of sales lose the most money?
          These important questions for a business and helping to ask and answering them is why we visualize data.

          """)
    return

@app.cell(hide_code=True)
def __(mo):
    mo.md("""
          
        # Working with data

          Most of the time visualizations are meant to highlight the result of some operation on a set of data. Most of these operations are done before you visualize data, but many can be feature of dashboards or interactive visualizations. The point of visualizing data is to make these operations easier to understand.
          If humans could automatically parse the cells in an Excel, we'd never use charts, but that's just not how our brains work. There are many many kinds of things that people do with data but it's important to understand the most common because that's what most of us need to communicate and to understand.
          
        ## Filtering
          
          This means looking at all sales in New York City or all computer purchases on Jan 12, 2025. You filter out items to try to find insights about a specific category of items or range of numeric or temporal values. This can be static, "here are sales from Asia", or interactive, "select which region you want to see sales from".
          
        ## Sorting
          
          This means arranging values according to one or more variables, for instance, individual sales ranked from highest dollar amount to lowest. You've definitely seen this before. It's important to know what you can and can't sort.
          
        ## Aggregating
          
          When we aggregate, we group information about an event by one of its values to reduce what we're looking at. That can be simple, like adding together all the sales, or complicated, like grouping together all sales to East Asia except Korea by category to compare monitor sales to projector sales. 
          Aggregation often gets combined with other operations: find the biggest sales and sort them, find the least expensive items to ship that are consumer electronics, the average order amount in December vs April. 
          By combining different operations, we can use visualization to explore for ourselves and communicate to others.

        ## Feature Engineering
          
          Often times the information about filtered or aggregated values alone isn't quite enough, sometimes we need to make up new kinds of information. An easy example is profit: purchase price minus cost to seller. Profit margin is just profit divided by sales. 
          Complex metrics like Annual Run Rate are made from aggregating and filtering data. These are new features built from existing data. Building new feature

        ## What do I need to know about these?
          
          You don't need to be a data analyst or data scientist to do data visualization well. However, understanding what people have done to create certain views into data or how insights might come from certain operations on that data is very helpful to communicate effectively.
          Data is made, not found, and knowing _how_ it's made helps you know how to use it effectively.

          """)
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md("""
          
        # Stages of data work

          Most of the time, when we're working with data we have a few different stages of doing so: we explore, we diagnose, and then we explain. 
          At first, we're just trying to understnad what the data is and what things we might be able to learn from it. Is the sales data complete? Can we join it with other data sources like how much stock is at our suppliers or global prices?
          These kinds of visualizations are open-ended and iterative and often involve many quick visualizations and are focused on our own learning or sharing with our team rather than communicating with an audience.
          
          Once we understand what the data is and what it might tell us, then we can diagnose whether what we think is happening is actually there. Do profits have a monthly cycle? Are orders in EMEA growing faster than in LATAM? Is the information reliable and does it communicate an insight?
          This process often involves using multiple kinds of transformations and views of the data to test a hypothesis.

          If we believe in the insight and understand the data that supports it, we should communicate that insight. We want to use the minimal number of charts to communicate our idea.  Here, the design is of paramount importance.
          Typically each visualization is focused on one single message for the audicen. We should ask ourselves, and be prepared to answer questions like: "What is the key insight?", "What evidence supports it?", "What should be done?"

          """)
    return

if __name__ == "__main__":
    app.run()
