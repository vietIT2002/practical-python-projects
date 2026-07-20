# Maintainer notes: assumptions and open decisions

This document records the assumptions behind the repository's current setup, the
conservative defaults chosen where a decision was reversible, and the items that
still need a maintainer decision before specific milestones. It is aimed at
maintainers, not end users.

## Confirmed identity

- Owner: `vietIT2002` (personal account).
- Repository: <https://github.com/vietIT2002/practical-python-projects> (public).
- Default branch: `main`.
- License: MIT.

## Defaults chosen (reversible)

These were selected to keep progress moving and can be changed before launch:

- GitHub Discussions: enabled.
- Documentation website: deferred; to be revisited near the first stable release.
- Sponsorship links: none.
- Python support: minimum 3.12; continuous integration targets 3.12–3.14 as the
  dependency ecosystem allows.

## Open decisions (needed before launch)

These concern public contact details and are intentionally left unset until the
maintainer confirms them, since they cannot be guessed:

| Item | Needed for | Status |
|---|---|---|
| Public contact email | Community and branding files | Pending |
| Security reporting address | `SECURITY.md` | Pending |
| Code of Conduct enforcement contact | `CODE_OF_CONDUCT.md` | Pending |

Foundation and tooling work does not depend on these and can proceed.

## Actions that require GitHub access

The following are configured through the GitHub interface or an authenticated
API, not by editing files in the repository. They are listed here so they are
not overlooked:

- Repository topics.
- Social preview image.
- Branch protection / rulesets and required status checks.
- Enabling GitHub Discussions.
- Environments and secrets.
- Publishing releases.

## Conventions

- Commits use concise, conventional messages and leave the repository in a
  valid state.
- Secrets, credentials, and personal environment files are never committed; use
  environment variables and `.env.example` placeholders instead.
- Commit author email is visible in a public repository; contributors who prefer
  privacy can configure a no-reply address before contributing.
