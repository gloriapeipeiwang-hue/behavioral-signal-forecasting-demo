import argparse, os, requests, pandas as pd
URL = "https://amazon-reviews-pds.s3.amazonaws.com/tsv/amazon_reviews_us_Electronics_v1_00.tsv.gz"
def stream_download(url, out_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: f.write(chunk)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='data/amazon_electronics.tsv.gz')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    print('Downloading...', URL)
    stream_download(URL, args.out)
    if args.limit>0:
        df = pd.read_csv(args.out, sep='\t', compression='gzip', on_bad_lines='skip', nrows=args.limit)
        small = args.out.replace('.tsv.gz', f'.head{args.limit}.csv.gz')
        df.to_csv(small, index=False, compression='gzip')
        print('Subset:', small)
if __name__=='__main__':
    main()
