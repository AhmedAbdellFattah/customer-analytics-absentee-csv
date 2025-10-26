# preprocess.py
import sys, os, pandas as pd, numpy as np, subprocess
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def main():
    if len(sys.argv) < 2:
        print('Usage: python preprocess.py <path/to/csv>'); sys.exit(1)
    path = sys.argv[1]
    df = pd.read_csv(path)
    print(f'[preprocess] Loaded {path} shape={df.shape}')

    # Data cleaning: drop duplicates
    before = df.shape[0]
    df = df.drop_duplicates().reset_index(drop=True)
    print(f'[preprocess] Dropped duplicates: {before - df.shape[0]} rows removed')

    # Fill missing: numeric -> median, categorical -> mode
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    for c in num_cols:
        df[c] = df[c].fillna(df[c].median())
    for c in cat_cols:
        df[c] = df[c].fillna(df[c].mode()[0] if not df[c].mode().empty else 'missing')

    # Feature transformation: encode categorical, scale numeric
    if cat_cols:
        df_enc = pd.get_dummies(df[cat_cols], drop_first=True, dummy_na=False)
    else:
        df_enc = pd.DataFrame(index=df.index)

    scaler = StandardScaler()
    if num_cols:
        scaled = pd.DataFrame(scaler.fit_transform(df[num_cols]), columns=num_cols, index=df.index)
    else:
        scaled = pd.DataFrame(index=df.index)

    df_trans = pd.concat([scaled, df_enc], axis=1)

    # Discretization: bin first numeric column into quartiles (if exists)
    if num_cols:
        col_to_bin = num_cols[0]
        try:
            df[f'{col_to_bin}_bin'] = pd.qcut(df[col_to_bin].rank(method='first'), q=4, labels=False, duplicates='drop')
            df_trans[f'{col_to_bin}_bin'] = df[f'{col_to_bin}_bin'].astype(float).fillna(-1)
        except Exception as e:
            print('[preprocess] Binning failed:', e)

    # Dimensionality reduction: PCA (keep up to 5 components)
    if df_trans.shape[1] > 0:
        k = min(5, df_trans.shape[1])
        pca = PCA(n_components=k, random_state=42)
        pcs = pca.fit_transform(df_trans.values)
        pc_cols = [f'PC{i+1}' for i in range(pcs.shape[1])]
        final_df = pd.DataFrame(pcs, columns=pc_cols, index=df.index)
        print(f'[preprocess] Applied PCA: kept {pcs.shape[1]} components')
    else:
        final_df = df_trans

    out = 'data_preprocessed.csv'
    final_df.to_csv(out, index=False)
    print(f'[preprocess] Saved preprocessed -> {out} shape={final_df.shape}')

    subprocess.run([sys.executable, 'analytics.py', out], check=True)

if __name__ == '__main__':
    main()
