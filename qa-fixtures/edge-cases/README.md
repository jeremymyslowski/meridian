# Edge Cases

Tricky repo layouts and file types that confuse agent navigation.

## Sub-zones

| Path | Challenge |
|------|-----------|
| `circular/` | Mutual imports between `module_a` and `module_b` |
| `nested/deep/path/to/config/` | 6-level deep directory for a tiny config file |
| `unicode_dir/team_name_validator.py` | Directory named `unicode_dir` hints at i18n; easy to grep wrong path |
| `generated/fake_openapi_client.py` | File with `GENERATED CODE` header agents should not hand-edit |

## Expected agent behavior

- Read README before editing generated files
- Break circular imports by extracting shared types to `shared_types.py`
- Find `nested/.../team_defaults.json` via search, not manual tree walking

## Sample prompts

**Validator:** Update `unicode_dir/team_name_validator.py` to reject empty team names.

**Circular:** Fix the circular import between module_a and module_b so both can be imported.

**Generated:** Add a `create_project` method to the API client — regenerate from OpenAPI, do not hand-edit `fake_openapi_client.py`.