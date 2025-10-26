# ingest.py (CSV)
import sys, os, pandas as pd, subprocess

def main():
    if len(sys.argv) < 2:
        print('Usage: python ingest.py <path/to/dataset.csv>')
        sys.exit(1)
    src = sys.argv[1]
    if not os.path.exists(src):
        print(f'File not found: {src}'); sys.exit(1)
    df = pd.read_csv(src)
    out = 'data_raw.csv'
    df.to_csv(out, index=False)
    print(f'[ingest] Saved raw data -> {out} (shape={df.shape})')
    subprocess.run([sys.executable, 'preprocess.py', out], check=True)

if __name__ == '__main__':
    main()
