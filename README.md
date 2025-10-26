# customer-analytics-absentee-csv

**Team:**  
- **Ahmed Mohamed AbdelFattah (Team Leader)** — 202001160  
- **Ahmed Hesham Abdelaziz** — 202002082

This project was built from the uploaded CSV `Absenteeism_at_work.csv`.

## Files included
- `Dockerfile`  
- `ingest.py`  
- `preprocess.py`  
- `analytics.py`  
- `visualize.py` (uses matplotlib)  
- `cluster.py`  
- `summary.sh`  
- `README.md` (this file)  
- `data/Absenteeism_at_work.csv`  
- `results/` (contains outputs produced by a pipeline run)

---

## Purpose
A reproducible data-processing pipeline that ingests the dataset, preprocesses it, produces textual insights and a visual summary, performs K-Means clustering, and saves outputs for submission.

---

## Run locally (recommended)
1. (Optional) create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   # .\venv\Scripts\Activate  # Windows PowerShell
   ```

2. Install required Python packages:
   ```bash
   pip install --upgrade pip
   pip install pandas numpy matplotlib scikit-learn scipy requests
   ```

3. Run the pipeline (starts at ingest and chains automatically):
   ```bash
   python ingest.py data/Absenteeism_at_work.csv
   ```

4. After completion the following outputs will be present in the project root:
   - `data_raw.csv`  
   - `data_preprocessed.csv`  
   - `insight1.txt`, `insight2.txt`, `insight3.txt`  
   - `summary_plot.png`  
   - `clusters.txt`

---

## Run with Docker
1. (Optional) If using the original `.xls` you may need to add `xlrd` to the `Dockerfile` pip install line. For this CSV-based project the included Dockerfile is sufficient.

2. Build the image:
   ```bash
   docker build -t customer-analytics-absentee-csv:latest .
   ```

3. Run interactively (bind host `data/` and `results/` so outputs are visible on host):
   ```bash
   docker run -it --name customer_pipeline      -v "$(pwd)/data":/app/pipeline/data      -v "$(pwd)/results":/app/pipeline/results      customer-analytics-absentee-csv:latest
   ```
   Then inside the container run:
   ```bash
   python ingest.py /app/pipeline/data/Absenteeism_at_work.csv
   ```

4. Or run one-shot from host (overrides default `CMD`):
   ```bash
   docker run --name customer_pipeline      -v "$(pwd)/data":/app/pipeline/data      -v "$(pwd)/results":/app/pipeline/results      customer-analytics-absentee-csv:latest      python ingest.py /app/pipeline/data/Absenteeism_at_work.csv
   ```

5. If you run without bind-mounting `results/`, use the included `summary.sh` on the host to copy outputs out of a running container:
   ```bash
   ./summary.sh <container_id_or_name>
   ```

---

## Execution flow (script chaining)
1. `python ingest.py <input.csv>`  
   → writes `data_raw.csv` and calls:
2. `preprocess.py data_raw.csv`  
   → writes `data_preprocessed.csv` and calls:
3. `analytics.py data_preprocessed.csv`  
   → writes `insight1.txt`, `insight2.txt`, `insight3.txt` and calls:
4. `visualize.py data_preprocessed.csv`  
   → writes `summary_plot.png` and calls:
5. `cluster.py data_preprocessed.csv`  
   → writes `clusters.txt`

---

## Notes & tips
- Preprocessing includes duplicate removal, missing-value handling (median for numeric, mode for categorical), encoding categorical variables, scaling numeric features, discretization of the first numeric column (quartiles), and PCA to up to 5 components.
- Clustering uses K-Means with `k=3` (or fewer if the dataset is tiny) and `random_state=42` for reproducibility.
- The pipeline scripts chain automatically; starting from `ingest.py` will run the full pipeline.
- If running in Docker and `pip` fails to compile some scientific packages, ensure your Docker host has internet access and the Dockerfile includes system build dependencies (the provided Dockerfile installs typical build deps like `build-essential`, `libopenblas-dev`, etc.).
- If you prefer, convert `.xls` to `.csv` (or add `xlrd` to the Dockerfile) before running.

---

## Contact / Authors
- **Ahmed Mohamed AbdelFattah (Team Leader)** — 202001160  
- **Ahmed Hesham Abdelaziz** — 202002082

--- 

*Prepared for: Nile University — CSCI461: Introduction to Big Data*
