SPHINXMAKE = $(MAKE) -C docs

schema:
	uv run python manage.py spectacular --file docs/source/openapi.yaml --validate

docs-html: schema
	$(SPHINXMAKE) html

docs-pdf: schema
	$(SPHINXMAKE) latex
	make -C docs/build/latex

tags:
	fdfind -e py -X etags
