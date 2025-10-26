# cluster.py
import sys, pandas as pd, numpy as np
from sklearn.cluster import KMeans
def main():
    if len(sys.argv) < 2:
        print('Usage: python cluster.py <path/to/preprocessed.csv>'); sys.exit(1)
    path = sys.argv[1]
    df = pd.read_csv(path)
    numeric = df.select_dtypes(include=[np.number])
    if numeric.empty:
        with open('clusters.txt','w') as f: f.write('No numeric features available for clustering.\n'); print('No numeric features'); return
    X = numeric.values
    n_samples = X.shape[0]
    k = 3 if n_samples >= 3 else 1
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    unique, counts = np.unique(labels, return_counts=True)
    with open('clusters.txt','w') as f:
        f.write(f'Total samples: {n_samples}\n')
        for u,c in zip(unique,counts):
            f.write(f'Cluster {int(u)}: {int(c)} samples\n')
    print('[cluster] Wrote clusters.txt')
if __name__ == '__main__':
    main()
