# Componentes web
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# auxiliares
from app import *
import sidebar

# =================================== #
# DADOS
# =================================== #



# =================================== #
# LAYOUT
# =================================== #

conexao_stylesheet = [{
    'selector': 'node',
    'style': {
        'label': 'data(label)',
        'text-valign': 'center',
        'text-halign': 'center',
        "background-color": 'data(color)',
        'border-width': 1.5,
        "border-opacity": 1,
        'width': 'data(size)',
        'height': 'data(size)',
        'opacity': 0.90
    }
}, {
    'selector': 'edge',
    'style': {
        "line-fill": "linear-gradient",
        'width': 2.5,
        'curve-style': 'bezier',
        'source-endpoint': 'outside-to-node',
        'target-endpoint': 'outside-to-node'
    }
}]

app.layout = html.Div([

    dbc.Row([
        dbc.Col([        
            dcc.Location(id="base-url"),
            sidebar.layout
        ], sm=2),
        dbc.Col([
            html.Div([
            ], id="page-content")
        ], sm=10)
    ]),


])

# =================================== #
# CALLBACKS
# =================================== #





# =================================== #
# RUN SERVER
# =================================== #


if __name__ == "__main__":
    app.run(debug=True)