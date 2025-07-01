from shiny import App, ui, render
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from shinywidgets import render_plotly, output_widget, render_widget
import plotly.express as px
from ipyleaflet import Map, Marker

# Mock data for tab 1 - Line Chart
dates = [datetime.now() - timedelta(days=i) for i in range(30)][::-1]
values = np.random.randint(50, 100, size=30)
line_data = pd.DataFrame({"Date": dates, "Value": values})

# Mock data for tab 2 - Data Table
data = np.random.randn(20, 5)
columns = [f"Column {i+1}" for i in range(5)]
table_data = pd.DataFrame(data, columns=columns)

# Map center coordinates for Jaipur, India
jaipur_coords = (26.9124, 75.7873)

app_ui = ui.page_fluid(
    ui.h2("Python Shiny App Example - 3 Tabs (ipyleaflet)"),
    ui.tags.style("""
        html, body, .shiny-page, .container-fluid, .nav-content, .tab-content, .nav-panel {
            height: 100vh !important;
            min-height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        .container-fluid {
            max-width: 100vw !important;
            width: 100vw !important;
        }
        .tab-content, .nav-panel {
            height: 100vh !important;
        }
        #ipyleaflet_map {
            height: 100vh !important;
            min-height: 100vh !important;
            width: 100vw !important;
            min-width: 100vw !important;
            margin: 0 !important;
            padding: 0 !important;
            display: block;
        }
    """),
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
            "Jaipur Map (ipyleaflet)",
            output_widget("ipyleaflet_map", height="100vh", width="100vw")
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

    @output
    @render_widget
    def ipyleaflet_map():
        m = Map(
            center=jaipur_coords, 
            zoom=12, 
            scroll_wheel_zoom=True
        )
        m.add_layer(Marker(location=jaipur_coords, title="Jaipur, India"))
        return m

app = App(app_ui, server)