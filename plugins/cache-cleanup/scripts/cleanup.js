#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");

const CACHE_DIR = path.join(os.homedir(), ".claude", "plugins", "cache");

function parseSemver(version) {
  const match = version.match(/^(\d+)\.(\d+)\.(\d+)/);
  if (!match) return null;
  return [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
}

function compareSemver(a, b) {
  for (let i = 0; i < 3; i++) {
    if (a[i] !== b[i]) return a[i] - b[i];
  }
  return 0;
}

function getDirSize(dirPath) {
  let size = 0;
  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dirPath, entry.name);
      if (entry.isDirectory()) {
        size += getDirSize(full);
      } else {
        try {
          size += fs.statSync(full).size;
        } catch {}
      }
    }
  } catch {}
  return size;
}

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

function scan() {
  const results = { plugins: [], tempDirs: [] };

  if (!fs.existsSync(CACHE_DIR)) {
    return results;
  }

  const marketplaces = fs.readdirSync(CACHE_DIR, { withFileTypes: true });

  for (const mp of marketplaces) {
    if (!mp.isDirectory()) continue;
    const mpPath = path.join(CACHE_DIR, mp.name);

    // Flag orphaned temp directories at marketplace level
    if (mp.name.startsWith("temp_local_")) {
      const size = getDirSize(mpPath);
      results.tempDirs.push({ path: mpPath, name: mp.name, size });
      continue;
    }

    const plugins = fs.readdirSync(mpPath, { withFileTypes: true });

    for (const plugin of plugins) {
      if (!plugin.isDirectory()) continue;

      // Flag temp dirs inside marketplaces too
      if (plugin.name.startsWith("temp_local_")) {
        const fullPath = path.join(mpPath, plugin.name);
        const size = getDirSize(fullPath);
        results.tempDirs.push({ path: fullPath, name: plugin.name, size });
        continue;
      }

      const pluginPath = path.join(mpPath, plugin.name);
      const versions = fs.readdirSync(pluginPath, { withFileTypes: true })
        .filter((d) => d.isDirectory())
        .map((d) => ({
          name: d.name,
          semver: parseSemver(d.name),
          path: path.join(pluginPath, d.name),
        }));

      if (versions.length <= 1) continue;

      // Sort: semver versions first (ascending), non-semver last
      const semverVersions = versions.filter((v) => v.semver !== null);
      const nonSemver = versions.filter((v) => v.semver === null);

      semverVersions.sort((a, b) => compareSemver(a.semver, b.semver));

      // Keep the latest semver version, mark everything else for removal
      const latest = semverVersions.length > 0
        ? semverVersions[semverVersions.length - 1]
        : versions[versions.length - 1];

      const toRemove = versions.filter((v) => v !== latest);

      if (toRemove.length === 0) continue;

      const removeSizes = toRemove.map((v) => ({
        ...v,
        size: getDirSize(v.path),
      }));

      results.plugins.push({
        marketplace: mp.name,
        plugin: plugin.name,
        keep: latest.name,
        remove: removeSizes,
        totalFree: removeSizes.reduce((sum, v) => sum + v.size, 0),
      });
    }
  }

  return results;
}

function printReport(results, deleted) {
  const action = deleted ? "Deleted" : "Would delete";
  let totalFreed = 0;

  if (results.plugins.length === 0 && results.tempDirs.length === 0) {
    console.log("Cache is clean — no old versions to remove.");
    return;
  }

  for (const p of results.plugins) {
    console.log(`\n${p.marketplace}/${p.plugin} (keeping ${p.keep}):`);
    for (const v of p.remove) {
      console.log(`  ${action}: ${v.name} (${formatBytes(v.size)})`);
      totalFreed += v.size;
    }
  }

  for (const t of results.tempDirs) {
    console.log(`\n${action} temp directory: ${t.name} (${formatBytes(t.size)})`);
    totalFreed += t.size;
  }

  console.log(`\nTotal: ${action.toLowerCase()} ${results.plugins.reduce((n, p) => n + p.remove.length, 0) + results.tempDirs.length} directories, ${formatBytes(totalFreed)} freed.`);
}

function deleteOld(results) {
  for (const p of results.plugins) {
    for (const v of p.remove) {
      fs.rmSync(v.path, { recursive: true, force: true });
    }
  }
  for (const t of results.tempDirs) {
    fs.rmSync(t.path, { recursive: true, force: true });
  }
}

// --- Main ---
const args = process.argv.slice(2);
const doDelete = args.includes("--delete");

const results = scan();

if (doDelete) {
  if (results.plugins.length === 0 && results.tempDirs.length === 0) {
    console.log("Cache is clean — nothing to delete.");
    process.exit(0);
  }
  deleteOld(results);
  printReport(results, true);
} else {
  printReport(results, false);
}
