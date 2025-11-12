import argparse, pandas as pd, numpy as np
from pathlib import Path

def agg_daily(scored_csv, out_csv):
    df = pd.read_csv(scored_csv, compression='gzip', parse_dates=['date'])
    df['day'] = df['date'].dt.date
    g = df.groupby('day').agg(n=('sent_compound','size'), sent_mean=('sent_compound','mean'), sent_std=('sent_compound','std'), stars_mean=('star_rating','mean')).reset_index()
    g['sent_std'] = g['sent_std'].fillna(0.0)
    for col in ['n','sent_mean','stars_mean']:
        g[f'{col}_lag1'] = g[col].shift(1)
        g[f'{col}_chg'] = g[col] - g[f'{col}_lag1']
    g = g.dropna().reset_index(drop=True)
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    g.to_csv(out_csv, index=False, compression='gzip')
    return g

def join_census(daily_csv, census_csv, out_csv):
    d = pd.read_csv(daily_csv, compression='gzip', parse_dates=['day'])
    c = pd.read_csv(census_csv, parse_dates=['month'])
    d['month'] = d['day'].values.astype('datetime64[M]')
    joined = d.merge(c, on='month', how='left').sort_values('day')
    joined['sales_next7'] = joined['sales'].shift(-7)
    joined['y_up'] = (joined['sales_next7'] > joined['sales']).astype(int)
    joined = joined.dropna().reset_index(drop=True)
    joined.to_csv(out_csv, index=False, compression='gzip')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scored', required=True)
    ap.add_argument('--census', required=True)
    ap.add_argument('--daily_out', default='data/daily_agg.csv.gz')
    ap.add_argument('--joined_out', default='data/daily_with_sales.csv.gz')
    args = ap.parse_args()
    agg_daily(args.scored, args.daily_out)
    join_census(args.daily_out, args.census, args.joined_out)

if __name__=='__main__':
    main()
