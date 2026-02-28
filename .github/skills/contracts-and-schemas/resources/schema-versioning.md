# Schema versioning guidance
- Backward compatible in v1:
  - Add optional fields
  - Add new message types/topics
- Breaking (requires v2):
  - Remove/rename fields
  - Change types
  - Change semantic meaning
Migration pattern:
- Run v1 and v2 in parallel
- Add a translator consumer if needed
- Deprecate with a documented window