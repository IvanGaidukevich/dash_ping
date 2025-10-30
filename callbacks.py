import plotly.graph_objects as go
import pandas as pd
import assets.design as ds
import dash_bootstrap_components as dbc
import plotly.io as pio
from dash import html, Input, Output


pio.templates['custom'] = pio.templates['plotly'].update(
    layout=dict(colorway=ds.MY_PALETTE)
)

pio.templates.default = 'custom'


df = pd.read_csv('data/penguins.csv')


def register_callbacks(app):
    @app.callback(
        Output('bill-length-scatter', 'figure'),
        Output('body-mass-histogram', 'figure'),
        Output('flipper-length-box', 'figure'),
        Output('species-pie', 'figure'),
        Output('stats-panel', 'children'),
        Input('species-filter', 'value'),
        Input('island-filter', 'value'),
        Input('sex-filter', 'value'),
    )
    def update_graphs(selected_species, selected_islands, selected_genders):

        filtered_df = df[
            (df['species'].isin(selected_species)) &
            (df['island'].isin(selected_islands)) &
            (df['sex'].isin(selected_genders))
            ]

        total_penguins = len(filtered_df)
        avg_mass = filtered_df['body_mass_g'].mean()
        avg_flipper = filtered_df['flipper_length_mm'].mean()
        species_count = filtered_df['species'].value_counts()

        scatter_fig = go.Figure()

        for species in filtered_df['species'].unique():
            species_df = filtered_df[filtered_df['species'] == species]
            scatter_fig.add_trace(
                go.Scatter(
                    x=species_df['bill_length_mm'],
                    y=species_df['bill_depth_mm'],
                    mode='markers',
                    name=species
                )
            )

        scatter_fig.update_layout(
            title="Длина и глубина клюва по видам",
            title_font_size=ds.GRAPH_TITLE_FONT_SIZE,
            title_x=ds.GRAPH_TITLE_ALIGN,
            title_font_weight=ds.GRAPH_FONT_WEIGHT,
            xaxis_title="Длина клюва (мм)",
            yaxis_title="Глубина клюва (мм)",
            font=dict(family=ds.GRAPH_FONT_FAMILY),
            xaxis=dict(title_font_size=ds.GRAPH_FONT_SIZE, tickfont=dict(size=ds.GRAPH_FONT_SIZE)),
            yaxis=dict(title_font_size=ds.GRAPH_FONT_SIZE, tickfont=dict(size=ds.GRAPH_FONT_SIZE)),
            legend=dict(font=dict(size=ds.GRAPH_FONT_SIZE)),
            plot_bgcolor=ds.PLOT_BACKGROUND_COLOR,
            paper_bgcolor=ds.PAPER_BACKGROUND_COLOR,
        )

        hist_fig = go.Figure()
        for species in filtered_df['species'].unique():
            species_df = filtered_df[filtered_df['species'] == species]
            hist_fig.add_trace(
                go.Histogram(
                    x=species_df['body_mass_g'],
                    name=species
                )
            )

        hist_fig.update_layout(
            title="Распределение массы тела",
            title_font_size=ds.GRAPH_TITLE_FONT_SIZE,
            title_x=ds.GRAPH_TITLE_ALIGN,
            title_font_weight=ds.GRAPH_FONT_WEIGHT,
            xaxis_title="Масса тела (г)",
            yaxis_title="Количество",
            font=dict(family=ds.GRAPH_FONT_FAMILY),
            xaxis=dict(title_font_size=ds.GRAPH_FONT_SIZE, tickfont=dict(size=ds.GRAPH_FONT_SIZE)),
            yaxis=dict(title_font_size=ds.GRAPH_FONT_SIZE, tickfont=dict(size=ds.GRAPH_FONT_SIZE)),
            legend=dict(font=dict(size=ds.GRAPH_FONT_SIZE)),
            plot_bgcolor=ds.PLOT_BACKGROUND_COLOR,
            paper_bgcolor=ds.PAPER_BACKGROUND_COLOR,
        )

        box_fig = go.Figure()

        for species in filtered_df['species'].unique():
            species_df = filtered_df[filtered_df['species'] == species]
            box_fig.add_trace(
                go.Box(
                    y=species_df['flipper_length_mm'],
                    name=species
                ))

        box_fig.update_layout(
            title="Распределение длины плавника по видам",
            title_font_size=ds.GRAPH_TITLE_FONT_SIZE,
            title_x=ds.GRAPH_TITLE_ALIGN,
            title_font_weight=ds.GRAPH_FONT_WEIGHT,
            yaxis_title="Длина плавника (мм)",
            font=dict(family=ds.GRAPH_FONT_FAMILY),
            xaxis=dict(title_font_size=ds.GRAPH_FONT_SIZE, tickfont=dict(size=ds.GRAPH_FONT_SIZE)),
            yaxis=dict(title_font_size=ds.GRAPH_FONT_SIZE, tickfont=dict(size=ds.GRAPH_FONT_SIZE)),
            legend=dict(font=dict(size=ds.GRAPH_FONT_SIZE)),
            plot_bgcolor=ds.PLOT_BACKGROUND_COLOR,
            paper_bgcolor=ds.PAPER_BACKGROUND_COLOR,
        )

        pie_fig = go.Figure(
            go.Pie(
                labels=species_count.index,
                values=species_count.values,
                textinfo='percent'
            )
        )

        pie_fig.update_layout(
            title="Распределение по видам",
            title_font_size=ds.GRAPH_TITLE_FONT_SIZE,
            title_x=ds.GRAPH_TITLE_ALIGN,
            title_font_weight=ds.GRAPH_FONT_WEIGHT,
            font=dict(family=ds.GRAPH_FONT_FAMILY),
            legend=dict(font=dict(size=ds.GRAPH_FONT_SIZE)),
            plot_bgcolor=ds.PLOT_BACKGROUND_COLOR,
            paper_bgcolor=ds.PAPER_BACKGROUND_COLOR,
        )

        stats_panel = dbc.Card([
            dbc.CardHeader("Статистика выборки"),
            dbc.CardBody([
                html.P(f'Всего пингвинов: {total_penguins}'),
                html.P(f'Средняя масса тела: {avg_mass:.0f}'),
                html.P(f'Средняя длина плавника : {avg_flipper:.0f}')
            ])
        ]
        )
        return scatter_fig, hist_fig, box_fig, pie_fig, stats_panel




