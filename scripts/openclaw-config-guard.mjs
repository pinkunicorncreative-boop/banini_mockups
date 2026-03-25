#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';

const HOME = os.homedir();
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const schemaPath = path.join(ROOT, 'config-guard', 'schema.json');
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));

const expandHome = (p) => p.replace(/^~(?=$|\/)/, HOME);
const now = new Date();
const stamp = now.toISOString().replace(/[:.]/g, '-');

const envPath = expandHome(schema.files.env);
const configPath = expandHome(schema.files.config);
const backupDir = expandHome(schema.files.backupDir);
const stateDir = expandHome(schema.files.stateDir);
const requiredJsonFiles = schema.json.requiredFiles.map(expandHome);
const forbiddenValues = new Set((schema.env.forbiddenValues || []).map((v) => String(v).trim().toLowerCase()));

fs.mkdirSync(backupDir, { recursive: true });
fs.mkdirSync(stateDir, { recursive: true });

function parseEnvFile(text) {
  const out = {};
  const lines = text.split(/\r?\n/);
  for (const line of lines) {
    if (!line || /^\s*#/.test(line)) continue;
    const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$/);
    if (!m) continue;
    let value = m[2] ?? '';
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    out[m[1]] = value;
  }
  return out;
}

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function copyIfExists(file, suffix) {
  if (!fs.existsSync(file)) return null;
  const base = path.basename(file);
  const dest = path.join(backupDir, `${stamp}-${suffix}-${base}`);
  fs.copyFileSync(file, dest);
  return dest;
}

function latestBackupFor(baseName, type) {
  if (!fs.existsSync(backupDir)) return null;
  const entries = fs.readdirSync(backupDir)
    .filter((name) => name.endsWith(`-${baseName}`) && name.includes(`-${type}-`))
    .sort();
  return entries.length ? path.join(backupDir, entries[entries.length - 1]) : null;
}

function writeJson(file, value) {
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

function fail(message, report, code = 1) {
  const textPath = path.join(stateDir, 'last-failure.txt');
  const jsonPath = path.join(stateDir, 'last-report.json');
  fs.writeFileSync(textPath, message + '\n');
  writeJson(jsonPath, report);
  process.stderr.write(message + '\n');
  process.exit(code);
}

const report = {
  ok: false,
  timestamp: now.toISOString(),
  envPath,
  configPath,
  backups: {},
  env: { required: [], optional: [], placeholder: [], missing: [] },
  json: { checked: [], broken: [], restored: [] },
  refs: { missing: [], placeholder: [] },
  notes: []
};

// Snapshot current known-good candidates before touching anything.
report.backups.env = copyIfExists(envPath, 'preflight');
report.backups.config = copyIfExists(configPath, 'preflight');

if (!fs.existsSync(envPath)) {
  fail(
    `[openclaw-config-guard] Missing env file: ${envPath}`,
    { ...report, error: 'env_missing' },
    20
  );
}

let envRaw = fs.readFileSync(envPath, 'utf8');
let env = parseEnvFile(envRaw);

for (const key of schema.env.required) {
  const value = (env[key] || '').trim();
  if (!value) report.env.missing.push(key);
  else if (forbiddenValues.has(value.toLowerCase())) report.env.placeholder.push(key);
  else report.env.required.push(key);
}
for (const key of schema.env.optional || []) {
  const value = (env[key] || '').trim();
  if (!value) continue;
  if (forbiddenValues.has(value.toLowerCase())) report.env.placeholder.push(key);
  else report.env.optional.push(key);
}

if (report.env.missing.length || report.env.placeholder.length) {
  const lines = [
    '[openclaw-config-guard] Refusing to start OpenClaw because config secrets are busted.',
    report.env.missing.length ? `Missing required env vars: ${report.env.missing.join(', ')}` : null,
    report.env.placeholder.length ? `Placeholder/fake values detected: ${report.env.placeholder.join(', ')}` : null,
    `Fix ${envPath}, then restart.`
  ].filter(Boolean);
  fail(lines.join('\n'), report, 21);
}

const jsonFiles = [...new Set(requiredJsonFiles.filter((file) => fs.existsSync(file)))];
for (const file of jsonFiles) {
  try {
    JSON.parse(fs.readFileSync(file, 'utf8'));
    report.json.checked.push({ file, sha256: sha256(file) });
  } catch (error) {
    const backup = latestBackupFor(path.basename(file), 'known-good');
    if (backup) {
      fs.copyFileSync(backup, file);
      report.json.restored.push({ file, backup });
      try {
        JSON.parse(fs.readFileSync(file, 'utf8'));
      } catch (restoreError) {
        report.json.broken.push({ file, error: String(restoreError.message || restoreError) });
      }
    } else {
      report.json.broken.push({ file, error: String(error.message || error) });
    }
  }
}

if (report.json.broken.length) {
  const broken = report.json.broken.map((item) => `${item.file}: ${item.error}`).join('\n');
  fail(
    `[openclaw-config-guard] Broken JSON detected and no valid rollback was available.\n${broken}`,
    report,
    22
  );
}

let config;
try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (error) {
  const backup = latestBackupFor(path.basename(configPath), 'known-good');
  if (backup) {
    fs.copyFileSync(backup, configPath);
    report.json.restored.push({ file: configPath, backup });
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  } else {
    fail(
      `[openclaw-config-guard] openclaw.json is invalid and there is no known-good rollback: ${error.message}`,
      { ...report, error: 'config_invalid' },
      23
    );
  }
}

function walk(node, ptr = '$') {
  if (typeof node === 'string') {
    const match = node.match(/^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$/);
    if (match) {
      const key = match[1];
      const value = (env[key] || process.env[key] || '').trim();
      if (!value) report.refs.missing.push({ key, ptr });
      else if (forbiddenValues.has(value.toLowerCase())) report.refs.placeholder.push({ key, ptr });
    }
    return;
  }
  if (Array.isArray(node)) {
    node.forEach((item, i) => walk(item, `${ptr}[${i}]`));
    return;
  }
  if (node && typeof node === 'object') {
    for (const [key, value] of Object.entries(node)) walk(value, `${ptr}.${key}`);
  }
}
walk(config);

if (report.refs.missing.length || report.refs.placeholder.length) {
  const missing = report.refs.missing.map((r) => `${r.key} @ ${r.ptr}`);
  const placeholder = report.refs.placeholder.map((r) => `${r.key} @ ${r.ptr}`);
  fail(
    [
      '[openclaw-config-guard] Config references unresolved or fake env vars.',
      missing.length ? `Missing refs:\n- ${missing.join('\n- ')}` : null,
      placeholder.length ? `Placeholder refs:\n- ${placeholder.join('\n- ')}` : null,
      `Fix ${envPath}, then restart.`
    ].filter(Boolean).join('\n'),
    report,
    24
  );
}

// Normalize openclaw.json formatting once it proves valid.
const normalizedConfig = JSON.stringify(config, null, 2) + '\n';
if (fs.readFileSync(configPath, 'utf8') !== normalizedConfig) {
  fs.writeFileSync(configPath + '.tmp', normalizedConfig);
  JSON.parse(fs.readFileSync(configPath + '.tmp', 'utf8'));
  fs.renameSync(configPath + '.tmp', configPath);
  report.notes.push('Normalized openclaw.json formatting.');
}

// Refresh known-good backups after successful validation.
report.backups.knownGoodEnv = copyIfExists(envPath, 'known-good');
report.backups.knownGoodConfig = copyIfExists(configPath, 'known-good');
report.ok = true;
writeJson(path.join(stateDir, 'last-report.json'), report);
fs.writeFileSync(path.join(stateDir, 'last-success.txt'), `[openclaw-config-guard] OK ${now.toISOString()}\n`);
process.stdout.write('[openclaw-config-guard] OK\n');
