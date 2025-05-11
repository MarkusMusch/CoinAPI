""" This module contains the components for the Basis Trade Leveraged tab. """
import dash_mantine_components as dmc

from backend.models.models_orm import Coin, Symbol
from frontend.src.components.components_id_tree import ComponentsIdTree


fieldset_basis_trade_leveraged = dmc.Fieldset(
    legend="Chart Settings Basis Trade Leveraged",
    mt='xl',
    children=[
        dmc.Stack(
            children=[
                dmc.Select(
                    id=ComponentsIdTree.Tabs.TabSettings.SELECT_COIN_BASIS_TRADE_LEVERAGED,
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
                ),
                dmc.Select(
                    id=ComponentsIdTree.Tabs.TabSettings.SELECT_STABLECOIN_BASIS_TRADE_LEVERAGED,
                    label="Select Stablecoin",
                    placeholder="Select Stablecoin",
                    value=Coin.DAI,
                    allowDeselect=False,
                    data=[
                        {
                            "value": coin,
                            "label": coin.value,
                            "description": coin.value
                        }
                        for coin in Coin
                    ]
                )
            ]
        )
    ]
)