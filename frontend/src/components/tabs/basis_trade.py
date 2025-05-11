""" This module contains the components for the basis trade tab. """
import dash_mantine_components as dmc

from backend.models.models_orm import Symbol
from frontend.src.components.components_id_tree import ComponentsIdTree


fieldset_basis_trade = dmc.Fieldset(
    legend="Chart Settings",
    mt='xl',
    children=[
        dmc.Select(
            id=ComponentsIdTree.Tabs.TabSettings.SELECT_COIN_BASIS_TRADE,
            label="Select Coin",
            placeholder="Select Coin",
            value=Symbol.BTCUSDT,
            allowDeselect=False,
            data=[
                {
                    "value": symbol,
                    "label": symbol.value,
                    "description": symbol.value
                }
                for symbol in Symbol
            ]
        )
    ]
)