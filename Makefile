RUN = uv run
CODE = src/venomx
MODEL = $(CODE)/model

.PHONY: all
all: test models

.PHONY: test
test: doctest
	$(RUN) pytest tests

.PHONY: pytest
pytest:
	$(RUN) pytest

.PHONY: apidoc
apidoc:
	$(RUN) sphinx-apidoc -f -M -o docs/ $(CODE)/ && cd docs && $(RUN) make html

.PHONY: apidoc
doctest:
	$(RUN) python -m doctest --option ELLIPSIS --option NORMALIZE_WHITESPACE $(CODE)/tools/*.py

%-doctest: %
	$(RUN) python -m doctest --option ELLIPSIS --option NORMALIZE_WHITESPACE $<

.PHONY: models
models: $(MODEL)/venomx.py

$(MODEL)/%.py: $(MODEL)/%.yaml
	$(RUN) gen-pydantic --pydantic-version 2 $< > $@.tmp && mv $@.tmp $@
