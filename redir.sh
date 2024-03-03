#!/bin/bash

for MINOR in 6 7 8; do
    git mv docs/archive/0.${MINOR}.1 docs/archive/0.${MINOR}
    git ci -m "Archive: Move 0.${MINOR}.1 to 0.${MINOR}"
    python3.11 scripts/redirect.py docs/archive/0.${MINOR}.1 docs/archive/0.${MINOR}
    git ci -am "Archive: Add redirect from 0.${MINOR}.1 to 0.${MINOR}"
done

export MINOR=9
export PATCH=2

git mv docs/archive/0.${MINOR}.${PATCH} docs/archive/0.${MINOR}
git ci -m "Archive: Move 0.${MINOR}.${PATCH} to 0.${MINOR}"
python3.11 scripts/redirect.py docs/archive/0.${MINOR}.${PATCH} docs/archive/0.${MINOR}
git ci -am "Archive: Add redirect from 0.${MINOR}.${PATCH} to 0.${MINOR}"

export MINOR=9
export PATCH=1

git rm -rf docs/archive/0.${MINOR}.${PATCH}
git ci -m "Archive: Delete version 0.${MINOR}.${PATCH}"
python3.11 scripts/redirect.py docs/archive/0.${MINOR}.${PATCH} docs/archive/0.${MINOR}
git ci -am "Archive: Add redirect from 0.${MINOR}.${PATCH} to 0.${MINOR}"

export MINOR=9
export PATCH=0

git rm -rf docs/archive/0.${MINOR}.${PATCH}
git ci -m "Archive: Delete version 0.${MINOR}.${PATCH}"
python3.11 scripts/redirect.py docs/archive/0.${MINOR}.${PATCH} docs/archive/0.${MINOR}
git ci -am "Archive: Add redirect from 0.${MINOR}.${PATCH} to 0.${MINOR}"
