#!/usr/bin/env node
"use strict";

// Vendors the writer-style skill (self-contained: skill + agents + commands) into a
// project's ./.claude/ so Claude Code discovers it. Node core only — no dependencies.
// Runs automatically on `npm install @stbr/writer-style-skill`, or on demand via
// `npx @stbr/writer-style-skill`. For an all-projects install, use the Claude Code
// plugin instead (see README → Installation).

const fs = require("fs");
const path = require("path");

const PKG_ROOT = path.resolve(__dirname, "..");
// The skill is self-contained (profiles/, tools/, rules/ live under skills/writer-style/);
// agents/ and commands/ are the only sibling components.
const COMPONENTS = ["skills", "agents", "commands"];
const SKIP = new Set([".DS_Store", "__pycache__", ".pytest_cache"]);

function copyRecursive(src, dst) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dst, { recursive: true });
    for (const name of fs.readdirSync(src)) {
      if (SKIP.has(name) || name.endsWith(".pyc")) continue;
      copyRecursive(path.join(src, name), path.join(dst, name));
    }
  } else {
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.copyFileSync(src, dst);
  }
}

function main() {
  const projectRoot = process.env.INIT_CWD || process.cwd();
  const claudeDir = path.join(projectRoot, ".claude");

  // Don't vendor into our own repo during a local/dev install of this package.
  if (path.resolve(claudeDir, "..") === PKG_ROOT) {
    console.log("[writer-style] dev install detected — skipping vendor step.");
    console.log(
      "[writer-style] run `npx @stbr/writer-style-skill` inside a project to install it there.",
    );
    return;
  }

  const copied = [];
  for (const comp of COMPONENTS) {
    const src = path.join(PKG_ROOT, comp);
    if (!fs.existsSync(src)) continue;
    copyRecursive(src, path.join(claudeDir, comp));
    copied.push(comp);
  }

  if (!copied.length) {
    console.log(
      "[writer-style] nothing to install (package payload not found).",
    );
    return;
  }

  console.log(`[writer-style] installed into ${claudeDir}/`);
  console.log(`[writer-style]   components: ${copied.join(", ")}`);
  console.log(
    "[writer-style]   skill:    .claude/skills/writer-style/SKILL.md",
  );
  console.log(
    "[writer-style]   commands: /write-in-voice  /validate-voice  /new-persona  /profile-corpus",
  );
  console.log(
    "[writer-style] note: this is a per-project install. For every project, use the Claude Code plugin",
  );
  console.log(
    "[writer-style]       (claude plugin marketplace add solanabr/writer-style-skill).",
  );
  try {
    require("child_process").execSync("python3 --version", { stdio: "ignore" });
    console.log("[writer-style] python3 found — Pass-C validator ready.");
  } catch {
    console.log(
      "[writer-style] WARNING: python3 not found. Install Python 3 (stdlib only) to run the",
    );
    console.log(
      "[writer-style]          validator at .claude/skills/writer-style/tools/validate_voice.py.",
    );
  }
}

try {
  main();
} catch (err) {
  // Never fail the npm install over the vendor step.
  console.error(
    "[writer-style] install step skipped:",
    err && err.message ? err.message : err,
  );
}
process.exit(0);
