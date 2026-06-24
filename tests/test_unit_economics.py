import pandas as pd

from src.compute_unit_economics import (
    build_marketplace_price_summary,
    classify_rough_headroom,
    compute_supplier_costs,
)

def test_compute_supplier_costs_converts_selected_price_to_thb():
    """
    Supplier selected price should convert into THB using the FX rate.
    """

    supplier_df = pd.DataFrame(
        {
            "selected_unit_price": [5.50],
            "fx_rate_to_thb": [35.00],
            "international_shipping_thb": [0.00],
        }
    )

    result = compute_supplier_costs(supplier_df)

    assert result.loc[0, "supplier_cost_thb_est"] == 192.50
    assert result.loc[0, "source_cost_with_shipping_thb_est"] == 192.50


def test_compute_supplier_costs_treats_missing_shipping_as_zero():
    """
    Missing shipping estimates should not break the first pilot calculation.
    """

    supplier_df = pd.DataFrame(
        {
            "selected_unit_price": [8.50],
            "fx_rate_to_thb": [35.00],
            "international_shipping_thb": [None],
        }
    )

    result = compute_supplier_costs(supplier_df)

    assert result.loc[0, "supplier_cost_thb_est"] == 297.50
    assert result.loc[0, "international_shipping_thb"] == 0
    assert result.loc[0, "source_cost_with_shipping_thb_est"] == 297.50


def test_marketplace_price_summary_uses_min_and_max_delivered_price():
    """
    Marketplace summary should capture the cheapest and highest observed prices.
    """

    marketplace_df = pd.DataFrame(
        {
            "product_id": ["p002", "p002"],
            "observation_id": ["obs_001", "obs_002"],
            "total_delivered_price_thb": [166, 537],
        }
    )

    result = build_marketplace_price_summary(marketplace_df)

    assert result.loc[0, "product_id"] == "p002"
    assert result.loc[0, "observed_min_delivered_price_thb_obs"] == 166
    assert result.loc[0, "observed_max_delivered_price_thb_obs"] == 537
    assert result.loc[0, "observed_listing_count"] == 2


def test_classify_rough_headroom_returns_early_positive_signal():
    """
    High rough headroom should produce an early positive signal.
    """

    assert classify_rough_headroom(0.30) == "early_positive_signal"
    assert classify_rough_headroom(0.50) == "early_positive_signal"


def test_classify_rough_headroom_returns_thin_headroom():
    """
    Positive but low rough headroom should be treated as thin.
    """

    assert classify_rough_headroom(0.00) == "thin_headroom"
    assert classify_rough_headroom(0.10) == "thin_headroom"


def test_classify_rough_headroom_returns_negative_headroom():
    """
    Negative rough headroom should flag a difficult product.
    """

    assert classify_rough_headroom(-0.01) == "negative_headroom"
    assert classify_rough_headroom(-0.50) == "negative_headroom"