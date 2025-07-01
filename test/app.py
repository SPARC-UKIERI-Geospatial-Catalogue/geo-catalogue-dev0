from shiny import App, ui, render
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from shinywidgets import render_plotly, output_widget
import plotly.express as px
#import folium
import io
import ipyleaflet

# Mock data for tab 1 - Line Chart
dates = [datetime.now() - timedelta(days=i) for i in range(30)][::-1]
values = np.random.randint(50, 100, size=30)
line_data = pd.DataFrame({"Date": dates, "Value": values})

# Mock data for tab 2 - Data Table
data = np.random.randn(20, 5)
columns = [f"Column {i+1}" for i in range(5)]
table_data = pd.DataFrame(data, columns=columns)

# Map center coordinates for Jaipur, India
jaipur_coords = [26.9124, 75.7873]

# Mock data for tab 3 - Map (Jaipur, India) - used for plotly map only
jaipur = {"lat": 26.9124, "lon": 75.7873}
map_df = pd.DataFrame([jaipur])

# app_ui = ui.page_fluid(
#     ui.h2("Python Shiny App Example - 3 Tabs"),
#     ui.navset_tab(
#         ui.nav_panel(
#             "Line Chart",
#             output_widget("line_plot"),
#         ),
#         ui.nav_panel(
#             "Data Table",
#             ui.output_data_frame("table")
#         ),
#         ui.nav_panel(
#             "Jaipur Map",
#             ui.output_ui("leaflet_map")
#         ),
#         id="tabs"
#     )
# )

app_ui = ui.page_fluid(
    ui.h2("Python Shiny App Example - 3 Tabs (No Folium)"),
    ui.navset_tab(
        ui.nav_panel(
            "Line Chart",
            output_widget("line_plot"),
        ),
        ui.nav_panel(
            "Data Table",
            ui.output_data_frame("table")
        ),
        ui.nav_panel(
            "Jaipur Map (Plotly)",
            output_widget("plotly_map", height="600px")
        ),
        id="tabs"
    )
)

def server(input, output, session):
    @output
    @render_plotly
    def line_plot():
        fig = px.line(line_data, x="Date", y="Value", title="Mock Line Chart")
        return fig

    @output
    @render.data_frame
    def table():
        return table_data

    # @output
    # @render.ui
    # def leaflet_map():
    #     m = folium.Map(location=jaipur_coords, zoom_start=12, tiles="OpenStreetMap")
    #     folium.Marker(jaipur_coords, tooltip="Jaipur, India").add_to(m)
    #     # Render map to HTML
    #     map_html = m._repr_html_()
    #     # Wrap HTML in Shiny ui.HTML
    #     return ui.HTML(map_html)

    @output
    @render_plotly
    def plotly_map():
        fig = px.scatter_mapbox(
            map_df,
            lat="lat",
            lon="lon",
            zoom=11,
            height=550,
            center=dict(lat=jaipur["lat"], lon=jaipur["lon"]),
            mapbox_style="open-street-map",
        )
        fig.update_traces(marker=dict(size=14, color="red"))
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

app = App(app_ui, server)