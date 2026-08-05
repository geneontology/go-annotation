# CLAUDE.md — go-annotation

Instructions for agents working in this repo. Keep this file terse; extend it as conventions solidify.

## What this repo is

Two things in one repo:

1. **Issue tracker** for GO annotation requests (the bulk of activity — curator-driven, not code).
2. **Label-triggered GitHub Actions report runner** that dumps TSVs of annotations into `reports/<issue-number>/` on `master` when an issue is opened with a matching label.

The code surface is small. Most commits are issue-template nudges, spec tweaks, or auto-commits from the runner. The "software" commits — scripts and workflows — are what an agent usually touches.

## Layout

- `scripts/` — Python reporters pulling from GOlr + `external2go`.
  - `annotation-review-report.py` — main reporter, GOlr Solr query → GAF-like TSV.
  - `mapping-report.py` — greps GO terms out of `external2go` mapping files.
  - `extension-report.py` — variant of the review reporter (currently untracked; confirm before committing).
- `.github/workflows/` — label-gated runners.
  - `report-direct-ann-term.yml` → label `direct_ann_to_list_of_terms`.
  - `report-regulates-ann-term.yml` → label `reg_ann_to_list_of_terms`.
- `specs/` — human-authored GPAD/GPI format specs (`gpad-gpi-1_0.md`, `gpad-gpi-1_2.md`, `gpad-gpi-2-0.md`) plus UML PNGs. Curator-owned; don't edit without asking.
- `reports/` — archive of auto-committed TSV outputs, one subdirectory per issue number (655+ entries). Treated as immutable output. **Do not edit, reformat, rename, or rewrite history for anything under `reports/`** — the commit messages are permalinked into issue comments and rewriting breaks them.
- `README.md` — also houses the curator housekeeping SOP for `annotation review` and `PAINT` labels.
- `CONTRIBUTING.md` — guidelines for *ticket authors*, not contributors of code.

## Runtime and deps

- Workflows run on `ubuntu-22.04` with system `python3`. No venv, no `requirements.txt`, no `pyproject.toml`.
- Script runtime deps: `requests`, `pytz`, stdlib. Stay within that unless the task requires more — and if it does, install in the workflow step, not globally.
- No test suite, no linter config. Scripts are standalone and copy-paste-evolved — don't introduce a package structure or shared-utils module without discussing it first.

## Code style (match what's there)

- `argparse` at top of file, verbose flag toggles `logging.INFO`.
- `die_screaming()` idiom for fatal exits (sets non-zero status so CI notices).
- Globals at module scope are fine; the existing scripts comment "they were here before I got here--don't judge" — don't refactor them away just because.
- Scripts are self-contained: new reporter → new `scripts/<name>.py`, new workflow → new `.github/workflows/<name>.yml`, don't factor.
- Keep comments sparse; explain *why* not *what*.

## Commit conventions

- Every software commit links to an issue. Examples from history:
  - `draft attempt and script and workflow for #4559`
  - `switch to evidence_closure and try to add union for ECO_0000006 and ECO_0000204; for #4963`
  - `catch fixes and debugging up; for geneontology/annotation-query#104` (cross-repo form)
- Matches the `pipeline-from-goa` trailer convention (`; for org/repo#NN`). Prefer this style here too.
- The auto-commit workflow uses `sjcarbon@lbl.gov` as the committer; don't change it casually.
- Never rewrite history that touches `reports/`.

## External services

- **GOlr Solr** — `https://golr-aux.geneontology.io/solr/select?...`. Existing scripts still use `http://` URLs; Cloudflare 301s them to HTTPS and `requests` follows silently, so they keep working. Prefer `https://` in new code. Canonical `fl` field list lives in `annotation-review-report.py`; add new fields there.
  - **GOlr flattens with/from grouping.** `evidence_with` is a flat multi-valued field, and no value anywhere in the index contains a comma (`fq=evidence_with:*,*` → `numFound: 0`, checked 2026-08-05). So `A,B` (AND) and `A|B` (OR) are indistinguishable by the time a reporter here sees them — see [GPAD 2.0 with/from semantics](#gpad-20-withfrom-column-7-semantics). A report that needs the grouping must read the GPAD/GAF files, not GOlr.
- **External2go snapshot** — `http://snapshot.geneontology.org/ontology/external2go/`; the `reg` workflow `wget -r`'s it and then prunes specific files (`pfam2go`, `pirsf2go`, …) — mirror that pattern if adding another mapping reporter.
- **GitHub issue search** — plain REST, `api.github.com/search/issues`. No auth in scripts; rate limits apply, scripts `time.sleep(10)` before calling.

## GPAD 2.0 with/from (column 7) semantics

`specs/gpad-gpi-2-0.md` glosses column 7 in one line — "Pipe-separated entries represent independent evidence; comma-separated entries represent grouped evidence". That is a *compression*, not the whole rule, and the operative statement is not in the spec. Traced 2026-08-05; the sources below save re-digging it.

- **Pipe = OR, comma = AND, precedence is OR-of-ANDs**: `A,B|C,D|E` parses as `(A,B)|(C,D)|E`, and pipe-separated entries are equivalent to separate annotations. Stated by the author of that spec line in [go-annotation#3031](https://github.com/geneontology/go-annotation/issues/3031) (2020-06), three months after writing it. The sentence itself compresses [go-annotation#2349](https://github.com/geneontology/go-annotation/pull/2349) ("The comma means AND, not OR", 2019-05), which is also where the "triply mutant" example comes from.
- **The fullest published statement is on a superseded page** — [GAF 2.1](https://geneontology.org/docs/go-annotation-file-gaf-format-2.1/), still served but delisted from site nav. GAF 2.2 and the GPAD 2.0 docs page now carry the same short wording as the spec (verbatim identical to each other); the long OR/AND paragraph was narrowed to the annotation-extension column in Oct 2025 — no rationale traced yet in commit, PR, or issue history.
- **Per-evidence-code operator limits are unstated and unenforced.** GAF 2.1 allowed commas only for IMP/IGI/IPI/IC/IGC. No current spec repeats it, no GORULE checks it (`go-site` `metadata/rules/*.md` contains zero "comma"), and the `with_structure: simple|compound` key in `go-site`'s `eco-usage-constraints.yaml` that encodes the same split is read by nothing. Released files still honour it in practice.
- For behaviour rather than prose, `ontobio` is the reference parser: `ConjunctiveSet` splits on `|` then `,`, for both GAF and GPAD.

## Label → workflow wiring

Adding a new report type = three coordinated edits:

1. Add/mint a GitHub label on the repo.
2. New workflow file under `.github/workflows/` (clone one of the two existing, change the `if: contains(...labels...)` guard and the `--label` / `--field` args).
3. Script either reuses `annotation-review-report.py` with new `--field` / `--prefix`, or a new `scripts/<name>.py`.

Workflows trigger on `issues: [opened]`. There's an inline TODO in both workflow files about possibly switching to `locked`; don't change this speculatively.

## Things to check with me first

- Touching `reports/` in any way (bulk cleanup, reorganization, archival).
- Editing `specs/gpad-gpi-*.md` — these are curator-authored (pgaudet et al.); propose via issue.
- Mass issue operations (closing, relabeling, commenting across many tickets).
- Adding dependencies, a test harness, a linter, or a packaging layout. The repo has intentionally stayed minimal.
- Anything that changes the auto-commit identity or the `stefanzweifel/git-auto-commit-action` usage.

## Sibling repos that overlap

- `geneontology/annotation-query` — closely related reporter scripts; changes here and there often move together (see commit `03bba9c`).
- `geneontology/pipeline-from-goa` — upstream data ingest feeding GOlr. Shares the `; for org/repo#NN` commit-trailer convention.
- `geneontology/operations` — documents the hosts behind `snapshot.geneontology.org` and `golr-aux.geneontology.io`; check there when debugging endpoint issues.
- `geneontology/go-ontology` — authoritative source for GO terms referenced in tickets (obsoletion reviews link back here).
- `geneontology/go-site` / `geneontology/go-fastapi` — downstream public surface for the data this repo's reports describe.

## Out-of-scope referrals (from CONTRIBUTING.md / README.md)

- UniProt / HAMAP / UniPathway issues → `help@uniprot.org` or `http://www.uniprot.org/update`.
- EBI GOA / QuickGO / Protein2GO → `goa@ebi.ac.uk`.

If a ticket or task lands here that really belongs to one of those, flag it rather than trying to satisfy it locally.
