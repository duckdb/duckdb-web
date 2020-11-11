mkdir -p ../benchmark-results
mkdir -p ../benchmark-results/graphs
R -f scripts/generate_graphs.R
python3 scripts/generate_parquet.py
scp -r ../benchmark-results/ duckdbdemo:/local/home/da-duckdbdemo/dbroot/
