import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, "https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"],
        suppress_callback_exceptions=True,
        )

app.scripts.config.serve_locally = True
server = app.server