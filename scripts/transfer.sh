python3 scripts/generate_minidb.py
python3 scripts/generate_descriptions.py
R -f scripts/generate_graphs.R
python3 scripts/benchmark_html.py
git add benchmarks
git add _includes
git add _data
git add images/graphs/
git add minibenchmarks.db
git commit -m "Update benchmarks"
git push

