from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(dag_id='behavioral_signal_forecasting', start_date=datetime(2024,1,1), schedule_interval='@weekly', catchup=False) as dag:
    download = BashOperator(task_id='download_reviews', bash_command='python -m src.pipeline.download_amazon --out data/amazon_electronics.tsv.gz --limit 500000')
    score = BashOperator(task_id='score_sentiment', bash_command='python -m src.pipeline.score_sentiment --inp data/amazon_electronics.tsv.gz --out data/electronics_scored.csv.gz')
    join = BashOperator(task_id='aggregate_join', bash_command='python -m src.pipeline.aggregate_and_join --scored data/electronics_scored.csv.gz --census data/census_electronics_monthly.csv --daily_out data/daily_agg.csv.gz --joined_out data/daily_with_sales.csv.gz')
    train = BashOperator(task_id='train_eval', bash_command='python -m src.pipeline.train_and_eval --joined data/daily_with_sales.csv.gz --model_out models/logreg.pkl --out_dir results')
    download >> score >> join >> train
