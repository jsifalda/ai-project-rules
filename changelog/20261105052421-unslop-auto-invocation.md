# Let unslop auto-trigger

- Removed the restricted invocation from `unslop`: no RESTRICTED-INVOCATION description, no Invocation section.
- Why: cutting AI tells is a safe, read-and-edit task with no outward effect, so a description match is enough to load it.
- The description now names its triggers and keeps the pointers to `write-like-human` and `rewrite`.
