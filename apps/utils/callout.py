import marimo as mo

def _callout(kind: str, content: str):
    css_class = "callout-danger" if kind == "danger" else "callout-info"
    return mo.Html(f"<div class='{css_class}'>{content}</div>")

def callout_info(content: str):
    return _callout("info", content)

def callout_danger(content: str):
    return _callout("danger", content)