# PRD-21225 · Code review

## Round 1 · 2026-10-30 · reviewed dev/PRD-21225 @ c3c6790 (base master @ fce33b1)

Status: frozen @ c3c6790057e2d1544fca2d5f5e5dadb8c42d276e1

Verdict: approved

### Scope

Diff `origin/master...c3c6790` (base = default branch `master` @ `fce33b17`, unchanged since the dev worktree
was created, confirmed via `git fetch origin master`). Files touched: `src/duo_mcp/tools/logs.py` (new),
`src/duo_mcp/server.py` (2-line registration + instructions sentence), `README.md` (scope/tool-table/known-gaps
updates), `tests/test_tools.py` (2-line dict updates), `docs/tickets/PRD-21225.md`, `docs/tickets/PRD-21225.ac.json`.

### Findings

None. No must-fix, no suggestion.

### Verification performed

- `uv sync && uv run pytest -v` on commit `c3494b9` (the tested commit; `c3c6790` only adds docs on top):
  16 passed, 0 failed — matches the Self-test table in `docs/tickets/PRD-21225.md`.
- Read `src/duo_mcp/tools/logs.py` against `src/duo_mcp/tools/groups.py` (the pattern it claims to copy):
  identical shape — `client_factory()` / `NO_TOKEN` guard / `ToolAnnotations(readOnlyHint=True)` /
  `dump_json_capped()` / `except DuoError as e: return e.to_envelope()`. No deviation.
- Read `api_client.py`'s `request()` and `_canon_params()`: confirmed `None`-valued params (e.g. `mintime`
  omitted by the caller) are filtered out of both the signed query string and the HMAC canonical string
  (`clean_params = {k: v for k, v in (params or {}).items() if v is not None}`, `_canon_params` has the same
  `if value is None: continue` guard) — same as `groups.py`'s `limit`/`offset`, which also default to `None`.
  No malformed `mintime=None` query string risk.
- Read `_parse()`: unwraps Duo's `{"stat": ..., "response": ...}` envelope generically — the new endpoint gets
  the same unwrapping as every other tool, no endpoint-specific handling needed or added.
- `grep -rnP '[\x{4e00}-\x{9fff}]' --exclude-dir=.git --exclude-dir=.venv .` on the worktree: no matches.
- `diff` of `README.md`'s `## MSPbots Connector` section (lines 9-79) against
  `~/.claude/skills/vendor-mcp-development/reference/readme-connector-section.md`: byte-identical, confirming
  the Self-test's "untouched by this change" claim.
- `git diff origin/master...HEAD -- src/ tests/ README.md`: read in full. Change is exactly what the tech
  design's Change list specifies — one new tool file, a 2-line `server.py` registration diff, a 2-line test-dict
  update, README additions. No scope creep (none of the other 14 removed categories or 5 other log variants were
  re-added), no unrelated files touched.
- Credential handling: `logs.py` reads credentials only via `client_factory()` (contextvar-backed, per-request),
  same as every other tool — no new credential path introduced, SOP's three ironclad rules unaffected.
- SOP §14 checklist: no item is newly violated by this diff. The pre-existing tool count (29 > 20, a "should"
  item under §14 "面向 Agent 设计") already exceeded 20 before this change (28 tools on `master`) — not
  introduced by this ticket, not a regression, not scored here.

### Conclusion

Change matches the tech design exactly (chosen Option A, no deviation), reuses all existing infrastructure,
introduces no new dependency, and is covered by the existing structural snapshot test plus the two
tool-agnostic suites (middleware header-gating, error-envelope mapping). TC2/TC3 remain untested pending a real
Duo account, which is a documented non-blocker per `mcp-track.md` §2.5/§3. Approved; proceeding to merge into
`master`, publish to INT, and check the connector wiki.
