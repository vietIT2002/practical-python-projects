# GitHub settings (maintainer actions)

These settings are configured through the GitHub web interface or an
authenticated API, not by editing files in the repository. They are listed here
with exact steps so nothing is missed. None of them are performed automatically.

## Repository description and website

**Settings** are on the repository home page (the gear next to **About**):

- **Description:** `Learn Python by building practical, tested, and production-minded projects.`
- **Website:** leave empty until a documentation site exists.

## Topics

In the **About** panel, add topics:
`python`, `python-projects`, `learn-python`, `beginner-friendly`, `tutorial`,
`cli`, `testing`, `uv`, `automation`, `open-source`, `education`.

Add `fastapi` only once a FastAPI-based project is published, so topics stay
truthful.

## Issues and Discussions

- **Settings → General → Features**: keep **Issues** enabled.
- Enable **Discussions** to activate the "Questions and discussion" link in the
  issue chooser (see `.github/ISSUE_TEMPLATE/config.yml`). Create at least a
  "Q&A" and an "Ideas" category.

## Private vulnerability reporting

- **Settings → Code security → Private vulnerability reporting**: **Enable**.
- This activates the private report route referenced by
  [`SECURITY.md`](../../SECURITY.md) and the Code of Conduct enforcement route.

## Secret scanning and push protection

- **Settings → Code security**: enable **Secret scanning** and **Push
  protection** where available for the account plan.

## Code scanning (CodeQL)

- **Settings → Code security → Code scanning**: add **CodeQL analysis** using
  **Default setup**. Default setup is preferred here over a committed workflow to
  reduce maintenance. If advanced (file-based) setup becomes necessary, add a
  workflow with actions pinned to commit SHAs and least-privilege permissions.

## Branch protection / ruleset for `main`

Create a ruleset (**Settings → Rules → Rulesets**) or a classic branch
protection rule targeting `main`:

- Require a pull request before merging.
- Require status checks to pass, selecting these checks (from the Quality
  workflow):
  - `quality (py3.12)`
  - `quality (py3.13)`
  - `quality (py3.14)`
- Require branches to be up to date before merging.
- Require conversation resolution before merging.
- Block force pushes and deletions.
- Require linear history (matches the squash-merge strategy below).

Require approvals once there is more than one maintainer.

## Merge strategy

**Settings → General → Pull Requests**:

- Enable **Squash merging**; disable merge commits and rebase merging to keep a
  linear history.
- Enable **Automatically delete head branches**.

## Labels

Create the labels listed in [`labels.md`](labels.md). They are referenced by the
issue templates and release-note configuration.

## Social preview

**Settings → General → Social preview**: upload
[`assets/brand/social-preview.png`](../../assets/brand/social-preview.png)
(1280×640, under GitHub's size limit). To regenerate it, see
[brand guidelines](../brand-guidelines.md).
