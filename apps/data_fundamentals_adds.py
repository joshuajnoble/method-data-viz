# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.21.1",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


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


@app.cell
def _(mo):
    _date_picker = mo.md("{start} → {end}").batch(
        start=mo.ui.date(label="Start Date", value ="2026-01-01"),
        end=mo.ui.date(label="End Date", value ="2026-02-01")
    )
    _dropdown = mo.ui.dropdown(options=["All Locations", "Charlotte, NC", "London, UK", "New York, NY", "Santa Clara, CA", "Atlanta, GA"], label="Choose location", value="All Locations")

    mo.hstack([_date_picker, _dropdown], align="center", gap=2, widths=[.5, .5])
    return


if __name__ == "__main__":
    app.run()
