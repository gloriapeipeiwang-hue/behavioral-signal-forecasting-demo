# Behavioral Signal Forecasting Demo

**End-to-end pipeline linking sentiment and behavioral signals to retail sales trends**

---

## Overview
This demo illustrates a **real-time behavioral signal forecasting system** for the **Electronics & Appliances** retail sector.  
It uses **simulated multi-source streaming data** (product reviews, search queries, and social mentions) combined with **public U.S. Census retail sales data** to forecast **weekly sales shifts**.

The project showcases how behavioral and sentiment indicators can anticipate demand fluctuations and support marketing optimization decisions.

---

## Key Features
- **Data Simulation:** Generates 60 days of event-level sentiment and behavioral signals with category-level variation.
- **Feature Aggregation:** Daily rolling features for sentiment mean, variance, and event volume.
- **Modeling:** Logistic regression for weekly up/down sales forecasting; Random Forest as a robustness check.
- **Evaluation:** ROC and PR curve visualizations with AUC metrics.
- **Automation:** Airflow DAG for daily retraining and evaluation workflow.
- **Visualization:** Category-level forecast trajectories and budget allocation examples.

---

## Tech Stack
- **Python:** `pandas`, `numpy`, `scikit-learn`, `matplotlib`
- **Automation:** `Airflow`
- **Versioning & CI:** Git, GitHub Actions (future integration)
- **Deployment-ready structure:** Modular `src/` folder for reproducible pipeline execution.

---

## Quickstart
```bash
pip install -r requirements.txt

# 1) Generate simulated events
python -m src.demo_pipeline.simulate_stream --days 60 --out data/events_stream.csv.gz

# 2) Aggregate daily features
python -m src.demo_pipeline.featurize --events data/events_stream.csv.gz --out data/category_daily_agg.csv.gz

# 3) Train model and evaluate
python -m src.demo_pipeline.train_models --data data/category_daily_agg.csv.gz --model models/clf_logreg.pkl
python -m src.demo_pipeline.evaluate --data data/category_daily_agg.csv.gz --model models/clf_logreg.pkl --out_dir results
