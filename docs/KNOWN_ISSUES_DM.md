# Known Issues and Compatibility Notes for DM

## 1. Binary Type Handling

Dify-style binary wrapper previously caused compiler dispatch issues with DM.

Observed issue:

`'_DMBinary' object has no attribute '_compiler_dispatch'`

Working direction:

Use direct binary-compatible SQLAlchemy type handling where possible.

## 2. Alembic Compatibility

Default Alembic behavior was not sufficient for DM.

Adaptations added:

- DM Alembic implementation registration
- DM-specific alter column support

Related milestones:

- `dm-orm-pass`
- `dm-migration-pass`

## 3. JSON Field Compatibility

Some console core paths involved JSON field behavior that required DM-specific adaptation.

Known affected area:

- tenant plugin auto-upgrade

Related commit:

- `71a3e9a fix: adapt tenant plugin auto-upgrade JSON fields for DM`

## 4. EXISTS Expression Compatibility

Some SQL expression patterns involving `exists` were incompatible or unreliable with DM.

Known affected area:

- API token lookup

Resolution:

Avoid unsupported `exists` expression pattern for API token lookup.

Related commit:

- `3f54a4e fix: avoid exists expression for api token lookup on DM`

## 5. API Key Route ID Normalization

API key delete route required ID normalization for DM compatibility.

Related commit:

- `f4f750b fix: normalize api key delete route ids for DM`

## 6. Remaining Risk Areas

These areas may still contain DM-specific compatibility issues:

- dataset tables
- workflow execution records
- plugin runtime tables
- file upload metadata
- JSON queries
- long text fields
- timestamp behavior
- transaction behavior
- pagination queries
- raw SQL fragments
