# /// script
# dependencies = ["marimo"]
# requires-python = ">=3.13"
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium", css_file="custom.css")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # External Resources

    A curated guide of external resources to further your learning. These resources cover foundational data visualization concepts, chart selection guidance, community newsletters, and inspiring examples.

    ---

    ## Intro to Data Visualization

    - [**Online Book:** Fundamentals of Data Visualization by Claus O. Wilke](https://clauswilke.com/dataviz/)

    - [**Online Courses:** Open Visualization Academy by Alberto Cairo](https://openvisualizationacademy.org/)

    - [**Online Book and Lectures:** Visualization Analysis and Design by Tamara Munzner](https://www.cs.ubc.ca/~tmm/vadbook/)

    - [**Book:** Storytelling with Data by Cole Nussbaumer Knaflic](https://www.storytellingwithdata.com/books)

    - [**Book:** The Functional Art by Alberto Cairo](https://www.amazon.com/gp/product/0321834739)

    - [**Book:** Better Data Visualizations by Jonathan Schwabish](https://policyviz.com/pv_books/better-data-visualizations-a-guide-for-scholars-researchers-and-wonks/)

    ---

    ## Picking a Chart

    - [**Interactive Decision Tree:** From Data to Viz](https://www.data-to-viz.com/)

    - [**Library of Visualization Types:** The Data Visualisation Catalogue](https://datavizcatalogue.com/)

    - [**Vendor Resource:** Which Chart Type to Use — Datawrapper](https://www.datawrapper.de/blog/chart-types-guide)

    - [**Library of Visualization Types:** Visual Vocabulary — Financial Times](https://ft-interactive.github.io/visual-vocabulary/)

    - [**Book:** Practical Charts by Nicholas Desbarats](https://www.practicalreporting.com/practical-charts-book)

    ---

    ## Newsletters

    - [**Email Newsletter:** The Visualising Data Newsletter by Andy Kirk](https://visualisingdata.com/newsletter/)

    - [**Substack:** FILWD by Enrico Bertini](https://filwd.substack.com/)

    - [**Substack:** The PolicyViz Newsletter by Jonathan Schwabish](https://jschwabish.substack.com/)

    ---

    ## Work Examples

    - [**Awards:** Information is Beautiful Awards](https://www.informationisbeautifulawards.com/)

    - [**Digital Publication:** The Pudding](https://pudding.cool/)
    """)
    return


if __name__ == "__main__":
    app.run()
