# Dify DM Adaptation Context

## Goal
Adapt Dify backend to support Dameng Database (DM / 达梦数据库).

## Current branch
dm-adaptation

## Current milestones / tags
- dm-orm-pass
- dm-migration-pass
- dm-api-pass
- dm-console-core-pass
- dm-api-key-pass

## Completed work
1. DM database URI generation supported.
2. Alembic implementation registered for DM.
3. Alembic alter column support added for DM.
4. ORM layer adapted for DM.
5. Migration tests passed enough to tag dm-migration-pass.
6. API startup and core backend routes adapted.
7. Console core JSON field issues adapted.
8. API key delete route ID normalization fixed.
9. API token lookup adjusted to avoid unsupported exists expression on DM.

## Important commits
- e29bddb feat(dm): handle dm database uri generation
- be8e0aa feat(dm): register alembic implementation for dm
- 914621d feat(dm): support alembic alter column for dm
- 71a3e9a fix: adapt tenant plugin auto-upgrade JSON fields for DM
- 3f54a4e fix: avoid exists expression for api token lookup on DM
- f4f750b fix: normalize api key delete route ids for DM

## Known environment
- OS: WSL / Windows mixed environment
- Project path:
  ~/projects/dify-dm
- API path:
  ~/projects/dify-dm/api
- Database: Dameng DM
- Python dependency manager: uv
- Current branch:
  dm-adaptation

## Testing status
Passed / partially passed:
- DM connection
- SQLAlchemy basic binary field tests
- ORM adaptation
- Migration adaptation
- API startup
- Console core flow
- API key related flow

Still likely remaining:
- Full backend regression
- Plugin system edge cases
- Workflow / dataset / file upload flows
- Celery / worker / sandbox related flows
- Full frontend-console manual verification
- Long-term strategy for rebasing against upstream Dify

## Development strategy
Keep official Dify as upstream.
Keep DM adaptation isolated in dm-adaptation branch.
Use small commits and milestone tags after each validated layer.

When Dify updates:
1. git fetch upstream
2. git checkout dm-adaptation
3. git rebase upstream/main
4. resolve conflicts
5. rerun DM regression tests
