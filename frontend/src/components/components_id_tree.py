""" This module contains the ComponentsIdTree class, which is a tree-like structure that contains the id's of the components in the frontend. """
from enum import Enum


class ComponentsIdTree():
    
    class App(str, Enum):
        MANTINE_PROVIDER = "mantine-provider"
    
    class AppShellHeader(str, Enum):
        COLOR_THEME_TOGGLE = "color-theme-toggle"
    
    class Tabs():

        class TabStores(dict, Enum):
            STORE_BASIS_TRADE = {
                "branch": "stores",
                "leaf": "basis-trade",
                "type": "regular"
            }
            STORE_BASIS_TRADE_LEVERAGED = {
                "branch": "stores",
                "leaf": "basis-trade",
                "type": "leveraged"
            }

        class TabPanels(str, Enum):
            PANEL_BASIS_TRADE = "Basis Trade"
            PANEL_BASIS_TRADE_LEVERAGED = "Basis Trade Leveraged"
        
        class TabCarousel(dict, Enum):
            CAROUSEL_BASIS_TRADE = {
                "branch": "carousel",
                "leaf": "basis-trade",
                "type": "regular"
            }
            CAROUSEL_BASIS_TRADE_LEVERAGED = {
                "branch": "carousel",
                "leaf": "basis-trade",
                "type": "leveraged"
            }
        
        class TabSettings(dict, Enum):
            SELECT_COIN_BASIS_TRADE = {
                "leaf": "select-coin",
                "leaf": "basis-trade",
                "type": "regular"
            }
            SELECT_COIN_BASIS_TRADE_LEVERAGED = {
                "leaf": "select-coin",
                "leaf": "basis-trade",
                "type": "leveraged"
            }
            SELECT_STABLECOIN_BASIS_TRADE_LEVERAGED = {
                "leaf": "select-coin",
                "leaf": "basis-trade",
                "type": "leveraged",
                "field": "stablecoin"
            }