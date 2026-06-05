#!/usr/bin/env node

// sync-skills.js — SessionStart hook that auto-syncs Claude Code skills.
// Scans the source directory(ies) given as CLI args for skill folders (each
// containing SKILL.md) and creates directory symlinks in ~/.claude/skills/.
//
// Usage:
//   node sync-skills.js <skills-dir> [<skills-dir> ...]
//
// The source folder is configured by the setup-skills-autorefresh installer,
// which bakes it into the SessionStart hook command in ~/.claude/settings.json.
// To change the synced folder, re-run that installer with a different path.
//
// Filtering: edit WHITELIST / BLACKLIST below to include/exclude specific skills.
//
// Copilot CLI counterpart: ~/.copilot/hooks/sync-skills.js (separate, copy-based)
// — keep WHITELIST / BLACKLIST in sync between the two when filters change.

const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILLS_DIR = path.join(os.homedir(), '.claude', 'skills');
const COMMANDS_DIR = path.join(os.homedir(), '.claude', 'commands');

// Source directory(ies) — passed as CLI args by the registered hook command.
// Resolved to absolute paths so the created symlinks always have stable targets.
const SOURCES = process.argv.slice(2).map((p) => path.resolve(p));

if (SOURCES.length === 0) {
  console.error(
    '[sync-skills] No source directory provided. Re-run the setup-skills-autorefresh installer to register a skills folder.'
  );
  process.exit(0);
}

// Filter skills by name (exact match, no globs).
// - WHITELIST: if non-empty, ONLY these skills are synced (BLACKLIST ignored).
// - BLACKLIST: skills to skip. Only consulted when WHITELIST is empty.
// Leave both as [] to sync everything (default).
const WHITELIST = [];
const BLACKLIST = [
  'ai-testing-agents',
  'postman-test-generator',
  'testrail-delete-test-runs',
  'weekly-sprint-update',
];

function migrateLegacyCommands() {
  if (!fs.existsSync(COMMANDS_DIR)) return;

  let migrated = 0;
  for (const entry of fs.readdirSync(COMMANDS_DIR)) {
    const fullPath = path.join(COMMANDS_DIR, entry);
    try {
      const target = fs.readlinkSync(fullPath);
      if (SOURCES.some((s) => target.startsWith(s))) {
        fs.unlinkSync(fullPath);
        migrated++;
      }
    } catch {
      // Not a symlink, leave alone
    }
  }
  if (migrated > 0) {
    console.log(
      `[sync-skills] Migrated: removed ${migrated} legacy symlinks from ~/.claude/commands/`
    );
  }
}

function syncSkills() {
  // Ensure ~/.claude/skills/ exists
  if (!fs.existsSync(SKILLS_DIR)) {
    fs.mkdirSync(SKILLS_DIR, { recursive: true });
  }

  // Collect all skills from sources (priority order)
  const skillMap = new Map(); // name -> source path
  const conflicts = [];

  for (const source of SOURCES) {
    if (!fs.existsSync(source)) {
      console.error(`[sync-skills] WARNING: source not found, skipping: ${source}`);
      continue;
    }

    const entries = fs.readdirSync(source, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      if (entry.name.startsWith('.')) continue;

      const skillPath = path.join(source, entry.name);
      const skillMd = path.join(skillPath, 'SKILL.md');

      if (!fs.existsSync(skillMd)) continue;

      if (WHITELIST.length > 0) {
        if (!WHITELIST.includes(entry.name)) continue;
      } else if (BLACKLIST.includes(entry.name)) {
        continue;
      }

      if (skillMap.has(entry.name)) {
        conflicts.push({
          name: entry.name,
          winner: skillMap.get(entry.name),
          loser: skillPath,
        });
      } else {
        skillMap.set(entry.name, skillPath);
      }
    }
  }

  for (const c of conflicts) {
    console.error(
      `[sync-skills] CONFLICT: "${c.name}" exists in both sources. Using: ${c.winner} (skipping: ${c.loser})`
    );
  }

  // Determine source roots for ownership check
  const sourceRoots = SOURCES.filter((s) => fs.existsSync(s)).map(
    (s) => fs.realpathSync(s) + path.sep
  );
  const isManaged = (target) => sourceRoots.some((root) => target.startsWith(root));

  let created = 0;
  let removed = 0;
  let unchanged = 0;

  // Remove stale managed symlinks
  for (const entry of fs.readdirSync(SKILLS_DIR)) {
    const fullPath = path.join(SKILLS_DIR, entry);
    try {
      const target = fs.readlinkSync(fullPath);
      const resolvedTarget = path.isAbsolute(target)
        ? target
        : path.resolve(SKILLS_DIR, target);

      if (!isManaged(resolvedTarget)) continue;

      if (!skillMap.has(entry) || skillMap.get(entry) !== resolvedTarget) {
        fs.unlinkSync(fullPath);
        removed++;
      }
    } catch {
      // Not a symlink, leave alone
    }
  }

  // Create/update symlinks
  for (const [name, sourcePath] of skillMap) {
    const linkPath = path.join(SKILLS_DIR, name);

    if (fs.existsSync(linkPath)) {
      try {
        const currentTarget = fs.readlinkSync(linkPath);
        if (currentTarget === sourcePath) {
          unchanged++;
          continue;
        }
        fs.unlinkSync(linkPath);
      } catch {
        console.error(
          `[sync-skills] WARNING: ${linkPath} exists but is not a symlink, skipping`
        );
        continue;
      }
    }

    fs.symlinkSync(sourcePath, linkPath);
    created++;
  }

  const total = skillMap.size;
  console.log(
    `[sync-skills] Synced ${total} skills (${created} new, ${removed} removed, ${unchanged} unchanged, ${conflicts.length} conflicts)`
  );
}

try {
  migrateLegacyCommands();
  syncSkills();
} catch (err) {
  console.error(`[sync-skills] Error: ${err.message}`);
}
