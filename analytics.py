# analytics.py
import sys, pandas as pd, numpy as np, subprocess
def main():
    if len(sys.argv) < 2:
        print('Usage: python analytics.py <path/to/preprocessed.csv>'); sys.exit(1)
    path = sys.argv[1]
    df = pd.read_csv(path)
    print(f'[analytics] Loaded {path} shape={df.shape}')

    # Insight 1: shape + columns
    insight1 = f'Rows: {df.shape[0]}, Columns: {df.shape[1]}\nColumns: {", ".join(df.columns.tolist())}\n'

    # Insight 2: top features by variance
    variances = df.var(numeric_only=True).sort_values(ascending=False)
    insight2 = 'Top 3 features by variance:\n'
    for col, var in variances.head(3).items():
        insight2 += f'- {col}: variance={var:.4f}\n'

    # Insight 3: basic numeric summary
    means = df.select_dtypes(include=[np.number]).mean()
    mean_of_means = means.mean() if not means.empty else float('nan')
    n_nans = df.isna().sum().sum()
    insight3 = f'Numeric features count: {len(means)}\nMean of feature means: {mean_of_means:.4f}\nTotal missing values: {int(n_nans)}\n'

    with open('insight1.txt','w') as f: f.write(insight1)
    with open('insight2.txt','w') as f: f.write(insight2)
    with open('insight3.txt','w') as f: f.write(insight3)

    print('[analytics] Wrote insight1.txt, insight2.txt, insight3.txt')
    subprocess.run([sys.executable, 'visualize.py', path], check=True)

if __name__ == '__main__':
    main()
