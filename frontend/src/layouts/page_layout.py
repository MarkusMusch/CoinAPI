""" This module contains the layout of the page. """
from enum import Enum
from typing import List

from dash import dcc
import dash_mantine_components as dmc

from frontend.src.components.components_id_tree import ComponentsIdTree
from frontend.src.components.tabs.basis_trade import fieldset_basis_trade
from frontend.src.components.tabs.basis_trade_leveraged import fieldset_basis_trade_leveraged
from frontend.src.components.tabs.tab_layout import generate_tab


def generate_stores(ids: Enum) -> List[dcc.Store]:
    """ Generate the stores for the page. 
    
    Args:
        ids (Enum): The ids of the stores.

    Returns:
        List[dcc.Store]: The stores for the page.
    """
    return [
        dcc.Store(
            id=store_id,
            data={'active_carousel': 0}
        ) for store_id in ids
    ]


def generate_tabs(ids: Enum) -> List[dmc.TabsTab]:
    """Generate the tabs for the page.

    Args:
        ids (Enum): The ids of the tabs.
    
    Returns:
        List[dmc.TabsTab]: The tabs for the page.
    """
    return [
        dmc.TabsTab(
            value=panel_id,
            children=panel_id
        ) for panel_id in ids
    ]


def generate_panels(
    ids_panels: Enum,
    ids_carousels: Enum,
    fieldsets: List[dmc.Fieldset]
) -> List[dmc.TabsPanel]:
    """Generate the panels for the page.

    Args:
        ids_panels (Enum): The ids of the panels.
        ids_carousels (Enum): The ids of the carousels.
        fieldsets (List[dmc.Fieldset]): The fieldsets for the panels.

    Returns:
        List[dmc.TabsPanel]: The panels for the page.
    """
    return [
        dmc.TabsPanel(
            id=panel_id,
            value=panel_id,
            children=generate_tab(carousel_id, fieldset)
        ) for panel_id, carousel_id, fieldset in 
            zip(ids_panels, ids_carousels, fieldsets)
    ]


page_layout = dmc.Box(
    children=[
        dmc.Tabs(
            value=ComponentsIdTree.Tabs.TabPanels.PANEL_BASIS_TRADE,
            children=[
                dmc.TabsList(
                    children=[
                        *generate_stores(ComponentsIdTree.Tabs.TabStores),
                        *generate_tabs(ComponentsIdTree.Tabs.TabPanels)
                    ]
                ),
                *generate_panels(
                    ComponentsIdTree.Tabs.TabPanels,
                    ComponentsIdTree.Tabs.TabCarousel,
                    [fieldset_basis_trade, fieldset_basis_trade_leveraged]
                )
            ]
        )
    ],
    style={"maxWidth": "1600px", "margin": "auto"}
)


app_layout = dmc.Box(
    children=[
        dmc.Box(
            children=[
                page_layout
            ]
        )
    ]
)