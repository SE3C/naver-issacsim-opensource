'use strict';

// Read-only, isolated source-input tests. No real Originals file is opened
// and no knowledge-base output can be written by the injected filesystem.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const generator = path.join(__dirname, 'build_knowledge_base.js');
const script = fs.readFileSync(generator, 'utf8');
const raw = path.resolve(__dirname, '..', '..', 'naver-issacsim-originals', 'data', 'raw');
const lectures = path.join(raw, 'lectures');
const glossary = path.join(raw, 'glossary', 'page.htm');
const codebase = path.join(raw, 'codebase');
const ordinaryFilename = '01강의. 강화학습과 시뮬레이션 기초 · 탄생 · NAVER CONNECT ROBOTICS GUIDE BOOK.htm';
const ordinaryArticle = '<article id="readContent"><h1>01. 강화학습과 시뮬레이션 기초</h1><p>내용</p></article>';
const validGlossary = '<article class="glossary__term"><h3 class="glossary__term-name">용어</h3></article>';

function executeFixture(options = {}) {
  const dirs = new Set([raw, lectures, path.join(raw, 'glossary'), codebase]);
  const lessonName = options.filename || ordinaryFilename;
  const files = new Map([
    [path.join(lectures, lessonName), options.article ?? ordinaryArticle],
    [glossary, options.glossary ?? validGlossary],
    [path.join(codebase, 'code.py'), options.code ?? 'print(1)'],
  ]);
  if (options.zeroByte) files.set(path.join(codebase, 'height scanner.txt'), '');
  if (options.readmeOnly) {
    files.delete(path.join(codebase, 'code.py'));
    files.set(path.join(codebase, 'README.md'), 'Collected source metadata');
  }
  if (options.remove) {
    if (dirs.has(options.remove)) dirs.delete(options.remove);
    else files.delete(options.remove);
  }
  let writes = 0;
  const messages = [];
  function fsError(code) {
    const error = new Error(code);
    error.code = code;
    return error;
  }
  const fakeFs = {
    constants: fs.constants,
    statSync(file) {
      if (dirs.has(file)) return { isDirectory: () => true, isFile: () => false, size: 0 };
      if (files.has(file)) return { isDirectory: () => false, isFile: () => true, size: files.get(file).length };
      throw fsError('ENOENT');
    },
    accessSync(file) {
      if (!dirs.has(file) && !files.has(file)) throw fsError('ENOENT');
      if (file === options.denyRead) throw fsError('EACCES');
    },
    readdirSync(folder, opts) {
      if (!dirs.has(folder)) throw fsError('ENOENT');
      const names = [...files.keys()]
        .filter((file) => path.dirname(file) === folder).map((file) => path.basename(file));
      if (opts?.withFileTypes) return names.map((name) => ({
        name, isDirectory: () => false, isFile: () => true,
      }));
      return names;
    },
    readFileSync(file) {
      if (file === options.denyRead) throw fsError('EACCES');
      if (!files.has(file)) throw fsError('ENOENT');
      return files.get(file);
    },
    mkdirSync() { writes++; throw new Error('Unexpected output directory creation'); },
    writeFileSync() { writes++; throw new Error('Unexpected file write'); },
  };
  const processStub = {
    argv: [process.execPath, generator, ...(options.args ?? ['--preflight-only'])],
    exit(code) {
      const signal = new Error('Fixture exit');
      signal.code = 'FIXTURE_EXIT';
      signal.exitCode = code;
      throw signal;
    },
  };
  let exitCode;
  try {
    vm.runInNewContext(script, {
      require(name) {
        if (name === 'fs') return fakeFs;
        if (name === 'path') return path;
        if (name === 'crypto') return require('node:crypto');
        if (name === 'child_process') return require('node:child_process');
        throw new Error('Unexpected import: ' + name);
      },
      __dirname,
      process: processStub,
      console: { error: (...lines) => messages.push(lines.join(' ')),
        log: (...lines) => messages.push(lines.join(' ')) },
    }, { filename: generator, timeout: 4000 });
    throw new Error('Preflight unexpectedly entered full build');
  } catch (error) {
    if (error.code !== 'FIXTURE_EXIT') throw error;
    exitCode = error.exitCode;
  }
  assert.equal(writes, 0, 'Preflight must not create or change outputs');
  return { exitCode, messages: messages.join('\n') };
}

const tests = [
  ['normal lesson', {}, 0],
  ['00 special introduction', {
    filename: '00강의. 들어가며 · 탄생 · NAVER CONNECT ROBOTICS GUIDE BOOK.htm',
    article: '<article id="readContent"><div data-block="hook-0kang"><h1>세계를 휩쓰는 로보틱스의 물결</h1></div></article>',
  }, 0],
  ['21 appendix punctuation', {
    filename: '21강의. 부록 · 본선 연습 해보기 · 초월 · NAVER CONNECT ROBOTICS GUIDE BOOK.htm',
    article: '<article id="readContent"><h1>21. 부록, 본선 연습 해보기</h1></article>',
  }, 0],
  ['02 maps to 03 wrong lesson', {
    filename: '02강의. Isaac Sim 처음 열기 · 탄생 · NAVER CONNECT ROBOTICS GUIDE BOOK.htm',
    article: '<article id="readContent"><h1>03. 중력 만져보기</h1></article>',
  }, 2],
  ['same number wrong title', {
    filename: '02강의. Isaac Sim 처음 열기 · 탄생 · NAVER CONNECT ROBOTICS GUIDE BOOK.htm',
    article: '<article id="readContent"><h1>02. 중력 만져보기</h1></article>',
  }, 2],
  ['empty article', { article: '<article id="readContent"></article>' }, 2],
  ['loading placeholder', { article: '<article id="readContent">불러오는 중이에요…</article>' }, 2],
  ['not an article', { article: '<article><p>other</p></article><span id="readContent"></span>' }, 2],
  ['empty glossary', { glossary: '<article class="glossary__term"></article>' }, 2],
  ['whitespace codebase', { code: '  \n\t' }, 2],
  ['README only', { readmeOnly: true }, 2],
  ['zero byte historical file plus valid code', { zeroByte: true }, 0],
  ['CLI typo', { args: ['--preflght-only'] }, 2],
  ['missing required glossary', { remove: glossary }, 2],
  ['nested article valid', {
    article: '<article id="outer"><article id="readContent"><h1>01. 강화학습과 시뮬레이션 기초</h1></article></article>',
  }, 0],
];
// Keep every observed 2026-10-14 source-identity mismatch as a fixture.
for (const [number, title, chapter, observedHeading] of [
  ['02', 'Isaac Sim 처음 열기', '탄생', '03. 중력 만져보기'],
  ['03', '중력 만져보기', '탄생', '04. 로봇 불러오기'],
  ['05', '관절 움직이기', '각성', '06. 지형 만들기'],
  ['06', '지형 만들기', '각성', '07. 카메라로 보기'],
  ['08', '라이다로 거리 재기', '각성', '09. 키보드로 조작하기'],
  ['16', 'policy.pt 파일 준비하기', '진화', '17. 자연어를 로봇 명령으로'],
]) {
  tests.push(['observed mislabeled ' + number, {
    filename: number + '강의. ' + title + ' · ' + chapter + ' · NAVER CONNECT ROBOTICS GUIDE BOOK.htm',
    article: '<article id="readContent"><h1>' + observedHeading + '</h1></article>',
  }, 2]);
}
for (const [number, title, chapter] of [
  ['04', '로봇 불러오기', '탄생'], ['07', '카메라로 보기', '각성'],
  ['09', '키보드로 조작하기', '각성'], ['12', '로봇 학습 준비하기', '진화'],
  ['14', '보상 함수 설계와 조정', '진화'], ['15', '학습 관찰과 진단', '진화'],
  ['17', '자연어를 로봇 명령으로', '초월'],
  ['18', '믿을 수 있는 로봇 명령 만들기', '초월'],
  ['19', '생각하는 로봇, 완성', '초월'],
]) {
  tests.push(['observed loading-only ' + number, {
    filename: number + '강의. ' + title + ' · ' + chapter + ' · NAVER CONNECT ROBOTICS GUIDE BOOK.htm',
    article: '<article id="readContent"><div class="read__loading">불러오는 중이에요…</div></article>',
  }, 2]);
}
for (const [name, fixture, expected] of tests) {
  const result = executeFixture(fixture);
  assert.equal(result.exitCode, expected, name + ': ' + result.messages);
  process.stdout.write('PASS ' + name + ' (exit ' + result.exitCode + ', writes 0)\n');
}
process.stdout.write('PASS ' + tests.length + ' isolated lecture preflight fixtures\n');
