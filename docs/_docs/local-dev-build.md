---
layout: page
title: Local MDL Build and Testing
permalink: /docs/local-dev-build/
---

### Local MDL Build and Testing

This guide shows how to build and test a local version of MDL that mirrors production, while keeping your global `mdl` intact. The local build installs as `mdlbeta`.

### Quickstart

```bash
# from repo root
make local-mdl
# or step-by-step
make dev-sync   # copies production assets/templates into local source
make dev-build  # builds and installs editable as mdlbeta
make dev-test   # smoke tests using mdlbeta

# If your environment blocks pip installs (PEP 668), use the wrapper:
make mdlbeta
./scripts/mdlbeta --help
./scripts/mdlbeta build --mdl test_examples/hello_world.mdl -o dist
```

After success:

```bash
mdlbeta --help
mdlbeta --version
```

### What gets synced

The script copies non-code assets (if they exist upstream) from the published production package into your local `minecraft_datapack_language/` folder:

- assets/
- resources/
- templates/
- completions/
- data/
- static/

This ensures `mdlbeta` behaves like production with respect to templates and other goodies.

Pin a production version with:

```bash
MDL_PROD_VERSION=1.2.3 make dev-sync
```

### Commands

- make dev-sync: Run `scripts/sync_prod_assets.sh`
- make dev-build: Run `scripts/dev_build.sh` (editable install provides `mdlbeta`)
- make dev-test: Run `scripts/test_dev.sh` smoke tests
- make local-mdl: Sync + install + run smoke tests in one step

### Manual use of helper

```bash
scripts/local_mdl.sh --test
```

### Notes

- Global `mdl` remains unchanged; use `mdlbeta` for local testing.
- If you change code, re-run `make dev-build` to refresh `mdlbeta`.
- Re-run `make dev-sync` when production adds new assets/templates.

