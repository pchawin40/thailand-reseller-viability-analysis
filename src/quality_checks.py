from pathlib import Path

import pandas as pd

MARKETPLACE_PATH = Path("data/observations/marketplace_observations.csv")
SUPPLIER_PATH = Path("data/observations/supplier_cost_benchmarks.csv")

REQUIRED_MARKETPLACE_COLUMNS = {
    "observation_id",
    "observation_date",
    "product_id",
    "product_name",
    "category",
    "platform",
    "seller_type",
    "ship_from_country",
    "listed_price_thb",
    "shipping_fee_thb",
    "total_delivered_price_thb",
    "estimated_delivery_days",
    "rating",
    "review_count",
    "units_sold_displayed",
    "promotion_flag",
    "match_quality",
    "source_reference"   
}

REQUIRED_SUPPLIER_COLUMNS = {
    "observation_date",
    "product_id",
    "supplier_platform",
    "supplier_country",
    "source_currency",
    "unit_price_low",
    "unit_price_high",
    "selected_unit_price",
    "minimum_order_quantity",   
    "assumed_order_quantity",
    "origin_shipping_cost",
    "international_shipping_thb",
    "estimated_unit_weight_kg",
    "fx_rate_to_thb",
    "fx_source",
    "match_quality",
    "source_reference",
}

def check_required_columns(df: pd.DataFrame, required_columns: set[str], file_name: str) -> None:
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
            raise ValueError(f"FAILED: {file_name} is missing columns: {sorted(missing_columns)}")

def check_supplier_benchmarks_quality(path: Path = SUPPLIER_PATH) -> None:
    if not path.exists():
        raise FileNotFoundError(f"FAILED: Supplier benchmark file not found: {path}")
    
    df = pd.read_csv(path)

    check_required_columns(df, REQUIRED_SUPPLIER_COLUMNS, "supplier_cost_benchmarks.csv")

    if df.empty:
        raise ValueError("FAILED: supplier_cost_benchmarks.csv is empty")

    if df["product_id"].isna().any():
        raise ValueError("FAILED: supplier benchmark product_id has missing values")

    if df["selected_unit_price"].isna().any():
        raise ValueError("FAILED: supplier benchmark selected_unit_price has missing values")
    
    if (df["selected_unit_price"] <= 0).any():
        raise ValueError("FAILED: supplier benchmark selected_unit_price must be positive")
    
    if (df["estimated_unit_weight_kg"] <= 0).any():
        raise ValueError("FAILED: supplier benchmark estimated_unit_weight_kg must be positive")
    
    print("PASSED: Supplier benchmark quality checks passed")

def check_marketplace_observations_quality(path: Path = MARKETPLACE_PATH) -> None:
    if not path.exists():
        raise FileNotFoundError(f"FAILED: Marketplace observation file not found: {path}")
    
    df = pd.read_csv(path)

    check_required_columns(df, REQUIRED_MARKETPLACE_COLUMNS, "marketplace_observations.csv")

    if df.empty:
        raise ValueError("FAILED: marketplace_observations.csv is empty")
    
    if df["product_id"].isna().any():
        raise ValueError("FAILED: marketplace product_id has missing values")
    
    if df["listed_price_thb"].isna().any():
        raise ValueError("FAILED: marketplace listed_price_thb has missing values")
    
    if (df["listed_price_thb"] <= 0).any():
        raise ValueError("FAILED: marketplace listed_price_thb must be positive")
    
    valid_seller_types = {"local", "cross_border", "unknown"}
    invalid_seller_types = set(df["seller_type"].dropna()) - valid_seller_types

    if invalid_seller_types:
        raise ValueError(f"FAILED: invalid seller_type values: {sorted(invalid_seller_types)}")
    
    valid_match_quality = {"high", "medium", "low"}
    invalid_match_quality = set(df["match_quality"].dropna()) - valid_match_quality

    if invalid_match_quality:
        raise ValueError(f"FAILED: invalid match_quality values: {sorted(invalid_match_quality)}")
    
    print("PASSED: Marketplace observation quality checks passed")

def check_product_relationships(
    marketplace_path: Path = MARKETPLACE_PATH,
    supplier_path: Path = SUPPLIER_PATH
) -> None:
    marketplace_df = pd.read_csv(marketplace_path)
    supplier_df = pd.read_csv(supplier_path)

    marketplace_products = set(marketplace_df["product_id"].dropna())
    supplier_products = set(supplier_df["product_id"].dropna())

    supplier_without_marketplace = supplier_products - marketplace_products
    marketplace_without_supplier = marketplace_products - supplier_products

    if supplier_without_marketplace:
        raise ValueError(
            "FAILED: Supplier benchmark has product_id values not found in marketplace observations: "
            f"{sorted(supplier_without_marketplace)}"
        )
        
    if marketplace_without_supplier:
        raise ValueError(
            "FAILED: Marketplace observations have product_id values without supplier benchmarks: "
            f"{sorted(marketplace_without_supplier)}"
        )
        
    print("PASSED: Product relationship checks passed")


if __name__ == "__main__":
    check_marketplace_observations_quality()
    check_supplier_benchmarks_quality()
    check_product_relationships()