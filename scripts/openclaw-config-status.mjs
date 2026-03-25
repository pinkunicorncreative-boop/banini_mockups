#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const HOME = os.homedir();
const envPath = path.join(HOME, '.openclaw', '.env');
const configPath = path.join(HOME, '.openclaw', 'openclaw.json');
const stateDir = path.join(HOME, '.openclaw', 'state', 'config-guard');
const reportPath = path.join(stateDir, 'last-report.json');
const failurePath = path.join(stateDir, 'last-failure.txt');

const REQUIRED = ['GEMINI_API_KEY', 'OPENCLAW_GATEWAY_TOKEN'];
const OPTIONAL = ['NANO_BANANA_PRO_API_KEY', 'NOTION_API_KEY', 'OPENAI_API_KEY', 'ELEVENLABS_API_KEY'];
const FORBIDDEN = new Set(['replace_me','changeme','your_api_key_here','your_token_here','example','test','dummy','null','undefined']);

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
function mask(value='') {
  if (!value) return '(missing)';
  if (value.length <= 8) return '****';
  return `${value.slice(0,4)}…${value.slice(-4)}`;
}
function state(value) {
  if (!value) return 'missing';
  if (FORBIDDEN.has(String(value).trim().toLowerCase())) return 'placeholder';
  return 'set';
}

const env = fs.existsSync(envPath) ? parseEnv(fs.readFileSync(envPath, 'utf8')) : {};
const report = fs.existsSync(reportPath) ? JSON.parse(fs.readFileSync(reportPath, 'utf8')) : null;
const failure = fs.existsSync(failurePath) ? fs.readFileSync(failurePath, 'utf8').trim() : null;
const config = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf8')) : {};

const integrations = {
  core: ['GEMINI_API_KEY', 'OPENCLAW_GATEWAY_TOKEN'],
  'nano-banana-pro': ['NANO_BANANA_PRO_API_KEY'],
  notion: ['NOTION_API_KEY'],
  openai: ['OPENAI_API_KEY'],
  elevenlabs: ['ELEVENLABS_API_KEY']
};

const lines = [];
lines.push('OPENCLAW CONFIG STATUS');
lines.push('');
lines.push(`env file: ${envPath}`);
lines.push(`config:   ${configPath}`);
lines.push('');
lines.push('Secrets');
for (const key of [...REQUIRED, ...OPTIONAL]) {
  lines.push(`- ${key}: ${state(env[key])} ${state(env[key]) === 'set' ? mask(env[key]) : ''}`.trim());
}
lines.push('');
lines.push('Integrations');
for (const [name, keys] of Object.entries(integrations)) {
  const statuses = keys.map((k) => state(env[k]));
  const integrationState = statuses.every((s) => s === 'set') ? 'enabled' : (name === 'core' ? 'broken' : 'disabled');
  lines.push(`- ${name}: ${integrationState}`);
}
lines.push('');
if (report) {
  lines.push(`Last guard run: ${report.timestamp}`);
  if (report.json?.restored?.length) {
    lines.push('Recovered JSON:');
    for (const item of report.json.restored) lines.push(`- ${item.file} <= ${item.backup}`);
  }
  if (report.notes?.length) {
    lines.push('Notes:');
    for (const note of report.notes) lines.push(`- ${note}`);
  }
  lines.push('');
}
if (failure) {
  lines.push('Last failure');
  lines.push(failure);
  lines.push('');
}
if (config?.skills?.entries) {
  lines.push('Configured skill refs');
  for (const [key, value] of Object.entries(config.skills.entries)) {
    const apiKey = value && typeof value === 'object' ? value.apiKey : undefined;
    if (typeof apiKey === 'string') lines.push(`- ${key}: ${apiKey}`);
  }
}
console.log(lines.join('\n'));
