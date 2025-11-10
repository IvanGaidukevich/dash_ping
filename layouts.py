import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc


df = pd.read_csv('data/penguins.csv')


def create_layout():
    return dbc.Container([
       # Хедер
       html.Div([
            html.H1("Анализ пингвинов Антарктики!!!!!!!!", className="main-header"),
            html.H2("Исследование характеристик пингвинов по видам", className="main-subheader"),
        ], className="header"
        ),

        # Фильтры
        dbc.Row([
            dbc.Col([html.Label("Вид пингвина", className="filter-label"),
                     dcc.Dropdown(id="species-filter",
                                  options=[{'label': s, 'value': s} for s in df['species'].unique()],
                                  value=df['species'].unique(),
                                  multi=True,
                                  className='filter-dropdown'
                                  )], md=4),

            dbc.Col([html.Label("Остров обитания", className="filter-label"),
                     dcc.Dropdown(id="island-filter",
                                  options=[{'label': i, 'value': i} for i in df['island'].unique()],
                                  value=df['island'].unique(),
                                  multi=True,
                                  className='filter-dropdown'
                                  )], md=4),

            dbc.Col([html.Label("Пол пингвина", className="filter-label"),
                     dcc.Dropdown(id="sex-filter",
                                  options=[{'label': sx, 'value': sx} for sx in df['sex'].unique() if pd.notna(sx)],
                                  value=df['sex'].dropna().unique(),
                                  multi=True,
                                  className='filter-dropdown'
                                  )], md=4)
        ], className="filters-row"

        ),

        # Графики

        dbc.Row([dbc.Col([dcc.Graph(id='bill-length-scatter', className="dash-graph")], md=6),
                 dbc.Col([dcc.Graph(id='body-mass-histogram', className="dash-graph")], md=6)
                 ]),

        dbc.Row([dbc.Col([dcc.Graph(id='flipper-length-box', className="dash-graph")], md=6),
                 dbc.Col([dcc.Graph(id='species-pie', className="dash-graph")], md=6)
                 ]),

        # информационная панель

        html.Div(id='stats-panel', className="stats-panel")

    ], fluid=True)