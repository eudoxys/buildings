# Package

- [x] Bring the repository in line with the Eudoxys package guidelines (see `CLAUDE.md`, `MANIFEST.md`)

- [x] Fast offline tests and a validation workflow (see `buildings/_test/`)

- [ ] Replace progress `print` calls in `Buildings.__init__` with logging or a progress option

- [ ] Fix the county suffix-stripping line in `Buildings.__init__` (joins characters, not words)

- [ ] Check and regenerate published county files for counties with one building (written transposed before the `to_counties` fix)

- [ ] Write the per-state index HTML that `buildings/_make_index.py` computes but doesn't save

- [ ] First release (`pyproject.toml` version `YEAR.MONTH.0`)

# Data

- [ ] Record the AutoBEM retrieval date and per-state building counts in `buildings/README.md`
