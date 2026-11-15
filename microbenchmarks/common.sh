# Common settings and helper functions for the microbenchmark scripts.
# Source this file from the scripts: source "$(dirname "$0")/common.sh"
#
# Environment variables:
#   DUCKDB    path to the DuckDB CLI binary (default: duckdb)
#   DATA_DIR  directory containing the input datasets (default: current directory)
#   WORK_DIR  directory where the database files and the results are created (default: current directory)
#   RUNS      number of times each query is executed, the median is reported (default: 5)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DUCKDB="${DUCKDB:-duckdb}"
DATA_DIR="$(cd "${DATA_DIR:-.}" && pwd)"
WORK_DIR="$(cd "${WORK_DIR:-.}" && pwd)"
RUNS="${RUNS:-5}"

# Turn off the CLI's agent mode (DuckDB 2.0+) to keep the output format stable
export DUCKDB_AGENT_MODE=0

echo "DuckDB version: $(${DUCKDB} -batch -noheader -csv -c 'SELECT version();')"

# Runs a command and prints its wall-clock time in seconds.
# The command's stdout is discarded, its stderr is appended to errors.log.
timed() {
    local TIMEFORMAT='%3R'
    { time "$@" > /dev/null 2>> "${WORK_DIR}/errors.log"; } 2>&1
}

# Runs a query RUNS times in a single DuckDB process and prints the median of the query times.
# Usage: median_query_time ⟨database_file⟩ ⟨query⟩
median_query_time() {
    local db="$1"
    local query="$2"
    if [ ! -f "${db}" ]; then
        echo "Database file ${db} does not exist" >&2
        return 1
    fi
    local args=(-c "SET enable_progress_bar = false;" -c ".timer on")
    for _ in $(seq 1 "${RUNS}"); do
        args+=(-c "${query}")
    done
    ${DUCKDB} -csv "${db}" "${args[@]}" 2>&1 \
        | grep '^Run Time' \
        | awk '{print $5}' \
        | sort -n \
        | awk '{a[NR] = $1} END {print a[int((NR + 1) / 2)]}'
}

# Prints the size of a file in bytes
file_size() {
    wc -c < "$1" | tr -d ' '
}
