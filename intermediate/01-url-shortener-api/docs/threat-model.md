# Threat model

This is a teaching example. It demonstrates good structure and safe defaults,
but it is **not** a hardened production service. This document is honest about
what it does and does not protect against.

## Assets

- The mapping of short codes to destination URLs.
- Click counts.
- Availability of the redirect endpoint.

## Trust boundaries

- The HTTP API is the boundary between untrusted clients and the database.
- The database is trusted local storage (SQLite by default).

## Threats and current handling

| Threat | Handling in this example |
|---|---|
| **Malicious destination URLs** | URLs are validated to be `http`/`https` and well-formed. The service **never fetches** destinations. It does **not** and cannot vouch that a destination is safe — a valid URL can still be malicious. |
| **Redirect abuse (open redirect)** | This service is intentionally an open redirector: anyone can create a link to any URL. That is its purpose, so it must not be exposed as a trusted-domain redirect. |
| **Alias enumeration** | Generated codes use a cryptographically strong random source (`secrets`), so codes are not guessable in sequence. Custom aliases are, by nature, guessable. |
| **Click-count inflation** | Counts increment on every redirect with no deduplication; they are approximate and trivially inflated. Do not treat them as analytics. |
| **Injection** | All database access uses parameterised SQLAlchemy operations. |
| **Reserved-path collisions** | Aliases that would shadow API routes (`docs`, `redoc`, `health`) are rejected. |

## Not provided by this example

- **Rate limiting.** There is none. A real deployment needs it (e.g. at a
  reverse proxy or API gateway).
- **Authentication and authorization.** Anyone can create and read links. There
  are no accounts, ownership, or per-user limits.
- **Abuse/malware screening** of destination URLs.
- **HTTPS termination.** Run behind a trusted reverse proxy that terminates TLS
  and sets forwarding headers.

## Deployment note

Deploy behind a trusted proxy, enable rate limiting and request-size limits
there, and add authentication before allowing untrusted users to create links.
