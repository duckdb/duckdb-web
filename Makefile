
format-check:
	black --check --skip-string-normalization --verbose --diff --color scripts/*.py

format-fix:
	black --skip-string-normalization scripts/*.py
