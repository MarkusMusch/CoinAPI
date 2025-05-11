""" This module contains the layout for graphs. """
from typing import Union, List

import dash_mantine_components as dmc


def generate_graph(
    title: str,
    data: list,
    series: list,
    with_reference_line: bool = True
) -> List[Union[dmc.Title, dmc.LineChart]]:
    """ Generate a graph with the given data.
    
    Args:
        title (str): The title of the graph.
        data (list): The data to be displayed in the graph.
        series (list): The series to be displayed in the graph.
        with_reference_line (bool, optional): Whether to display a reference line in the graph. Defaults to True.
        
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: The title and the graph.
    """
    reference_line = [{"y": 0, "label": "", "color": "red.6"}] if with_reference_line else None

    return [
        dmc.Center(
            children=[
                dmc.Title(
                    order=4,
                    mt='xl',
                    children=[title]
                )
            ]
        ),
        dmc.LineChart(
            h="calc(80vh - 300px)",
            lineProps={
                "isAnimationActive": True,
                "animationDuration": 500,
                "animationEasing": "ease-in-out",
                "animationBegin": 0,
            },
            dataKey="date",
            data=data,
            series = series,
            referenceLines=reference_line, 
            curveType="linear",
            tickLine="xy",
            gridAxis="xy",
            withDots=False,
            style={
                "marginTop": "10px",
                "marginBottom": "50px",
                "marginLeft": "50px",
                "marginRight": "50px"
            }
        )
    ]