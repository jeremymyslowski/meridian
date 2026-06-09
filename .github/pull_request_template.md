## Summary

<!-- What changed and why? -->

## Checklist

- [ ] Tests pass locally (`make ci` or relevant `make *-test`)
- [ ] OpenAPI changes update `packages/api-client` and `contract-manifest.json` (`make codegen-check`)
- [ ] New DB changes are a numbered migration (never edit old migrations)
- [ ] `qa-fixtures/` changes are not imported by `apps/` or `packages/`

## Agent scenario PRs (if applicable)

- [ ] Scenario number: <!-- e.g. 01 -->
- [ ] Only the intended files were changed (no unrelated refactors)
- [ ] Acceptance criteria from `docs/agent-scenarios/` are met
- [ ] Fixture tests or production tests run as documented