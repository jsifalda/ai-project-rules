#!/usr/bin/env node

// sync-skills.js — SessionStart hook that auto-syncs Claude Code skills.
// Scans the source directory(ies) given as CLI args for skill folders (each
// containing SKILL.md) and creates directory symlinks in ${CLAUDE_CONFIG_DIR:-~/.claude}/skills/.
// It also links *.md files from each source's sibling agents/ folder into .../agents/.
//
// Usage:
//   node sync-skills.js <skills-dir> [<skills-dir> ...]
//
// The source folder is configured by the setup-skills-autorefresh installer,
// which bakes it into the SessionStart hook command in ${CLAUDE_CONFIG_DIR:-~/.claude}/settings.json.
// To change the synced folder, re-run that installer with a different path.
//
// Filtering: edit WHITELIST / BLACKLIST below to include/exclude specific skills.
//
// Copilot CLI counterpart: ~/.copilot/hooks/sync-skills.js (separate, copy-based)
// — keep WHITELIST / BLACKLIST in sync between the two when filters change.

const fs = require('fs');
const path = require('path');
const os = require('os');

const envConfigDir = process.env.CLAUDE_CONFIG_DIR;
const CONFIG_BASE =
  envConfigDir && path.isAbsolute(envConfigDir) ? envConfigDir : path.join(os.homedir(), '.claude');
const SKILLS_DIR = path.join(CONFIG_BASE, 'skills');
const COMMANDS_DIR = path.join(CONFIG_BASE, 'commands');
const AGENTS_DIR = path.join(CONFIG_BASE, 'agents');

if (envConfigDir && !path.isAbsolute(envConfigDir)) {
  console.error(
    `[sync-skills] WARNING: CLAUDE_CONFIG_DIR is not absolute (${envConfigDir}), using ${CONFIG_BASE}`
  );
}

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
      if (SOURCES.some((s) => target === s || target.startsWith(s + path.sep))) {
        fs.unlinkSync(fullPath);
        migrated++;
      }
    } catch {
      // Not a symlink, leave alone
    }
  }
  if (migrated > 0) {
    console.log(
      `[sync-skills] Migrated: removed ${migrated} legacy symlinks from ${COMMANDS_DIR}/`
    );
  }
}

// Links regular *.md files from each source's sibling agents/ folder into
// ${CONFIG_BASE}/agents/. Same rules as skills: first source wins, unmanaged entries are never touched.
function syncAgents() {
  const agentMap = new Map(); // file name -> source file path
  const roots = [];
  for (const source of SOURCES) {
    const dir = path.join(path.dirname(source), 'agents');
    roots.push(dir + path.sep); // Kept even when the folder is gone, so its stale links get pruned
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
      roots.push(fs.realpathSync(dir) + path.sep);
    } catch {
      continue; // No agents folder next to this source
    }
    for (const entry of entries) {
      if (!entry.isFile() || entry.name.startsWith('.') || !entry.name.endsWith('.md')) continue;
      const filePath = path.join(dir, entry.name);
      if (agentMap.has(entry.name)) {
        console.error(
          `[sync-skills] CONFLICT: agent "${entry.name}" exists in both sources. Using: ${agentMap.get(entry.name)} (skipping: ${filePath})`
        );
      } else {
        agentMap.set(entry.name, filePath);
      }
    }
  }

  // Remove stale managed symlinks (source file gone or now provided by another source)
  if (fs.existsSync(AGENTS_DIR)) {
    for (const entry of fs.readdirSync(AGENTS_DIR)) {
      const fullPath = path.join(AGENTS_DIR, entry);
      try {
        const target = fs.readlinkSync(fullPath);
        const resolved = path.isAbsolute(target) ? target : path.resolve(AGENTS_DIR, target);
        if (!roots.some((r) => resolved.startsWith(r))) continue;
        if (agentMap.get(entry) !== resolved) fs.unlinkSync(fullPath);
      } catch {
        // Not a symlink, leave alone
      }
    }
  }

  if (agentMap.size === 0) return 0;
  fs.mkdirSync(AGENTS_DIR, { recursive: true });

  for (const [name, sourcePath] of agentMap) {
    const linkPath = path.join(AGENTS_DIR, name);
    try {
      let linkStat = null;
      try {
        linkStat = fs.lstatSync(linkPath); // lstat, so a dangling symlink still counts as present
      } catch {} // Nothing at that path
      if (linkStat) {
        if (!linkStat.isSymbolicLink()) {
          console.error(`[sync-skills] WARNING: ${linkPath} exists but is not a symlink, skipping`);
          continue;
        }
        const current = fs.readlinkSync(linkPath);
        if (current === sourcePath) continue;
        const resolved = path.isAbsolute(current) ? current : path.resolve(AGENTS_DIR, current);
        if (!roots.some((r) => resolved.startsWith(r))) {
          console.error(`[sync-skills] WARNING: ${linkPath} is an unmanaged symlink, skipping`);
          continue;
        }
        fs.unlinkSync(linkPath);
      }
      fs.symlinkSync(sourcePath, linkPath);
    } catch (err) {
      console.error(`[sync-skills] WARNING: failed to link agent ${name}: ${err.message}`);
    }
  }
  return agentMap.size;
}

function syncSkills() {
  // Ensure the skills dir exists
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
  let failed = 0;

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

    // One bad entry must never abort the run. Without this, a throw escapes to the
    // top-level catch and every remaining skill is left unlinked.
    try {
      // lstat, NOT existsSync. existsSync follows the link, so it reports false for a
      // dangling symlink while the name still occupies the directory entry — and then
      // symlinkSync below throws EEXIST. Do not simplify this back to existsSync.
      let linkStat = null;
      try {
        linkStat = fs.lstatSync(linkPath);
      } catch {
        // Nothing at that path. This is the normal case for a new skill.
      }

      if (linkStat) {
        if (!linkStat.isSymbolicLink()) {
          console.error(
            `[sync-skills] WARNING: ${linkPath} exists but is not a symlink, skipping`
          );
          continue;
        }

        // The entry is a symlink, so a failure below is a real I/O problem. Let it reach
        // the outer catch, which counts it. Do not swallow it as a "not a symlink" case.
        if (fs.readlinkSync(linkPath) === sourcePath) {
          unchanged++;
          continue;
        }
        fs.unlinkSync(linkPath);
      }

      fs.symlinkSync(sourcePath, linkPath);
      created++;
    } catch (err) {
      console.error(`[sync-skills] WARNING: failed to link ${name}: ${err.message}`);
      failed++;
    }
  }

  let agents = 0;
  try {
    agents = syncAgents();
  } catch (err) {
    console.error(`[sync-skills] WARNING: agent sync failed: ${err.message}`);
  }
  const total = skillMap.size;
  const failedNote = failed > 0 ? `, ${failed} failed` : '';
  console.log(
    `[sync-skills] Synced ${total} skills (${created} new, ${removed} removed, ${unchanged} unchanged, ${conflicts.length} conflicts${failedNote}), ${agents} agents`
  );
}

try {
  migrateLegacyCommands();
  syncSkills();
} catch (err) {
  console.error(`[sync-skills] Error: ${err.message}`);
}
