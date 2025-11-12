import argparse, pandas as pd, numpy as np, joblib, matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, precision_recall_curve, auc
from pathlib import Path

FEATS = ['n','sent_mean','stars_mean','n_chg','sent_mean_chg','stars_mean_chg','n_lag1','sent_mean_lag1','stars_mean_lag1']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--joined', required=True)
    ap.add_argument('--model_out', default='models/logreg.pkl')
    ap.add_argument('--out_dir', default='results')
    args = ap.parse_args()
    df = pd.read_csv(args.joined, compression='gzip', parse_dates=['day'])
    X = df[FEATS].values
    y = df['y_up'].values
    pipe = Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression(max_iter=300))])
    pipe.fit(X, y)
    prob = pipe.predict_proba(X)[:,1]
    fpr, tpr, _ = roc_curve(y, prob); roc_auc = auc(fpr, tpr)
    prec, rec, _ = precision_recall_curve(y, prob); pr_auc = auc(rec, prec)
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    import matplotlib.pyplot as plt
    plt.figure(); plt.plot(fpr, tpr); plt.plot([0,1],[0,1],'--'); plt.xlabel('FPR'); plt.ylabel('TPR'); plt.title('ROC'); plt.tight_layout(); plt.savefig(f"{args.out_dir}/roc.png", dpi=180); plt.close()
    plt.figure(); plt.plot(rec, prec); plt.xlabel('Recall'); plt.ylabel('Precision'); plt.title('PR'); plt.tight_layout(); plt.savefig(f"{args.out_dir}/pr.png", dpi=180); plt.close()
    joblib.dump(pipe, args.model_out)
    with open(f"{args.out_dir}/metrics.txt","w") as f:
        f.write(f"ROC_AUC={roc_auc:.3f}\nPR_AUC={pr_auc:.3f}\n")
    print('Saved', args.model_out, 'ROC_AUC=', roc_auc, 'PR_AUC=', pr_auc)

if __name__=='__main__':
    main()
