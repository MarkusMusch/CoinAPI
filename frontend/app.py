""" Main file to run the Dash app """
from dash import callback, Dash, _dash_renderer, Input, Output, State 
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from sqlalchemy import create_engine

from backend.data_access.api_client.bybit_client import ByBitClient
from backend.data_access.crud.crud_funding import read_most_recent_update_funding
from backend.data_access.crud.crud_interest import read_most_recent_update_interest
from backend.data_access.crud.crud_open_interest import read_most_recent_update_open_interest
from backend.services.download_data import (
    catch_latest_funding,
    catch_latest_open_interest,
    catch_latest_interest,
    fill_funding,
    fill_interest,
    fill_open_interest
)
from backend.models.models_orm import Base, Coin, Symbol
from frontend.settings import frontend_settings
# This is not explicitly used but needs to be imported to make the callabacks knwon to the app
import frontend.src.callbacks.load_carousel_callback
from frontend.src.components.components_id_tree import ComponentsIdTree
from frontend.src.layouts.page_layout import app_layout


engine = create_engine('sqlite:///funding_history.db')
Base.metadata.create_all(engine)


client = ByBitClient()

for symbol in Symbol:

    most_recent_funding = read_most_recent_update_funding(symbol)

    if most_recent_funding is not None:
        catch_latest_funding(
            client,
            symbol,
            most_recent_funding
        )
    else:
        fill_funding(
            client,
            symbol
        )
    
    most_recent_oi = read_most_recent_update_open_interest(symbol)

    if most_recent_oi is not None:
        catch_latest_open_interest(
            client,
            symbol,
            most_recent_oi
        )
    else:
        fill_open_interest(
            client,
            symbol
        )

for coin in Coin:

    most_recent_datetime = read_most_recent_update_interest(coin)
    
    if most_recent_datetime is not None:
        catch_latest_interest(
            client,
            coin,
            most_recent_datetime
        )
    else:
        fill_interest(
            client,
            coin
        )


_dash_renderer._set_react_version("18.2.0")
app = Dash(__name__, external_stylesheets=[dmc.styles.CAROUSEL])


theme_toggle = dmc.ActionIcon(
    id=ComponentsIdTree.AppShellHeader.COLOR_THEME_TOGGLE,
    variant="transparent",
    color="yellow",
    size="lg",
    ms="auto",
    children=[
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ]
)


app.layout = dmc.MantineProvider(
    id=ComponentsIdTree.App.MANTINE_PROVIDER,
    forceColorScheme='dark',
    children=[
        dmc.AppShell(
            children=[
                dmc.AppShellHeader(
                    children=[
                        dmc.Group(
                            align="right",
                            p="md",
                            pr="lg",
                            children=[
                                theme_toggle
                            ]
                        )
                    ]
                ),
                dmc.AppShellMain(
                    children=[
                        app_layout
                    ]
                ),
                dmc.AppShellFooter(
                    p="xs",
                    children=[
                        dmc.Text(
                            size="xs",
                            p="xxs",
                            children=[
                                "© 2024, None of the above is financial advice."
                            ]
                        )
                    ]
                )
            ],
            header={"height": "60px"},
            footer={"height": "40px"},
            p="xl",
            m="xl"
        )
    ]
)


@callback(
    Output(ComponentsIdTree.App.MANTINE_PROVIDER, "forceColorScheme"),
    Input(ComponentsIdTree.AppShellHeader.COLOR_THEME_TOGGLE, "n_clicks"),
    State(ComponentsIdTree.App.MANTINE_PROVIDER, "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(_, theme):
    """Switch the theme of the app."""
    return "dark" if theme == "light" else "light"


if __name__ == '__main__':
    app.run_server(
        debug=frontend_settings.DEBUG_MODE,
        port=frontend_settings.PORT,
        host=frontend_settings.HOST
    )