#!/bin/bash

set -euo pipefail

for F in [[:alpha:]]*.md; do
    echo ======================================================================
    echo $F
    echo ======================================================================
    python3.11 function-sections.py $F
done
