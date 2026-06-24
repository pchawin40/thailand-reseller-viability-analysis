import pandas as pd
from pathlib import Path

MARKETPLACE_PATH = Path("data/observations/marketplace_observations.csv")
SUPPLIER_PATH = Path("data/observations/supplier_cost_benchmarks.csv")
OUTPUT_PATH = Path("outputs/unit_economics_pilot.csv")

def load_marketplace_observations(path: Path = MARKETPLACE_PATH) -> pd.DataFrame:
    """
    Load manually collected marketplace observations
    """

    return pd.read_csv(path)

def load_supplier_benchmarks(path: Path = SUPPLIER_PATH) -> pd.DataFrame:
    """
    Load public supplier benchmark observations
    """
    return pd.read_csv(path)

def build_marketplace_price_summary(marketplace_df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarized observed marketplace prices by product

    For this first pilot, use the lowest observed delivered price as the competitive
    price reference. Later, split local and cross-border prices into separate 
    benchmarks
    """
    
    price_summary = (
        marketplace_df
        .groupby("product_id", as_index=False)
        .agg(
            observed_min_delivered_price_thb_obs=("total_delivered_price_thb", "min"),
            observed_max_delivered_price_thb_obs=("total_delivered_price_thb", "max"),
            observed_listing_count=("observation_id", "count"),
        )
    )

    return price_summary

def compute_supplier_costs(supplier_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert supplier benchmark prices into THB

    The selected_unit_price is observered in the supplier listing currency
    fx_rate_to_thb converts that supplier price into Thai Baht
    """
    supplier_df = supplier_df.copy()

    supplier_df["supplier_cost_thb_est"] = (
        supplier_df["selected_unit_price"] * supplier_df["fx_rate_to_thb"]
    )

    # Some supplier records may not have a reliable shipping estimate yet
    # So for the pilot, we treat international shipping as zero, 
    # but keeping the column separate so it can be improved later
    supplier_df["international_shipping_thb"] = supplier_df[
        "international_shipping_thb"
    ].fillna(0)

    supplier_df["source_cost_with_shipping_thb_est"] = (
        supplier_df["supplier_cost_thb_est"]
        + supplier_df["international_shipping_thb"]
    )

    return supplier_df

def build_unit_economics_pilot(
    marketplace_df: pd.DataFrame,
    supplier_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the first pilot unit-economics output

    Compare supplier cost against observed marketplace prices
    """
    marketplace_summary = build_marketplace_price_summary(marketplace_df)
    supplier_costs = compute_supplier_costs(supplier_df)

    output_df = supplier_costs.merge(
        marketplace_summary,
        on="product_id",
        how="left",
    )

    output_df["rough_price_headroom_thb_est"] = (
        output_df["observed_min_delivered_price_thb_obs"]
        - output_df["source_cost_with_shipping_thb_est"]
    )

    output_df["rough_price_headroom_pct_est"] = (
        output_df["rough_price_headroom_thb_est"]
        / output_df["observed_min_delivered_price_thb_obs"]
    )

    output_df["early_viability_signal"] = output_df[
        "rough_price_headroom_pct_est"
    ].apply(classify_rough_headroom)

    output_columns = [
        "product_id",
        "supplier_platform",
        "supplier_country",
        "source_currency",
        "selected_unit_price",
        "fx_rate_to_thb",
        "supplier_cost_thb_est",
        "international_shipping_thb",
        "source_cost_with_shipping_thb_est",
        "observed_min_delivered_price_thb_obs",
        "observed_max_delivered_price_thb_obs",
        "observed_listing_count",
        "rough_price_headroom_thb_est",
        "rough_price_headroom_pct_est",
        "match_quality",
        "source_reference",
    ]

    return output_df[output_columns]

def export_unit_economics_pilot(output_path: Path = OUTPUT_PATH) -> None:
    """
    Create the first dashboard-ready pilot unit-economics output
    """
    marketplace_df = load_marketplace_observations()
    supplier_df = load_supplier_benchmarks()

    output_df = build_unit_economics_pilot(
        marketplace_df=marketplace_df,
        supplier_df=supplier_df,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(output_path, index=False)

    print(f"Exported pilot unit economics to {output_path}")

def classify_rough_headroom(headroom_pct: float) -> str:
    """
    Translate rough price headroom into an early viability signal

    Only compare supplier benchmark cost plus shipping against the 
    lowest observed marketplace delivered price
    """
    if headroom_pct >= 0.30:
        return "early_positive_signal"
    
    if headroom_pct >= 0:
        return "thin_headroom"
    
    return "negative_headroom"

if __name__ == "__main__":
    export_unit_economics_pilot()

