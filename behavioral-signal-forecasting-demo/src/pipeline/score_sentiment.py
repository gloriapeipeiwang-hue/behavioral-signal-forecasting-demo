import argparse, pandas as pd, numpy as np, nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from pathlib import Path

def ensure_vader():
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inp', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    ensure_vader()
    sia = SentimentIntensityAnalyzer()
    df = pd.read_csv(args.inp, sep='\t' if args.inp.endswith('.tsv') or args.inp.endswith('.tsv.gz') else ',', compression='gzip', on_bad_lines='skip')
    if 'review_date' in df.columns:
        df['date'] = pd.to_datetime(df['review_date'], errors='coerce')
    elif 'reviewTime' in df.columns:
        df['date'] = pd.to_datetime(df['reviewTime'], errors='coerce')
    else:
        df['date'] = pd.to_datetime('today')
    txt = df.get('review_body', df.get('reviewText', '')).fillna('').astype(str)
    comp = txt.map(lambda t: sia.polarity_scores(t)['compound'])
    out = pd.DataFrame({'date': df['date'], 'star_rating': df.get('star_rating', df.get('overall', np.nan)), 'sent_compound': comp}).dropna(subset=['date'])
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False, compression='gzip')
    print('Wrote', args.out, 'rows=', len(out))

if __name__=='__main__':
    main()
