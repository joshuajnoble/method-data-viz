# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "pandas",
#     "plotly"
# ]
# ///
import marimo as mo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

__generated_with = "0.19.7"
app = mo.App(width="medium")

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
    import marimo as mo
    import pandas as pd
    import plotly.express as px

    @mo.cache
    def get_yearly():

        path_to_csv = mo.notebook_location() / "public" / "yearly_sales.csv"
        yearly = pd.read_csv(path_to_csv)
        yearly['Order Date'] = pd.to_datetime(yearly['Order Date'])
        yearly['year'] = yearly['year'].astype(str)
        return yearly

    @mo.cache
    def get_yearly_by_segment():

        path_to_csv = mo.notebook_location() / "public" / "yearly_sales_by_segment.csv"
        yearly_by_segment = pd.read_csv(path_to_csv)
        return yearly_by_segment
    
    @mo.cache
    def get_weekly_by_segment():

        path_to_csv = mo.notebook_location() / "public" / "weekly_sales_by_segment.csv"
        weekly_sales_by_segment = pd.read_csv(path_to_csv)
        return weekly_sales_by_segment
    
    return (mo,)


if __name__ == "__main__":
    app.run()