""" Callbacks for loading the content of the carousel in the basis trade and leveraged basis trade tabs. """
from typing import List, Tuple

from dash import callback, dcc, Input, MATCH, no_update, Output, State
import dash_mantine_components as dmc

from backend.models.models_orm import Coin, Symbol
from frontend.src.components.components_id_tree import ComponentsIdTree
from frontend.src.components.graph_layout import generate_graph
from frontend.src.data_handling.data_handling_basis_trade import (
    load_data_cumulative_funding,
    load_data_funding_rates
)
from frontend.src.data_handling.data_handling_basis_trade_leveraged import (
    load_data_cumulative_funding_leveraged,
    load_data_funding_rates_leveraged,
    load_data_net_income_leveraged
)


def generate_carousel_strategy(
    triggered: str,
    coin: Symbol,
    active: int,
    data: dict
) -> Tuple[List[dmc.CarouselSlide], dict]:
    """Generate the content for the carousel in the basis trade and leveraged basis trade tabs.
    
    Args:
        triggered (str): The type of the component that triggered the callback.
        coin (Symbol): The symbol of the coin selected in the Select component.
        active (int): The index of the currently active slide in the carousel.
        data (dict): The current state data stored in the store belonging to the active tab. It includes information
        
    Returns:
        List[dmc.CarouselSlide]: The content for the carousel.
    """
    if triggered == 'regular':

        data['active_carousel'] = active
        carousel = [dmc.CarouselSlide([]) for _ in range(2)]

        loaders = [
            load_data_cumulative_funding,
            load_data_funding_rates
        ]

        carousel[data["active_carousel"]] = dmc.CarouselSlide(
            generate_graph(
                *loaders[data["active_carousel"]](coin),
                data["active_carousel"] == 1
            )
        )

        return carousel, data

    elif triggered == 'leveraged':
        data['active_carousel'] = active
        carousel = [dmc.CarouselSlide([]) for _ in range(3)]

        loaders = [
            load_data_cumulative_funding_leveraged,
            load_data_funding_rates_leveraged,
            load_data_net_income_leveraged
        ]

        carousel[data["active_carousel"]] = dmc.CarouselSlide(
            generate_graph(
                *loaders[data["active_carousel"]](
                    coin
                )
            )
        )

        return carousel, data

    return no_update, data


@callback(
    Output({"branch": "carousel", "leaf": "basis-trade", "type": MATCH}, 'children', allow_duplicate=True),
    Output({"branch": "stores", "leaf": "basis-trade", "type": MATCH}, 'data'),
    Input({"branch": "carousel", "leaf": "basis-trade", "type": MATCH}, 'active'),
    State({"branch": "stores", "leaf": "basis-trade", "type": MATCH}, 'data'),
    State({"leaf": "select-coin", "leaf": "basis-trade", "type": MATCH}, 'value'),
    State({"branch": "carousel", "leaf": "basis-trade", "type": MATCH}, 'id'),
    prevent_initial_call=True
)
def update_basis_trade(
    active: int,
    data: dict,
    coin: Symbol,
    _id: str
) -> Tuple[List[dmc.CarouselSlide], dcc.Store]:
    """
    Update the content of the slides in the basis trade and leveraged basis trade carousel based on the active slide.

    Args:
        active (int): The index of the currently active slide in the carousel.
        data (dict): The current state data stored in the store belonging to the active tab. It includes information 
                    like which slide is currently active.
        coin (Symbol): The symbol of the coin selected in the Select component.
        _id (str): The ID of the component that triggered the callback.

    Returns:
        Tuple[Any, Any, dict]: A tuple containing:
            - The updated content for the carousel.
            - The updated state data reflecting the currently active carousel slide.
    """
    triggered = _id['type']
            
    return generate_carousel_strategy(triggered, coin, active, data)


@callback(
    Output(ComponentsIdTree.Tabs.TabCarousel.CAROUSEL_BASIS_TRADE, 'children', allow_duplicate=True),
    Input(ComponentsIdTree.Tabs.TabSettings.SELECT_COIN_BASIS_TRADE, 'value'),
    State(ComponentsIdTree.Tabs.TabStores.STORE_BASIS_TRADE, 'data'),
    prevent_initial_call=True
)
def handle_tab_switch_basis_trade(
    coin: Symbol,
    data: dict,
) -> List[dmc.CarouselSlide]:
    """ 
    Handle the tab switch event for the Basis Trade tab.
 
    Args:
        coin (Symbol): The symbol of the coin selected in the dropdown component.
        data (dict): The current state data stored in `tab-2-store`. It includes information 
                    like which slide is currently active.

    Returns:
        List[dmc.CarouselSlide]: The updated content for the slides in the Basis Trade carousel.
    """
    carousel = [dmc.CarouselSlide([]) for _ in range(2)]

    loaders = [
        load_data_cumulative_funding,
        load_data_funding_rates
    ]

    carousel[data["active_carousel"]] = dmc.CarouselSlide(
        generate_graph(
            *loaders[data["active_carousel"]](coin),
            data["active_carousel"] == 1
        )
    )

    return carousel


@callback(
    Output(ComponentsIdTree.Tabs.TabCarousel.CAROUSEL_BASIS_TRADE_LEVERAGED, 'children', allow_duplicate=True),
    Input(ComponentsIdTree.Tabs.TabSettings.SELECT_COIN_BASIS_TRADE_LEVERAGED, 'value'),
    Input(ComponentsIdTree.Tabs.TabSettings.SELECT_STABLECOIN_BASIS_TRADE_LEVERAGED, 'value'),
    State(ComponentsIdTree.Tabs.TabStores.STORE_BASIS_TRADE_LEVERAGED, 'data'),
    prevent_initial_call=True
)
def handle_tab_switch_basis_trade_leveraged(
    coin: Symbol,
    stable: Coin,
    data: dict,
) -> List[dmc.CarouselSlide]:
    """ 
    Handle the tab switch event for the Basis Trade tab.
 
    Args:
        coin (Symbol): The symbol of the coin selected in the dropdown component.
        stable (Coin): The stable coin selected in the dropdown component.
        data (dict): The current state data stored in `tab-2-store`. It includes information 
                    like which slide is currently active.

    Returns:
        List[dmc.CarouselSlide]: The updated content for the slides in the Basis Trade carousel.
    """
    carousel = [dmc.CarouselSlide([]) for _ in range(3)]

    loaders = [
        load_data_cumulative_funding_leveraged,
        load_data_funding_rates_leveraged,
        load_data_net_income_leveraged
    ]

    carousel[data["active_carousel"]] = dmc.CarouselSlide(
        generate_graph(
            *loaders[data["active_carousel"]](
                coin,
                stable
            )
        )
    )

    return carousel