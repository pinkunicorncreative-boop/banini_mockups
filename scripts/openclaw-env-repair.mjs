#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const HOME = os.homedir();
const envPath = path.join(HOME, '.openclaw', '.env');
const backupDir = path.join(HOME, '.openclaw', 'backups', 'config-guard');
fs.mkdirSync(backupDir, { recursive: true });
const stamp = new Date().toISOString().replace(/[:.]/g, '-');

const ORDER = [
  'GEMINI_API_KEY',
  'OPENCLAW_GATEWAY_TOKEN',
  'NANO_BANANA_PRO_API_KEY',
  'NOTION_API_KEY',
  'OPENAI_API_KEY',
  'ELEVENLABS_API_KEY',
  'GUMLOOP_API_KEY'
];
const DEFAULTS = Object.fromEntries(ORDER.map((k) => [k, '']));

function parseEnv(text) {
  const out = {};
  for (const line of text.split(/\r?\n/)) {
    if (!line || /^\s*#/.test(line)) continue;
    const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$/);
    if (!m) continue;
    let value = m[2] ?? '';
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) value = value.slice(1, -1);
    out[m[1]] = value;
  }
  return out;
}

const current = fs.existsSync(envPath) ? parseEnv(fs.readFileSync(envPath, 'utf8')) : {};
if (fs.existsSync(envPath)) {
  fs.copyFileSync(envPath, path.join(backupDir, `${stamp}-pre-repair-.env`));
}
const merged = { ...DEFAULTS, ...current };
const lines = [
  '# OpenClaw config guard managed env skeleton',
  '# Required: GEMINI_API_KEY, OPENCLAW_GATEWAY_TOKEN',
  '# Optional integrations can stay blank if unused',
  ...ORDER.map((key) => `${key}=${merged[key] ?? ''}`)
];
fs.writeFileSync(envPath + '.tmp', lines.join('\n') + '\n');
fs.renameSync(envPath + '.tmp', envPath);
console.log(`Rewrote ${envPath} with canonical key order and preserved values.`);
