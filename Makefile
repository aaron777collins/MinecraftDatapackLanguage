
# Quick helpers for MDL
.PHONY: venv install build sdist wheel pipx-install pipx-uninstall zipapp test clean clean-tmp dev-setup dev-build dev-sync dev-test local-mdl mdlbeta

PYTHON ?= python3

venv:
	$(PYTHON) -m venv .venv

install: venv
	. .venv/bin/activate; pip install -e .

build: ## sdist + wheel
	. .venv/bin/activate || true; python -m pip install -U pip build; python -m build

sdist: build
wheel: build

zipapp:
	python -c "import zipapp; zipapp.create_archive('$(CURDIR)', target='mdl.pyz', interpreter='/usr/bin/env python3', main='minecraft_datapack_language.cli:main', compressed=True)"; \
	echo "Created ./mdl.pyz"

pipx-install:
	pipx install .

pipx-uninstall:
	pipx uninstall minecraft-datapack-language || true

test:
	bash scripts/test_cli.sh

clean:
	rm -rf .venv build dist *.egg-info tmp_mdl_test mdl.pyz

clean-tmp:
	rm -rf .tmp

dev-setup:
	bash scripts/dev_setup.sh

dev-build:
	bash scripts/dev_build.sh

dev-sync:
	bash scripts/sync_prod_assets.sh

dev-test:
	bash scripts/test_dev.sh

local-mdl:
	bash scripts/local_mdl.sh --test

mdlbeta:
	chmod +x scripts/mdlbeta
	@echo "Run with: ./scripts/mdlbeta --help"
