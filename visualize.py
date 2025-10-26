# visualize.py - uses matplotlib only
import sys, pandas as pd, numpy as np, subprocess
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 2:
        print('Usage: python visualize.py <path/to/preprocessed.csv>'); sys.exit(1)
    path = sys.argv[1]
    df = pd.read_csv(path)
    numeric = df.select_dtypes(include=[np.number])
    if numeric.shape[1] >= 2:
        corr = numeric.corr()
        fig, ax = plt.subplots(figsize=(8,6))
        cax = ax.matshow(corr, vmin=-1, vmax=1)
        fig.colorbar(cax)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=90)
        ax.set_yticklabels(corr.columns)
        plt.title('Correlation heatmap (preprocessed features)')
        plt.tight_layout()
        plt.savefig('summary_plot.png', dpi=150)
        plt.close()
        print('[visualize] Saved summary_plot.png (heatmap)')
    elif numeric.shape[1] == 1:
        fig, ax = plt.subplots()
        ax.hist(numeric.iloc[:,0].dropna(), bins=20)
        ax.set_title(f'Histogram of {numeric.columns[0]}')
        plt.tight_layout()
        plt.savefig('summary_plot.png', dpi=150)
        plt.close()
        print('[visualize] Saved summary_plot.png (histogram)')
    else:
        col = df.columns[0]
        vc = df[col].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(6,4))
        ax.barh(vc.index.astype(str), vc.values)
        ax.set_title(f'Top values in {col}')
        plt.tight_layout()
        plt.savefig('summary_plot.png', dpi=150)
        plt.close()
        print('[visualize] Saved summary_plot.png (barplot)')

    subprocess.run([sys.executable, 'cluster.py', path], check=True)

if __name__ == '__main__':
    main()
