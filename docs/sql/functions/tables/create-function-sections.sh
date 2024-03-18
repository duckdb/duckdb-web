#!/bin/bash

set -euo pipefail

for F in *.md; do
    echo ======================================================================
    echo $F
    echo ======================================================================
    python3.11 function-sections.py $F
done
