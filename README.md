# Thailand Cross-Border Reseller Viability Analyzer

*By Chawin Pathompornvivat*

A portfolio analytics project that builds a product-level pricing and unit-economics decision tool using Python, DuckDB, SQL, and Power BI. The project evaluates whether a Thailand-based marketplace seller can source generic consumer products from overseas suppliers and resell them profitably after accounting for supplier cost, currency conversion, international shipping, import-cost assumptions, marketplace fees, advertising, fulfillment, expected returns, and cross-border price competition.

*This project is not intended to provide financial, tax, customs, legal, or business advice. It demonstrates data modeling, pricing analysis, unit-economics calculations, scenario modeling, validation, and dashboard reporting using public observations and documented assumptions.*

**Table of Contents**

* [Getting Started](#getting-started)
* [Skills Demonstrated](#skills-demonstrated)
* [Reseller Viability Analyzer at a Glance](#reseller-viability-analyzer-at-a-glance)
* [Analytics Objective](#analytics-objective)
* [MVP Scope](#mvp-scope)
* [Data Pipeline and Technologies Used](#data-pipeline-and-technologies-used)
* [Current Pilot Workflow](#current-pilot-workflow)
* [Data Model Overview](#data-model-overview)
* [SQL Analytics Workflow](#sql-analytics-workflow)
* [Dashboard Overview](#dashboard-overview)
* [Key Metrics](#key-metrics)
* [Project Structure](#project-structure)
* [Data Quality Checks](#data-quality-checks)
* [Common Commands](#common-commands)
* [Limitations](#limitations)
* [Conclusion and Next Steps](#conclusion-and-next-steps)

## Skills Demonstrated

As the project is completed, it will demonstrate:

* Building an end-to-end analytics pipeline using Python, pandas, DuckDB, and SQL
* Designing a star-schema-inspired data model for products, marketplace observations, supplier benchmarks, and cost scenarios
* Creating product-level unit-economics calculations for landed cost, contribution margin, and break-even price
* Comparing local and cross-border delivered prices using publicly observable marketplace data
* Building transparent pessimistic, base, and optimistic pricing scenarios
* Separating observed marketplace data from modeled estimates
* Creating data-quality checks for observations, assumptions, calculations, and final outputs
* Writing positive and negative pytest validation cases
* Automating tests with GitHub Actions
* Building a Power BI dashboard for pricing and product-selection decision support

## Getting Started

To run this project locally, clone this repository:

```bash
git clone https://github.com/pchawin40/thailand-reseller-viability-analysis.git
cd thailand-reseller-viability-analysis
```

### Create and Activate a Virtual Environment

Create the virtual environment one time:

```bash
python3 -m venv .venv
```

Activate it each time you work on the project:

```bash
source .venv/bin/activate
```

When the virtual environment is active, the terminal should show something similar to:

```bash
(.venv) ~/personal/thailand-reseller-viability-analysis$
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### Current Status

This project is currently in the pilot-data design stage.

The first milestone focuses on:

1. Defining the business question
2. Creating marketplace observation templates
3. Creating supplier-cost benchmark templates
4. Setting up a documented assumptions file
5. Collecting a small number of public product observations
6. Confirming that the data structure works before building Python, SQL, and Power BI outputs

## Reseller Viability Analyzer at a Glance

Marketplace resellers make product-selection and pricing decisions under uncertainty. A product may appear attractive because the supplier price is low, but the actual margin depends on shipping, import costs, marketplace fees, advertising, returns, fulfillment, and competitor pricing.

This project evaluates reseller viability using:

* Observed marketplace prices
* Observed total delivered prices
* Supplier-cost benchmarks
* Currency-converted sourcing cost
* Estimated landed cost
* Marketplace fee assumptions
* Advertising and return assumptions
* Contribution margin
* Break-even selling price
* Competitive price headroom
* Scenario-based viability classification

The final output is designed to help answer:

* Which products are worth evaluating?
* What selling price is required to break even?
* Can the product be priced competitively?
* Does faster local fulfillment support a price premium?
* Which cost assumptions create the greatest margin risk?
* Does the product remain viable under downside scenarios?
* Which products should be avoided?

## Analytics Objective

### Research Question

Which generic consumer products remain economically viable for a Thailand-based marketplace reseller after accounting for complete unit economics and direct cross-border marketplace competition?

### Project Objective

Build an end-to-end analytics workflow that converts publicly observable marketplace prices, supplier-cost benchmarks, and documented business assumptions into an explainable product-viability model.

The completed project will calculate product-level landed cost, contribution margin, break-even price, competitive price headroom, and scenario-based viability classifications.

The project demonstrates skills:

* Business problem framing
* Pricing and margin analysis
* Scenario analysis
* Data modeling
* SQL analytics
* Data validation
* Dashboard reporting
* Assumption documentation

## MVP Scope

The MVP is intentionally small and explainable.

### Initial Pilot

* Two generic, non-regulated products
* One Thai marketplace
* One local listing and one cross-border listing per product
* One public supplier benchmark per product
* Four marketplace observations
* Two supplier-cost observations

### Completed MVP Target

* 10–15 matched products
* Two to three product categories
* Two Thai marketplaces
* Public supplier-cost benchmarks
* Pessimistic, base, and optimistic scenarios
* Python, DuckDB, SQL, pytest, GitHub Actions, and Power BI

### Out of Scope for the MVP

* Large-scale or prohibited marketplace scraping
* Private customer information
* Confidential seller-account information
* Actual supplier invoices
* Live price monitoring
* Machine-learning forecasts
* Full business profitability after salaries, rent, and overhead
* Claims about the entire Thai e-commerce market
* Legal, tax, or customs advice

## Data Pipeline and Technologies Used

This project uses a lightweight local analytics stack:

* **Python**: Reads observation files, applies assumptions, calculates unit economics, and exports dashboard-ready outputs
* **Pandas**: Cleans marketplace observations and supplier-cost benchmarks
* **YAML**: Stores configurable and dated assumptions
* **DuckDB**: Serves as the local analytical database
* **SQL**: Builds schemas, cost calculations, scenario comparisons, and viability outputs
* **Power BI Desktop**: Presents product viability and pricing insights
* **Pytest**: Validates source data, assumptions, formulas, and outputs
* **GitHub Actions**: Runs tests automatically on push and pull request
* **GitHub**: Stores project code, documentation, assumptions, and dashboard artifacts

### Planned Pipeline Flow

```text
Marketplace observations
        +
Supplier-cost benchmarks
        +
Documented assumptions
        |
        v
Python and pandas transformations
        |
        v
DuckDB dimensions and fact tables
        |
        v
SQL unit-economics and scenario views
        |
        v
Dashboard-ready CSV outputs
        |
        v
Power BI viability dashboard
```

## Current Pilot Workflow

The first version of this project uses manually collected public observations instead of automated scraping.

Initial input files:

```text
data/observations/marketplace_observations.csv
data/observations/supplier_cost_benchmarks.csv
config/assumptions.yaml
```

The purpose of the pilot is to confirm that the available data can support the model before building the full pipeline.

### Marketplace Observation File

The marketplace observation file records one row per observed listing.

Planned fields include:

```text
observation_id
observation_date
product_id
product_name
category
platform
seller_type
ship_from_country
listed_price_thb
shipping_fee_thb
total_delivered_price_thb
estimated_delivery_days
rating
review_count
units_sold_displayed
promotion_flag
match_quality
source_reference
```

### Supplier-Cost Benchmark File

The supplier-cost benchmark file records public sourcing-cost estimates.

Planned fields include:

```text
observation_date
product_id
supplier_platform
supplier_country
source_currency
unit_price_low
unit_price_high
selected_unit_price
minimum_order_quantity
assumed_order_quantity
origin_shipping_cost
international_shipping_thb
estimated_unit_weight_kg
fx_rate_to_thb
fx_source
match_quality
source_reference
```

### Assumptions File

The assumptions file stores configurable model inputs such as:

```text
marketplace fee assumptions
transaction fee assumptions
import-cost assumptions
currency conversion assumptions
advertising cost assumptions
return cost assumptions
scenario settings
```

Assumptions are separated from observed values so that the model can be audited and updated without rewriting the analysis logic.

## Data Model Overview

The planned database uses a star-schema-inspired model.

### `dim_product`

Stores product-level attributes.

```text
product_id
product_name
category
hs_code_assumption
unit_of_measure
estimated_unit_weight_kg
```

### `dim_platform`

Stores marketplace attributes.

```text
platform_id
platform_name
country
fee_schedule_version
```

### `dim_scenario`

Stores scenario definitions.

```text
scenario_id
scenario_name
scenario_description
sourcing_cost_multiplier
advertising_cost_pct
return_rate
fee_adjustment_pct
```

### `fact_marketplace_observation`

Stores public marketplace listing observations.

```text
observation_id
observation_date
product_id
platform_id
seller_type
listed_price_thb_obs
shipping_fee_thb_obs
total_delivered_price_thb_obs
estimated_delivery_days_obs
rating_obs
review_count_obs
match_quality
```

### `fact_supplier_cost_benchmark`

Stores public supplier-cost benchmark observations.

```text
supplier_observation_id
observation_date
product_id
supplier_platform
supplier_country
source_currency
selected_unit_price
fx_rate_to_thb
supplier_cost_thb_est
minimum_order_quantity
international_shipping_thb_est
match_quality
```

### `fact_unit_economics`

Stores modeled unit-economics outputs by product, platform, and scenario.

```text
economics_id
product_id
platform_id
scenario_id
supplier_cost_thb_est
landed_cost_thb_est
platform_fee_thb_est
advertising_cost_thb_est
return_cost_thb_est
total_variable_cost_thb_est
break_even_price_thb_est
competitive_price_headroom_thb_est
contribution_margin_thb_est
contribution_margin_pct_est
viability_status
viability_reason
```

This structure keeps observed data, assumptions, and modeled outputs separate.

## SQL Analytics Workflow

The planned SQL workflow will build from raw observations into scenario-based product viability outputs.

### 1. Observation Cleaning

Clean marketplace and supplier-cost records, standardize category names, validate seller type, and separate observed values from estimated values.

### 2. Cost Standardization

Convert supplier prices into THB and calculate estimated sourcing cost per unit.

### 3. Landed Cost Calculation

Estimate landed cost by combining supplier cost, shipping, import-cost assumptions, and packaging or handling assumptions.

### 4. Platform Cost Calculation

Estimate marketplace-related costs such as commission, transaction fees, advertising cost, and expected return cost.

### 5. Unit Economics

Calculate break-even price, contribution margin, contribution margin percentage, and competitive price headroom.

### 6. Scenario Comparison

Compare pessimistic, base, and optimistic outcomes by product and category.

### 7. Viability Classification

Classify each product as:

```text
Viable
Conditional
Not viable
```

based on contribution margin and competitive price headroom.

## Dashboard Overview

The planned Power BI dashboard, named **Marketplace Viability Command Center**, will present the final analysis in a business-friendly format.

Planned dashboard pages:

### Page 1: Executive Viability Summary

Designed to answer:

```text
Which products appear viable, conditional, or not viable?
```

Planned visuals:

* Viable product count
* Conditional product count
* Not viable product count
* Average contribution margin
* Product viability table
* Scenario comparison chart

### Page 2: Unit Economics Detail

Designed to answer:

```text
Where does the margin go for each product?
```

Planned visuals:

* Cost waterfall
* Break-even price card
* Contribution margin card
* Cost component table
* Product and scenario slicers

### Page 3: Marketplace Competition

Designed to answer:

```text
How does the modeled reseller price compare with observed marketplace competition?
```

Planned visuals:

* Local versus cross-border delivered price comparison
* Competitive price headroom by product
* Delivery-time comparison
* Rating and review-count context
* Viability reason table

The dashboard will be powered by exported CSV files from DuckDB SQL marts.

## Key Metrics

### Supplier Cost in THB

Converts the observed supplier price into Thai Baht.

```text
supplier_cost_thb_est = selected_unit_price × fx_rate_to_thb
```

### Landed Cost

Estimates the total cost of getting one unit ready for resale.

```text
landed_cost_thb_est =
    supplier_cost_thb_est
  + international_shipping_thb_est
  + import_duty_thb_est
  + import_vat_thb_est
  + packaging_cost_thb_est
```

### Platform Fees

Estimates marketplace and transaction fees.

```text
platform_fee_thb_est =
    selling_price_thb × total_platform_fee_rate
```

### Expected Return Cost

Estimates expected return-related cost per sold unit.

```text
expected_return_cost_thb_est =
    return_rate × cost_per_return_thb
```

### Total Variable Cost

Combines all variable costs needed to sell one unit.

```text
total_variable_cost_thb_est =
    landed_cost_thb_est
  + platform_fee_thb_est
  + advertising_cost_thb_est
  + expected_return_cost_thb_est
```

### Contribution Margin

Estimates the margin remaining after variable costs.

```text
contribution_margin_thb_est =
    selling_price_thb
  - total_variable_cost_thb_est
```

### Contribution Margin Percentage

Shows contribution margin as a percentage of selling price.

```text
contribution_margin_pct_est =
    contribution_margin_thb_est / selling_price_thb
```

### Break-Even Price

Estimates the minimum selling price required to cover variable costs.

```text
break_even_price_thb_est =
    fixed_per_unit_costs / (1 - variable_fee_rate)
```

### Competitive Price Headroom

Compares the observed cross-border delivered price against the reseller break-even price.

```text
competitive_price_headroom_thb_est =
    observed_cross_border_delivered_price_thb_obs
  - break_even_price_thb_est
```

Interpretation:

```text
Positive = room to compete above break-even
Zero = competitor price equals break-even
Negative = competitor price is below break-even
```

### Viability Status

Classifies each product based on margin and competitive headroom.

```text
Viable = positive margin and positive competitive headroom
Conditional = positive margin but limited competitive headroom
Not viable = negative margin or competitor price below break-even
```

## Project Structure

Planned structure:

```text
.
├── README.md
├── config/
│   └── assumptions.yaml
├── data/
│   └── observations/
│       ├── marketplace_observations.csv
│       └── supplier_cost_benchmarks.csv
├── dashboard/
├── images/
├── outputs/
├── requirements.txt
├── sql/
├── src/
└── tests/
```

As the project develops, additional files will be added for:

```text
Python transformations
DuckDB schema
SQL marts
data quality checks
pytest tests
Power BI dashboard screenshots
```

## Data Quality Checks

Planned checks include:

### Observation Checks

* Required columns exist
* Observation dates are present
* Listed prices are positive
* Shipping fees are non-negative
* Seller type is valid
* Match quality is valid
* Each product has at least one local and one cross-border observation
* Product IDs are not missing

### Supplier Benchmark Checks

* Required columns exist
* Supplier prices are positive
* FX rates are present when needed
* Match quality is valid
* Minimum order quantity is non-negative
* Supplier-cost benchmarks exist for every analyzed product

### Assumption Checks

* Required assumption keys exist
* Fee rates are between 0 and 1
* Return rates are between 0 and 1
* Scenario names are present
* Assumptions include source and effective-date fields where applicable

### Output Checks

* Unit-economics output is not empty
* No negative cost components
* Contribution margin formulas reconcile
* Break-even price formulas reconcile
* Viability status is populated
* Observed and estimated fields are clearly labeled

## Common Commands

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

Future pipeline command:

```bash
python -m src.run_pipeline
```

Open the DuckDB database after it is created:

```bash
duckdb thailand_reseller_viability.duckdb
```

## Limitations

This project is a scenario-based analytics model, not a complete business plan.

Important limitations:

* Marketplace prices are point-in-time observations and may change frequently
* Supplier prices are public benchmarks, not negotiated purchase prices
* Shipping and import-cost assumptions are estimates
* Platform fees can vary by category, program, seller status, and date
* Seller type may not always be visible or perfectly classified
* Contribution margin is not the same as net profit
* The model excludes labor, rent, working capital, storage, business registration, and overhead
* The sample size is intentionally small for the MVP
* Results should not be generalized to the entire Thailand e-commerce market

The purpose of this project is to demonstrate a structured pricing and unit-economics analysis workflow using transparent assumptions and public observations.

## Conclusion and Next Steps

This project evaluates a practical pricing and marketplace strategy question: whether a Thailand-based reseller can still earn an acceptable margin when competing against cross-border marketplace sellers.

The first version will focus on a small manually collected pilot dataset so that the business logic, assumptions, and data model can be tested before expanding the project.

Next improvements are:

* Collect the initial two-product pilot dataset
* Validate the observation templates
* Build the first Python transformation script
* Create the DuckDB schema
* Calculate landed cost and contribution margin
* Add scenario-based viability classifications
* Add data-quality checks and pytest tests
* Build the Marketplace Viability Command Center dashboard

The long-term goal is to turn this into a clear pricing and unit-economics portfolio project that complements the fantasy football draft analyzer by showing business-oriented margin analysis, scenario modeling, and dashboard reporting.