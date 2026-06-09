# Scenario 01: JWT Expiry Mismatch

**Difficulty:** Medium  
**Starting branch:** `scenario/01-jwt-expiry`  
**Zone:** production

## User prompt

> Users are getting logged out unexpectedly after about 30 minutes, but the API is configured for 60-minute sessions. Find and fix the JWT/session TTL mismatch between the backend and frontend.

## Files the agent should touch

- `apps/web/src/config/session.ts` (incorrect client-side TTL)
- `apps/api/meridian_api/config.py` or `.env.example` (reference for correct value)
- Possibly `apps/web/src/context/AuthContext.tsx` (wire up session config)

## Acceptance criteria

- [ ] Client-side session/TTL constant matches API `jwt_expire_minutes` (60)
- [ ] No hardcoded `30` minute TTL remains in web session config
- [ ] Web tests still pass: `cd apps/web && npm test -- --run`
- [ ] API tests still pass: `make api-test` (with Postgres running)

## Verification

```bash
git checkout scenario/01-jwt-expiry
# after agent fix:
grep -r "30" apps/web/src/config/session.ts  # should not show TTL=30
make api-test
```

## Common failure modes

- Changes API TTL to 30 instead of fixing the frontend
- Edits `apps/api/meridian_api/auth.py` token creation without checking web config
- Adds complex refresh-token machinery instead of aligning constants
- Never finds `apps/web/src/config/session.ts` (only exists on scenario branch)