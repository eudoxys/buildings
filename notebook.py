import marimo

__generated_with = "0.23.9"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This notebook provides access to the building inventory.
    """)
    return


@app.cell
def _(mo):
    url_ui = mo.ui.text(label="Data source:",value="https://s3.us-east-1.amazonaws.com/buildings.eudoxys.com/",full_width=True)
    url_ui
    return (url_ui,)


@app.cell
def _(mo, os, pd, url_ui):
    with mo.status.spinner("Reading building index"):
        files = pd.read_csv(os.path.join(url_ui.value,"index.csv"),
                           index_col=["country","state","county"])
    return (files,)


@app.cell
def _(files, mo):
    _countries = sorted(files.index.get_level_values(0).unique())
    country_ui = mo.ui.dropdown(label="Country:",options=_countries,value="US")
    return (country_ui,)


@app.cell
def _(country_ui, files, mo):
    _states = sorted(files.loc[country_ui.value].index.get_level_values(0).unique())
    state_ui = mo.ui.dropdown(label="State:",options=_states,value=_states[0])
    return (state_ui,)


@app.cell
def _(country_ui, files, mo, state_ui):
    _counties = sorted(files.loc[country_ui.value,state_ui.value].index.get_level_values(0).unique())
    county_ui = mo.ui.dropdown(label="County:",options=_counties,value=_counties[0])
    return (county_ui,)


@app.cell
def _(mo):
    google_ui = mo.ui.checkbox(label="Link to Google Earth",value=False)
    geohash_ui = mo.ui.checkbox(label="Link to Geohash Explorer",value=False)
    return geohash_ui, google_ui


@app.cell
def _(country_ui, county_ui, google_ui, mo, state_ui):
    mo.hstack([country_ui,state_ui,county_ui,
               google_ui,
               # geohash_ui,
              ],justify='start')
    return


@app.cell
def _(country_ui, county_ui, files, mo, pd, state_ui):
    with mo.status.spinner("Reading data"):
        data = pd.read_csv(files.loc[country_ui.value,state_ui.value,county_ui.value].url.replace(" ","+"))
    return (data,)


@app.cell
def _(data, geohash_ui, google_ui, mo):
    if google_ui.value:
        with mo.status.spinner("Linking to Google Earth"):
            data["google"] = [f"https://earth.google.com/web/search/{str(x.latitude).replace('.','%2e')},{str(x.longitude).replace('.','%2e')}" for _,x in data.iterrows()]

    if geohash_ui.value:
        with mo.status.spinner("Linking to Geohash Explorer"):
            data["geohash"] = [f"https://geohash.softeng.co/{x.location}" for _,x in data.iterrows()]

    with mo.status.spinner("Loading table"):
        _columns = ["location","buildingtype","buildingcode","floorarea","floors","climatezone"]
        if google_ui.value:
            _columns.append("google")
        # elif geohash_ui.value:
        #     _columns.append("geohash")
        # else:
        #     _columns.extend(["latitude","longitude"])
        table_ui = mo.ui.table(data[_columns],selection="single")
    table_ui
    return (table_ui,)


@app.cell
def _(mo, table_ui):
    if len(table_ui.value) > 0:
        _frame = mo.iframe(f"https://geohash.softeng.co/{table_ui.value.location.values[0][:9]}") 
    else:
        _frame = mo.md("<font color=blue>HINT: select a building from the table above</font>")
    _frame
    return


@app.cell
def _():
    import marimo as mo
    import os
    import pandas as pd

    return mo, os, pd


if __name__ == "__main__":
    app.run()
