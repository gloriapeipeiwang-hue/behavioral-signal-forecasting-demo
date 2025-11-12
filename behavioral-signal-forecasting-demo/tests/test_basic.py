from src.pipeline.aggregate_and_join import agg_daily
import pandas as pd

def test_agg_daily_basic():
    df = pd.read_csv('data/electronics_scored.sample.csv.gz')
    df.to_csv('data/tmp.csv.gz', index=False)
    out = agg_daily('data/tmp.csv.gz', 'data/tmp_out.csv.gz')
    assert set(['n','sent_mean','stars_mean']).issubset(out.columns)
