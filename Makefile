
.phony: initial-run local-run format-check format-fix

format-check:
	black --check --skip-string-normalization --verbose --diff --color scripts/*.py

format-fix:
	black --skip-string-normalization scripts/*.py


initial-run:
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt && \
	 ./scripts/serve-latest.sh

local-run:
	source venv/bin/activate && ./scripts/serve-latest.sh
