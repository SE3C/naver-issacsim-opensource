'use strict';

// Lightweight, read-only repository layout validation. No network, no rewrite.
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const pack = path.join(root, 'data', 'processed', 'ai_library');
const expectedNumbers = [...Array.from({ length: 9 }, (_, n) => n), ...Array.from({ length: 12 }, (_, n) => n + 10)];
const expected = expectedNumbers.map((n) => String(n).padStart(2, '0'));
const errors = [];
function readRequiredDirectory(folder) {
  const full = path.join(root, folder);
  try {
    if (!fs.statSync(full).isDirectory()) throw new Error('not a directory');
    return fs.readdirSync(full);
  } catch (error) {
    errors.push(`Missing or unreadable required directory: ${folder} (${error.code || error.message})`);
    return [];
  }
}
const topLevel = readRequiredDirectory('data/processed/ai_library')
  .filter((name) => name.endsWith('.md')).sort();
const numbered = topLevel.map((name) => /^([0-9]{2})_.+\.md$/.exec(name)?.[1] || '?');
if (numbered.join(',') !== expected.join(',')) {
  errors.push(`AI core pack numbers should be ${expected.join(',')}; actual: ${numbered.join(',')}`);
}

// Preserve the 21-file public upload contract while checking selected canonical navigation.
const docs = topLevel.map((name) => path.join(pack, name)).concat([
  'README.md',
  'PROJECT_CONTEXT.md',
  'docs/DATA_LAYOUT.md',
  'data/processed/README.md',
  'docs/reorganization/README.md',
  'data/processed/incoming/ot/README.md',
  'data/processed/reference/public/README.md',
  'data/processed/reference/regulations/README.md',
  'data/processed/external_analysis/README.md',
  'data/processed/external_analysis/video_reports/README.md',
  'data/processed/operations/README.md',
  'data/processed/operations/windows_h1_video_evaluation/README.md',
  'data/processed/operations/windows_go2_video_evaluation/README.md',
  'data/processed/planning/08_H1_OFFICIAL_TRAINING_OPS_CHECKLIST.md',
  'data/processed/planning/historical/2026-09-10_H1_OFFICIAL_TRAINING_CHECKLIST.md',
  'data/processed/operations/windows_go2_video_evaluation/model4800_release_notes.md',
  'data/processed/operations/windows_go2_video_evaluation/2026-10-09_G2_SUBMIT-3_MODEL4800_EVALUATION_RELEASE_NOTES.md',
  'data/processed/operations/windows_go2_video_evaluation/model7050_release_notes.md',
  'data/processed/operations/windows_go2_video_evaluation/2026-10-04_LINTRACK-125_MODEL7050_EVALUATION_RELEASE_NOTES.md',
  'data/processed/reference/official/2026_briefing_qna_analysis.md',
  'data/processed/reference/official/2026-08-14_OFFICIAL_BRIEFING_QA_ANALYSIS.md',
  'docs/reorganization/2026-10-13_STAGE6_FILE_PLACEMENT.md',
  'docs/reorganization/2026-10-13_STAGE7_WORK_TYPE_SPLIT.md',
  'docs/reorganization/2026-10-13_STAGE8_CROSS_REPOSITORY_NAVIGATION.md',
  'docs/reorganization/2026-10-13_STAGE9_DRAFT_LINK_CONSISTENCY.md',
  'docs/reorganization/2026-10-13_STAGE10_ORIGINALS_REVIEW_INDEX_LINKS.md',
  'docs/AI_LIBRARY_GUIDE.md',
  'research/EXPERIMENTS.md',
  'research/experiments/go2/G-005.md',
  'research/EXPERIMENT_NAMING.md',
  'research/submission_presets/README.md',
  'data/processed/incoming/README.md',
  'data/processed/incoming/RELATIONSHIPS.md',
  'data/processed/incoming/REPORT_CROSSWALK.md',
  'data/processed/incoming/REPORT_PROVENANCE_TRIAGE.md',
  'docs/reorganization/2026-10-12_STAGE5_SOURCE_COVERAGE.md',
  'docs/reorganization/2026-10-12_STAGE4_REPORT_LINKAGE.md',
  'data/processed/experiments/DERIVED_IDENTITY_MAP.md',
  'data/processed/experiments/RECENT_POLICY_LINKS.md',
  'data/processed/planning/INDEX.md',
  'data/processed/planning/historical/README.md',
  'docs/reorganization/2026-10-12_FILE_MOVE_PLAN.md',
  'docs/reorganization/2026-10-12_STAGE2_MOVE_PLAN.md',
  'docs/reorganization/2026-10-12_STAGE3_CLASSIFICATION_AND_MOVES.md',
  'data/processed/incoming/other/README.md',
  'data/processed/incoming/other/inbox/README.md',
  'data/processed/incoming/other/reviewed/README.md',
  'data/processed/experiments/h1/README.md',
  'data/processed/experiments/go2/README.md',
  'data/processed/reference/game_engine/README.md',
  'data/processed/reference/README.md',
  'data/processed/reference/09_GAME_AGENT_NAVIGATION_SENSORS.md',
  'data/processed/reference/game_engine/09_GAME_AGENT_NAVIGATION_SENSORS.md',
  'data/processed/experiments/h1/2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md',
  'data/processed/planning/historical/2026-09-27_H1_PERSONAL_FRESH_AND_CONTINUATION_PLAN.md',
  'docs/ai_prompts/README.md',
  'docs/ai_prompts/historical/README.md',
  'research/experiments/h1/README.md',
  'research/experiments/h1/planned/README.md',
  ...[
    '01_SOLUTION_BLUEPRINT.md',
    '02_PRIVATE_SERVER_VALIDATION_DESIGN.md',
    '03_NVIDIA_SERVER_OPERATIONS.md',
    '05_PROJECT_STATUS_AND_EVIDENCE_BASED_STRATEGY.md',
    '07_H1_SECOND_RUN_PARAMETER_COMPARISON_PLAN.md',
    '09_NCRC_V1_IMPLEMENTATION_AND_LIMITS.md',
  ].flatMap((name) => [
    'data/processed/planning/' + name,
    'data/processed/planning/historical/' + name,
  ]),
  ...[
    '04_OPTUNA_REWARD_SEARCH_DESIGN.md',
    '06_H1_OFFICIAL_SERVER_BASELINE_DIAGNOSTIC.md',
  ].flatMap((name) => [
    'data/processed/planning/' + name,
    'data/processed/planning/historical/' + name,
  ]),
  ...[
    'HS-001.md',
    'HS-002.md',
    'exp-h1-action-airtime-fresh-interaction.md',
    'exp-h1-action-first-airtime-switch.md',
    'exp-h1-action-first-body-rate-switch.md',
    'exp-h1-action-foot-contact-stability.md',
  ].flatMap((name) => [
    'research/experiments/h1/' + name,
    'research/experiments/h1/planned/' + name,
  ]),
  'docs/ai_prompts/AI_공통_사용자_지침_20260923.txt',
  'docs/ai_prompts/historical/AI_공통_사용자_지침_20260923.txt',
  ...['h1', 'go2'].flatMap((robot) => ['training', 'analysis'].flatMap((kind) => {
    const folder = 'data/processed/experiments/' + robot + '/' + kind;
    const names = readRequiredDirectory(folder).filter((name) => name.endsWith('.md'));
    const actual = names.filter((name) => name !== 'README.md').length;
    const expectedCount = { h1: { training: 10, analysis: 45 }, go2: { training: 5, analysis: 9 } }[robot][kind];
    if (actual !== expectedCount) errors.push(`Moved document count mismatch in ${folder}: expected ${expectedCount}, got ${actual}`);
    return names.map((name) => folder + '/' + name);
  })),
  // Generated indexes are optional until a controlled full build. If present,
  // validate their relative links, too (including ../ references).
  ...['data/processed/planning/_generated', 'data/processed/external_analysis/_generated']
    .flatMap((folder) => fs.existsSync(path.join(root, folder))
      ? readRequiredDirectory(folder).filter((name) => name.endsWith('.md')).map((name) => folder + '/' + name)
      : []),
].map((name) => path.join(root, name)));

let testedLinks = 0;
for (const file of docs) {
  const display = path.relative(root, file).replace(/\\/g, '/');
  if (!fs.existsSync(file)) { errors.push(`Missing required document: ${display}`); continue; }
  const original = fs.readFileSync(file, 'utf8');
  const body = original.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
  if (file.startsWith(pack + path.sep)) {
    // A date-stamped H2 preceding the document title confuses Markdown section routing.
    const firstHeading = body.match(/^#{1,6}\s+.*$/m)?.[0] || '';
    if (!/^# [^#]/.test(firstHeading)) errors.push(`Missing leading H1 in ${display}`);
  }
  const prose = body.replace(/^\s*```[^\n]*\n[\s\S]*?^\s*```[^\n]*$/gm, '');
  for (const match of prose.matchAll(/!?\[[^\]\n]*\]\(([^)\n]+)\)/g)) {
    const target = match[1].trim().replace(/\s+["'][^"']*["']$/, '');
    if (/^(?:https?:|mailto:|data:|#|\/\/)/i.test(target) || !target) continue;
    let href;
    try { href = decodeURIComponent(target.split('#')[0].split('?')[0]); }
    catch (_) { href = target.split('#')[0].split('?')[0]; }
    if (!href) continue;
    const resolved = path.resolve(path.dirname(file), href);
    if (!resolved.startsWith(root + path.sep)) continue; // external sibling checkout
    testedLinks++;
    if (!fs.existsSync(resolved)) errors.push(`Broken relative link ${display}: ${target}`);
  }
}
// Verify that each selected curated index lists all of its source files.
// This is read-only; missing/outdated inventory links fail the structure check.
for (const folder of [
  'docs/reorganization',
  'data/processed/incoming/ot',
  'data/processed/external_analysis/video_reports',
  'data/processed/incoming/other/reviewed',
  'data/processed/incoming/other/inbox',
  'data/processed/experiments/h1',
  'data/processed/experiments/go2',
  'data/processed/operations/windows_h1_video_evaluation',
  'data/processed/operations/windows_go2_video_evaluation',
]) {
  const dir = path.join(root, folder), index = path.join(dir, 'README.md');
  if (!fs.existsSync(dir) || !fs.existsSync(index)) {
    errors.push('Missing indexed directory: ' + folder);
    continue;
  }
  const listed = fs.readFileSync(index, 'utf8');
  function walk(folderPath) {
    const out = [];
    for (const item of fs.readdirSync(folderPath, { withFileTypes: true })) {
      const full = path.join(folderPath, item.name);
      if (item.isDirectory()) out.push(...walk(full));
      else if (item.isFile()) out.push(path.relative(dir, full).split(path.sep).join('/'));
    }
    return out;
  }
  for (const name of walk(dir)) {
    if (name === 'README.md' || name === '.gitkeep' || name.endsWith('/.gitkeep')) continue;
    const href = name.split('(').join('%28').split(')').join('%29').split(' ').join('%20').split('#').join('%23');
    if (!listed.includes('](./' + href + ')')) errors.push('Unlisted file in ' + folder + ': ' + name);
  }
}

// Require the noncanonical source triage ledger to list every preserved reviewed source.
const reviewedDir = path.join(root, 'data/processed/incoming/other/reviewed');
const triagePath = path.join(root, 'data/processed/incoming/REPORT_PROVENANCE_TRIAGE.md');
if (!fs.existsSync(triagePath)) errors.push('Missing reviewed source triage ledger');
else {
  const body = fs.readFileSync(triagePath, 'utf8');
  for (const name of readRequiredDirectory('data/processed/incoming/other/reviewed')) {
    if (name === 'README.md' || name === '.gitkeep') continue;
    const encoded = name.split('(').join('%28').split(')').join('%29').split(' ').join('%20').split('#').join('%23');
    if (!body.includes('](other/reviewed/' + encoded + ')'))
      errors.push('Unlisted reviewed source in triage ledger: ' + name);
  }
}
const issueText = errors.slice(0, 80);
console.log(JSON.stringify({
  status: errors.length ? 'FAIL' : 'PASS',
  coreMarkdownFiles: topLevel.length,
  documentsRead: docs.length,
  localRelativeLinksChecked: testedLinks,
  issues: issueText,
  moreIssues: Math.max(0, errors.length - issueText.length),
}, null, 2));
if (errors.length) process.exitCode = 1;
