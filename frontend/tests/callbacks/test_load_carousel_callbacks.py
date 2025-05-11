import dash_mantine_components as dmc


from frontend.src.callbacks.load_carousel_callback import (
    generate_carousel_strategy,
    update_basis_trade,
    handle_tab_switch_basis_trade
)


def test_generate_carousel_strategy_regular(
    mock_symbol,
    mock_data,
    mock_generate_graph,
    mock_load_data_cumulative_funding,
    mock_load_data_funding_rates
):
    mock_load_data_cumulative_funding.return_value = ([], [])
    mock_load_data_funding_rates.return_value = ([], [])

    slides, data = generate_carousel_strategy('regular', mock_symbol, 0, mock_data)
    assert len(slides) == 2
    assert isinstance(slides[0], dmc.CarouselSlide)
    assert data['active_carousel'] == 0

    slides, data = generate_carousel_strategy('regular', mock_symbol, 1, mock_data)
    assert len(slides) == 2
    assert isinstance(slides[1], dmc.CarouselSlide)
    assert data['active_carousel'] == 1


def test_generate_carousel_strategy_leveraged(
    mock_symbol,
    mock_data,
    mock_generate_graph,
    mock_load_data_cumulative_funding_leveraged,
    mock_load_data_funding_rates_leveraged,
    mock_load_data_net_income_leveraged
):
    mock_load_data_cumulative_funding_leveraged.return_value = ([], [])
    mock_load_data_funding_rates_leveraged.return_value = ([], [])
    mock_load_data_net_income_leveraged.return_value = ([], [])

    slides, data = generate_carousel_strategy('leveraged', mock_symbol, 0, mock_data)
    assert len(slides) == 3
    assert isinstance(slides[0], dmc.CarouselSlide)
    assert data['active_carousel'] == 0

    slides, data = generate_carousel_strategy('leveraged', mock_symbol, 1, mock_data)
    assert len(slides) == 3
    assert isinstance(slides[1], dmc.CarouselSlide)
    assert data['active_carousel'] == 1

    slides, data = generate_carousel_strategy('leveraged', mock_symbol, 2, mock_data)
    assert len(slides) == 3
    assert isinstance(slides[2], dmc.CarouselSlide)
    assert data['active_carousel'] == 2


def test_update_basis_trade(
    mock_symbol,
    mock_data,
    mock_generate_graph,
    mock_load_data_cumulative_funding,
    mock_load_data_funding_rates,
    mock_load_data_cumulative_funding_leveraged,
    mock_load_data_funding_rates_leveraged,
    mock_load_data_net_income_leveraged
):
    mock_load_data_cumulative_funding.return_value = ([], [])
    mock_load_data_funding_rates.return_value = ([], [])
    mock_load_data_cumulative_funding_leveraged.return_value = ([], [])
    mock_load_data_funding_rates_leveraged.return_value = ([], [])
    mock_load_data_net_income_leveraged.return_value = ([], [])

    slides, data = update_basis_trade(0, mock_data, mock_symbol, {'type': 'regular'})
    assert len(slides) == 2
    assert isinstance(slides[0], dmc.CarouselSlide)
    assert data['active_carousel'] == 0

    slides, data = update_basis_trade(1, mock_data, mock_symbol, {'type': 'leveraged'})
    assert len(slides) == 3
    assert isinstance(slides[1], dmc.CarouselSlide)
    assert data['active_carousel'] == 1


def test_handle_tab_switch_basis_trade(
    mock_symbol,
    mock_data,
    mock_generate_graph,
    mock_load_data_cumulative_funding,
    mock_load_data_funding_rates,
    mock_load_data_cumulative_funding_leveraged,
    mock_load_data_funding_rates_leveraged,
    mock_load_data_net_income_leveraged
):
    mock_load_data_cumulative_funding.return_value = ([], [])
    mock_load_data_funding_rates.return_value = ([], [])
    mock_load_data_cumulative_funding_leveraged.return_value = ([], [])
    mock_load_data_funding_rates_leveraged.return_value = ([], [])
    mock_load_data_net_income_leveraged.return_value = ([], [])

    slides = handle_tab_switch_basis_trade(mock_symbol, mock_data, {'type': 'regular'})
    assert len(slides) == 2
    assert isinstance(slides[0], dmc.CarouselSlide)

    slides = handle_tab_switch_basis_trade(mock_symbol, mock_data, {'type': 'leveraged'})
    assert len(slides) == 3
    assert isinstance(slides[0], dmc.CarouselSlide)