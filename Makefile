RUN = poetry run
CODE = src/venomx
MODEL = $(CODE)/model

all: test models

test: pytest doctest


pytest:
	$(RUN) pytest

apidoc:
	$(RUN) sphinx-apidoc -f -M -o docs/ $(CODE)/ && cd docs && $(RUN) make html

doctest:
	$(RUN) python -m doctest --option ELLIPSIS --option NORMALIZE_WHITESPACE $(CODE)/tools/*.py

%-doctest: %
	$(RUN) python -m doctest --option ELLIPSIS --option NORMALIZE_WHITESPACE $<

models: $(MODEL)/venomx.py

$(MODEL)/%.py: $(MODEL)/%.yaml $(MODEL)/embedding.yaml
	$(RUN) gen-pydantic --pydantic-version 2 $< > $@.tmp && mv $@.tmp $@
