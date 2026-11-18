# Source-of-truth rule covers absence and host paths

- `general.md`: the source-of-truth rule now also covers an absence question, such as "is there a schedule for X?". An agent said a schedule did not exist because it read a path from an instruction file and did not read the live config.
- `authoring.md`: the hardcode ban now also covers a host path, in any shared instruction file. The bad schedules path got in because the rule named only repo names, slugs and people.
- Both files keep their old size.
