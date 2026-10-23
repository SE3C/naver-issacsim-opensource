const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const childProcess = require('child_process');

const projectRoot = path.resolve(__dirname, '..');
const rawRoot = path.resolve(projectRoot, '..', 'naver-issacsim-originals', 'data', 'raw');
const processedRoot = path.join(projectRoot, 'data', 'processed');
const lessonSourceDir = path.join(rawRoot, 'lectures');
const glossarySource = path.join(rawRoot, 'glossary', 'page.htm');
const codeSourceDir = path.join(rawRoot, 'codebase');
const serverBackupSourceDir = path.join(rawRoot, 'server_backup', 'extracted');
const externalServerAnalysisDir = path.join(rawRoot, 'external_analysis', 'server_backup');
const planningSourceDir = path.join(rawRoot, 'planning');

// Reject CLI mistakes before checking inputs or creating any output directories.
// Preserve the historical no-argument full-build invocation.
const cliArgs = process.argv.slice(2);
if (cliArgs.length > 1 || (cliArgs.length === 1 && cliArgs[0] !== '--preflight-only')) {
  console.error('Unknown knowledge-base CLI option(s): ' + cliArgs.join(' '));
  console.error('Usage: node tools/build_knowledge_base.js [--preflight-only]');
  process.exit(2);
}
const preflightOnly = cliArgs[0] === '--preflight-only';

// Preflight must run before even creating output directories; a missing,
// incomplete or unreadable mandatory Originals corpus must not trigger a build.
// Optional planning, server backup and external analysis inputs stay optional.
const requiredInputs = [
  ['lectures', lessonSourceDir, 'directory'],
  ['glossary saved page', glossarySource, 'file'],
  ['legacy codebase', codeSourceDir, 'directory'],
];
const inputIssues = [];
for (const [name, source, type] of requiredInputs) {
  try {
    const st = fs.statSync(source);
    if (type === 'file' ? !st.isFile() : !st.isDirectory()) {
      inputIssues.push(`${name}: wrong input type: ${source}`);
    } else {
      fs.accessSync(source, fs.constants.R_OK);
    }
  } catch (error) {
    inputIssues.push(`${name}: missing or unreadable: ${source} (${error.code || error.message})`);
  }
}
if (!inputIssues.length) {
  try {
    const lessonNames = fs.readdirSync(lessonSourceDir)
      .filter((name) => name.toLowerCase().endsWith('.htm'));
    if (!lessonNames.length) inputIssues.push('lectures: no .htm source pages');
    for (const name of lessonNames) {
      const source = path.join(lessonSourceDir, name);
      try {
        const html = fs.readFileSync(source, 'utf8');
        // The full build uses the same article/identity/content extraction.
        const article = extractBalancedArticle(html, 'id="readContent"');
        const { plainText, codeBlocks } = htmlToTextAndCode(article);
        const meaningfulText = plainText
          .replace(/\[\[CODE_BLOCK_\d+\]\]/g, '')
          .replace(/^불러오는 중이에요…$/, '')
          .trim();
        const hasCode = codeBlocks.some((block) => block.code.trim());
        const hasVideo = /<button\b[^>]*\bdata-id="[^"]+"[^>]*>/i.test(article);
        const hasImage = [...article.matchAll(/<img\b[^>]*>/gi)]
          .some((match) => Boolean(attr(match[0], 'src')));
        if (!meaningfulText && !hasCode && !hasVideo && !hasImage) {
          inputIssues.push(`lectures: no extractable text, code, video or image: ${source}`);
        } else {
          assertLessonSourceIdentity(name, article);
        }
      } catch (error) {
        inputIssues.push(`lectures: invalid saved source ${source}: ${error.message}`);
      }
    }
  } catch (error) {
    inputIssues.push(`lectures: cannot enumerate/read pages (${error.code || error.message})`);
  }
  try {
    const html = fs.readFileSync(glossarySource, 'utf8');
    if (!extractGlossaryTerms(html).length) {
      inputIssues.push('glossary: no extractable named glossary terms');
    }
  } catch (error) {
    inputIssues.push(`glossary: cannot read page (${error.code || error.message})`);
  }
  try {
    // Historical zero-byte files are allowed; the complete corpus must not be empty.
    const entries = walkFiles(codeSourceDir);
    if (!entries.length) inputIssues.push('legacy codebase: no input files');
    let hasContent = false;
    for (const name of entries) {
      const source = path.join(codeSourceDir, ...name.split('/'));
      const stat = fs.statSync(source);
      if (!stat.isFile()) throw new Error(`not a regular file: ${source}`);
      // The full build reads UTF-8; whitespace alone is not a corpus.
      // README is collection metadata, not evidence of usable code files.
      if (path.basename(name).toLowerCase() !== 'readme.md' && fs.readFileSync(source, 'utf8').trim()) {
        hasContent = true;
      } else if (path.basename(name).toLowerCase() === 'readme.md') {
        fs.readFileSync(source, 'utf8'); // Still fail on an unreadable preserved README.
      }
    }
    if (entries.length && !hasContent) inputIssues.push('legacy codebase: all files are empty');
  } catch (error) {
    inputIssues.push(`legacy codebase: cannot enumerate/read files (${error.code || error.message})`);
  }
}
if (inputIssues.length) {
  console.error('Knowledge base preflight FAILED: required raw input invalid.');
  for (const issue of inputIssues) console.error('- ' + issue);
  process.exit(2);
}
if (preflightOnly) {
  console.log('Knowledge base input preflight PASS (no files written).');
  for (const [name, source] of requiredInputs) console.log(`- ${name}: ${source}`);
  console.log('Note: this does not validate the complete build or its optional inputs.');
  process.exit(0);
}

const output = {
  lessons: path.join(processedRoot, 'lessons'),
  glossary: path.join(processedRoot, 'glossary'),
  codebase: path.join(processedRoot, 'codebase'),
  serverBackup: path.join(processedRoot, 'server_backup'),
  serverReports: path.join(processedRoot, 'server_backup', 'reports'),
  serverCatalog: path.join(processedRoot, 'server_backup', 'catalog'),
  serverTraining: path.join(processedRoot, 'server_backup', 'code', 'training'),
  serverPracticeSim: path.join(processedRoot, 'server_backup', 'code', 'practice_sim'),
  serverExamples: path.join(processedRoot, 'server_backup', 'code', 'examples'),
  serverWorkspace: path.join(processedRoot, 'server_backup', 'code', 'workspace'),
  planning: path.join(processedRoot, 'planning'),
  planningGenerated: path.join(processedRoot, 'planning', '_generated'),
  external: path.join(processedRoot, 'external_analysis'),
  externalGenerated: path.join(processedRoot, 'external_analysis', '_generated'),
};

for (const directory of Object.values(output)) {
  fs.mkdirSync(directory, { recursive: true });
}

function serverOutputDirectory(area) {
  if (area === 'robot_training') return output.serverTraining;
  if (area === 'practice_simulator') return output.serverPracticeSim;
  if (area === 'course_examples') return output.serverExamples;
  return output.serverWorkspace;
}

function serverProcessedPath(filename, area) {
  const parts = filename.split('/');
  const usesDedicatedArea = area === 'robot_training'
    || area === 'practice_simulator'
    || area === 'course_examples';
  const relativeParts = usesDedicatedArea ? parts.slice(1) : parts;
  relativeParts[relativeParts.length - 1] = `${relativeParts[relativeParts.length - 1]}.md`;
  return path.join(serverOutputDirectory(area), ...relativeParts);
}

function decode(value) {
  return String(value || '')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"')
    .replace(/&#x27;|&#39;/gi, "'")
    .replace(/&#(\d+);/g, (_, number) => String.fromCodePoint(Number(number)));
}

function attr(tag, name) {
  const match = new RegExp(`\\b${name}\\s*=\\s*["']([^"']*)["']`, 'i').exec(tag);
  return match ? decode(match[1]) : null;
}

function relative(filePath) {
  return path.relative(projectRoot, filePath).replace(/\\/g, '/');
}

function slug(value) {
  return String(value)
    .normalize('NFKC')
    .replace(/[\\/:*?"<>|]/g, '_')
    .replace(/\s+/g, ' ')
    .trim();
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function cleanText(fragment) {
  const text = String(fragment || '')
    .replace(/<script\b[\s\S]*?<\/script>/gi, '')
    .replace(/<style\b[\s\S]*?<\/style>/gi, '')
    .replace(/<svg\b[\s\S]*?<\/svg>/gi, '')
    .replace(/<canvas\b[\s\S]*?<\/canvas>/gi, '')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/span>/gi, ' ')
    .replace(/<\/(?:h[1-6]|p|section|div|ul|ol|li|button|figure|figcaption|blockquote)>/gi, '\n')
    .replace(/<li\b[^>]*>/gi, '- ')
    .replace(/<[^>]+>/g, '');

  return decode(text)
    .replace(/\r/g, '')
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n[ \t]+/g, '\n')
    .replace(/[ \t]{2,}/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line && !['▶', '✕ 영상 닫기', '저장', '→', '3D 불러오는 중…'].includes(line))
    .join('\n\n')
    .trim();
}

function extractBalancedArticle(markup, markerText) {
  const requestedId = /id=["']([^"']+)["']/.exec(markerText)?.[1];
  if (!requestedId) throw new Error(`Invalid article marker: ${markerText}`);
  const tags = /<\/?article\b[^>]*>/gi;
  const stack = [];
  let match;
  while ((match = tags.exec(markup))) {
    if (/^<\/article\b/i.test(match[0])) {
      const opened = stack.pop();
      if (opened?.target) return markup.slice(opened.start, tags.lastIndex);
    } else {
      // Match an article's own id, never an earlier article or a span.
      const idAttribute = [...match[0].matchAll(/\s+([^\s=/>]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g)]
        .find((attribute) => attribute[1].toLowerCase() === 'id');
      const id = idAttribute?.[2] ?? idAttribute?.[3];
      stack.push({ start: match.index, target: id === requestedId });
    }
  }
  throw new Error(`Balanced article with marker not found: ${markerText}`);
}

function extractGlossaryTerms(html) {
  const terms = [];
  const glossaryPattern = /<article\s+class="glossary__term"[^>]*>([\s\S]*?)<\/article>/gi;
  let glossaryMatch;
  while ((glossaryMatch = glossaryPattern.exec(html))) {
    const fragment = glossaryMatch[1];
    const name = cleanText((/glossary__term-name[^>]*>([\s\S]*?)<\/h3>/i.exec(fragment) || [])[1]);
    const english = cleanText((/glossary__(?:en|abbr)[^>]*>([\s\S]*?)<\/span>/i.exec(fragment) || [])[1]);
    const definition = cleanText((/glossary__term-def[^>]*>([\s\S]*?)<\/p>/i.exec(fragment) || [])[1]);
    const related = [...fragment.matchAll(/glossary__chip[^>]*>([\s\S]*?)<\/(?:a|span)>/gi)]
      .map((match) => cleanText(match[1]));
    if (name) terms.push({ name, english: english || null, definition, related });
  }
  return terms;
}

// Saved file labels must match the identity of the article being converted.
// The 00 introduction uses a themed H1; the 21 appendix includes a subtitle
// separated by a middle dot in its filename and a comma in its H1.
function assertLessonSourceIdentity(filename, article) {
  const expected = /^(\d{2})강의\.\s*(.*?)\s*·\s*(탄생|각성|진화|초월)\s*·\s*NAVER CONNECT/i.exec(filename);
  if (!expected) throw new Error(`unrecognized lecture filename: ${filename}`);
  const number = Number(expected[1]);
  if (number === 0) {
    if (!/\bdata-block=(["'])hook-0kang\1/i.test(article)) {
      throw new Error('00 introduction is missing its original hook-0kang content');
    }
    return;
  }
  const heading = cleanText((/<h1\b[^>]*>([\s\S]*?)<\/h1>/i.exec(article) || [])[1]);
  const actual = /^(\d{1,2})\s*\.\s*(.+)$/.exec(heading);
  const normalize = (value) => value.normalize('NFKC').toLowerCase()
    .replace(/[.,·・，!?：:／/()'“”_-]+/g, ' ')
    .replace(/\s+/g, ' ').trim();
  if (!actual || Number(actual[1]) !== number
      || normalize(actual[2]) !== normalize(expected[2])) {
    throw new Error(`expected ${expected[1]}. ${expected[2]}, got ${heading || '[no H1]'}`);
  }
}

function htmlToTextAndCode(article) {
  const codeBlocks = [];
  const replaced = article.replace(/<pre\b[^>]*>([\s\S]*?)<\/pre>/gi, (full, inner) => {
    const language = (/(?:language-|lang-)([a-z0-9_+-]+)/i.exec(full) || [])[1] || 'text';
    const code = decode(inner.replace(/<br\s*\/?>/gi, '\n').replace(/<[^>]+>/g, ''))
      .replace(/\r\n/g, '\n')
      .trim();
    const index = codeBlocks.length;
    codeBlocks.push({ index, language, code });
    return `\n\n[[CODE_BLOCK_${index}]]\n\n`;
  });
  return { plainText: cleanText(replaced), codeBlocks };
}

function splitText(text, maxLength = 1800) {
  const paragraphs = String(text || '').split(/\n{2,}/).filter(Boolean);
  const chunks = [];
  let current = '';

  for (const paragraph of paragraphs) {
    if (current && current.length + paragraph.length + 2 > maxLength) {
      chunks.push(current);
      current = '';
    }
    if (paragraph.length > maxLength) {
      for (let offset = 0; offset < paragraph.length; offset += maxLength) {
        if (current) chunks.push(current);
        chunks.push(paragraph.slice(offset, offset + maxLength));
        current = '';
      }
    } else {
      current = current ? `${current}\n\n${paragraph}` : paragraph;
    }
  }
  if (current) chunks.push(current);
  return chunks;
}

function splitCode(code, maxLength = 5000) {
  const lines = String(code || '').split('\n');
  const chunks = [];
  let current = [];
  let length = 0;
  for (const line of lines) {
    if (current.length && length + line.length + 1 > maxLength) {
      chunks.push(current.join('\n'));
      current = [];
      length = 0;
    }
    current.push(line);
    length += line.length + 1;
  }
  if (current.length) chunks.push(current.join('\n'));
  return chunks;
}

function detectLanguage(filename, content) {
  const lower = filename.toLowerCase();
  if (lower.endsWith('.md')) return 'markdown';
  if (lower.endsWith('.py') || lower.endsWith('.py.txt')) return 'python';
  if (/^(?:from\s+\S+\s+import|import\s+\S+|def\s+\w+\(|class\s+\w+)/m.test(content)) return 'python';
  return 'text';
}

function writeJsonl(filePath, rows) {
  fs.writeFileSync(filePath, rows.map((row) => JSON.stringify(row)).join('\n') + (rows.length ? '\n' : ''), 'utf8');
}

function walkFiles(root, current = root) {
  const files = [];
  for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
    const fullPath = path.join(current, entry.name);
    if (entry.isDirectory()) files.push(...walkFiles(root, fullPath));
    else if (entry.isFile()) files.push(path.relative(root, fullPath).replace(/\\/g, '/'));
  }
  return files;
}

const serverTextExtensions = new Set([
  '.py', '.md', '.toml', '.yaml', '.yml', '.json', '.txt', '.rst',
  '.sh', '.bat', '.ps1', '.ini', '.cfg', '.xml', '.html', '.gitignore',
]);

function sha1(value) {
  return crypto.createHash('sha1').update(String(value)).digest('hex');
}

function serverArea(relativePath) {
  const top = relativePath.split('/')[0];
  if (top === 'training') return 'robot_training';
  if (top === 'practice_sim') return 'practice_simulator';
  if (top === 'examples') return 'course_examples';
  if (top === 'IsaacLab') return 'vendored_isaaclab';
  if (top === '.vscode') return 'workspace_configuration';
  if (top === 'student_workspace') return 'student_workspace';
  if (/^NvStreamer-.*\.etli$/i.test(top)) return 'streaming_trace';
  return 'workspace_root';
}

function isSensitiveServerPath(relativePath) {
  const name = path.posix.basename(relativePath);
  return name === 'practice_key.bin'
    || /^\.env(?:\.|$)/i.test(name)
    || /(?:^|[_-])(secret|credential|password|private[_-]?key|access[_-]?token)(?:[_\-.]|$)/i.test(name);
}

function serverLanguage(filename, content) {
  const extension = path.extname(filename).toLowerCase();
  const languages = {
    '.py': 'python', '.md': 'markdown', '.toml': 'toml', '.yaml': 'yaml',
    '.yml': 'yaml', '.json': 'json', '.rst': 'rst', '.sh': 'shell',
    '.bat': 'batch', '.ps1': 'powershell', '.ini': 'ini', '.cfg': 'config',
    '.xml': 'xml', '.html': 'html', '.gitignore': 'gitignore', '.txt': 'text',
  };
  return languages[extension] || detectLanguage(filename, content);
}

function serverIngestionDecision(relativePath, bytes) {
  const normalized = relativePath.replace(/\\/g, '/');
  const extension = path.extname(normalized).toLowerCase();
  if (isSensitiveServerPath(normalized)) return { include: false, reason: 'sensitive_name' };
  if (normalized === '.DS_Store' || normalized.endsWith('/.DS_Store')) return { include: false, reason: 'metadata_file' };
  if (normalized.includes('/.git/') || normalized.startsWith('.git/')) return { include: false, reason: 'git_internal' };
  if (normalized.startsWith('IsaacLab/')) return { include: false, reason: 'vendored_dependency' };
  if (!/^(training|practice_sim|examples|\.vscode)\//.test(normalized)) return { include: false, reason: 'outside_project_text_scope' };
  if (!serverTextExtensions.has(extension)) return { include: false, reason: 'binary_or_unsupported' };
  if (bytes > 1024 * 1024) return { include: false, reason: 'text_file_over_1mib' };
  return { include: true, reason: 'project_text' };
}

function safeGit(args) {
  try {
    return childProcess.execFileSync('git', args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
  } catch {
    return null;
  }
}

const documents = [];
const chunkRows = [];
const videoRequests = [];
const imageRequests = [];

function addDocument(document, options = {}) {
  documents.push(document);
  const contentChunks = options.code
    ? splitCode(document.content)
    : splitText(document.content);
  contentChunks.forEach((text, chunkIndex) => {
    chunkRows.push({
      id: `${document.id}-chunk-${String(chunkIndex + 1).padStart(3, '0')}`,
      documentId: document.id,
      sourceType: document.sourceType,
      title: document.title,
      chapter: document.chapter || null,
      lessonNumber: document.lessonNumber ?? null,
      contentType: options.code ? 'code' : 'text',
      language: options.language || null,
      chunkIndex,
      text,
    });
  });
}

const lessonFiles = fs.readdirSync(lessonSourceDir)
  .filter((name) => name.toLowerCase().endsWith('.htm'))
  .sort((a, b) => a.localeCompare(b, 'ko'));

for (const filename of lessonFiles) {
  const sourcePath = path.join(lessonSourceDir, filename);
  const html = fs.readFileSync(sourcePath, 'utf8');
  const parsedName = /^(\d{2})강의\.\s*(.*?)\s*·\s*(.*?)\s*·\s*NAVER CONNECT/i.exec(filename);
  const lessonNumber = parsedName ? Number(parsedName[1]) : null;
  const lessonTitle = parsedName ? parsedName[2] : path.basename(filename, '.htm');
  const chapter = parsedName ? parsedName[3] : '미분류';
  const article = extractBalancedArticle(html, 'id="readContent"');
  assertLessonSourceIdentity(filename, article);
  const { plainText, codeBlocks } = htmlToTextAndCode(article);
  const headings = [...article.matchAll(/<h([1-6])\b[^>]*>([\s\S]*?)<\/h\1>/gi)]
    .map((match) => ({ level: Number(match[1]), text: cleanText(match[2]) }));
  const videos = [...article.matchAll(/<button\b[^>]*\bdata-id="([^"]+)"[^>]*>/gi)]
    .map((match) => ({
      id: match[1],
      label: attr(match[0], 'data-lb') || attr(match[0], 'aria-label') || '영상',
      url: `https://www.youtube.com/watch?v=${match[1]}`,
    }));
  const imageReferences = unique([...article.matchAll(/<img\b[^>]*>/gi)].map((match) => attr(match[0], 'src')));
  const id = `lecture-${String(lessonNumber).padStart(2, '0')}`;
  const markdownFilename = `${String(lessonNumber).padStart(2, '0')}_${slug(lessonTitle)}.md`;
  let markdownBody = plainText;
  for (const block of codeBlocks) {
    markdownBody = markdownBody.replace(
      `[[CODE_BLOCK_${block.index}]]`,
      `\`\`\`${block.language}\n${block.code}\n\`\`\``,
    );
  }
  const markdown = [
    '---',
    `id: ${id}`,
    `source_type: lecture`,
    `lesson_number: ${lessonNumber}`,
    `chapter: ${JSON.stringify(chapter)}`,
    `title: ${JSON.stringify(lessonTitle)}`,
    `source: ${JSON.stringify(relative(sourcePath))}`,
    '---',
    '',
    `# ${lessonNumber}강. ${lessonTitle}`,
    '',
    markdownBody,
    '',
    '## 외부 영상',
    '',
    ...(videos.length ? videos.map((video) => `- [${video.label}](${video.url}) — 분석 대기`) : ['- 없음']),
    '',
  ].join('\n');
  const processedPath = path.join(output.lessons, markdownFilename);
  fs.writeFileSync(processedPath, markdown, 'utf8');

  const document = {
    id,
    sourceType: 'lecture',
    lessonNumber,
    chapter,
    title: lessonTitle,
    source: relative(sourcePath),
    processed: relative(processedPath),
    content: plainText,
    headings,
    codeBlocks,
    videos,
    imageReferences,
  };
  addDocument(document);

  for (const block of codeBlocks) {
    splitCode(block.code).forEach((text, chunkIndex) => {
      chunkRows.push({
        id: `${id}-code-${String(block.index + 1).padStart(3, '0')}-${String(chunkIndex + 1).padStart(3, '0')}`,
        documentId: id,
        sourceType: 'lecture',
        title: lessonTitle,
        chapter,
        lessonNumber,
        contentType: 'code',
        language: block.language,
        codeBlockIndex: block.index,
        chunkIndex,
        text,
      });
    });
  }

  for (const video of videos) {
    videoRequests.push({
      requestId: `video-${video.id}`,
      documentId: id,
      lessonNumber,
      lessonTitle,
      label: video.label,
      url: video.url,
      status: 'pending_external_analysis',
      requestedFields: [
        'summary',
        'timestamped_scenes',
        'technical_concepts',
        'visible_code_or_commands',
        'procedures',
        'warnings',
      ],
    });
  }

  for (const [imageIndex, imageReference] of imageReferences.entries()) {
    let localPath = null;
    if (!/^https?:\/\//i.test(imageReference)) {
      try {
        localPath = path.resolve(path.dirname(sourcePath), decodeURIComponent(imageReference.split(/[?#]/)[0]));
      } catch {
        localPath = path.resolve(path.dirname(sourcePath), imageReference.split(/[?#]/)[0]);
      }
    }
    const sourceExists = localPath ? fs.existsSync(localPath) : null;
    imageRequests.push({
      requestId: `${id}-image-${String(imageIndex + 1).padStart(3, '0')}`,
      documentId: id,
      lessonNumber,
      lessonTitle,
      imageReference,
      localSource: localPath ? relative(localPath) : null,
      sourceExists,
      status: sourceExists === false ? 'missing_source_file' : 'pending_external_analysis',
      requestedFields: [
        'visual_summary',
        'visible_text',
        'ui_steps_or_controls',
        'code_or_commands',
        'diagram_relationships',
        'warnings',
      ],
    });
  }
}

const glossaryHtml = fs.readFileSync(glossarySource, 'utf8');
const declaredGlossaryCount = Number((/glossary__navlink[^>]*data-cat=""[^>]*>[^<]*<span>(\d+)<\/span>/i.exec(glossaryHtml) || [])[1] || 0);
const glossaryTerms = extractGlossaryTerms(glossaryHtml);

const glossaryMarkdown = [
  '# 단어 사전',
  '',
  `- 저장본에서 추출한 항목: ${glossaryTerms.length}개`,
  `- 원본 화면이 선언한 전체 항목: ${declaredGlossaryCount || '알 수 없음'}개`,
  '- 제한: 저장된 HTML에는 첫 페이지 항목만 포함되어 있어 전체 사전이 아닙니다.',
  '',
  ...glossaryTerms.flatMap((term) => [
    `## ${term.name}${term.english ? ` (${term.english})` : ''}`,
    '',
    term.definition,
    '',
    term.related.length ? `관련어: ${term.related.join(', ')}` : '관련어: 없음',
    '',
  ]),
].join('\n');
fs.writeFileSync(path.join(output.glossary, 'glossary.md'), glossaryMarkdown, 'utf8');
writeJsonl(path.join(output.glossary, 'terms.jsonl'), glossaryTerms.map((term, index) => ({
  id: `glossary-${String(index + 1).padStart(3, '0')}`,
  ...term,
  source: relative(glossarySource),
})));

glossaryTerms.forEach((term, index) => {
  addDocument({
    id: `glossary-${String(index + 1).padStart(3, '0')}`,
    sourceType: 'glossary',
    title: term.name,
    source: relative(glossarySource),
    processed: 'data/processed/glossary/glossary.md',
    content: [term.english, term.definition, term.related.length ? `관련어: ${term.related.join(', ')}` : ''].filter(Boolean).join('\n\n'),
    english: term.english,
    related: term.related,
  });
});

const codeFiles = walkFiles(codeSourceDir).sort((a, b) => a.localeCompare(b, 'ko'));
for (const filename of codeFiles) {
  const sourcePath = path.join(codeSourceDir, ...filename.split('/'));
  const content = fs.readFileSync(sourcePath, 'utf8').replace(/\r\n/g, '\n');
  const language = detectLanguage(filename, content);
  const id = `code-${slug(filename).toLowerCase().replace(/[^a-z0-9가-힣]+/g, '-')}`;
  const processedPath = path.join(output.codebase, ...filename.split('/')) + '.md';
  fs.mkdirSync(path.dirname(processedPath), { recursive: true });
  const markdown = [
    '---',
    `id: ${id}`,
    'source_type: codebase',
    `language: ${language}`,
    `source: ${JSON.stringify(relative(sourcePath))}`,
    '---',
    '',
    `# ${filename}`,
    '',
    `\`\`\`${language === 'text' ? '' : language}`,
    content,
    '\`\`\`',
    '',
  ].join('\n');
  fs.writeFileSync(processedPath, markdown, 'utf8');
  addDocument({
    id,
    sourceType: 'codebase',
    title: filename,
    source: relative(sourcePath),
    processed: relative(processedPath),
    content,
    language,
    lineCount: content ? content.split('\n').length : 0,
  }, { code: language === 'python', language });
}

const serverInventory = {
  present: fs.existsSync(serverBackupSourceDir),
  files: [],
  selectedFiles: [],
  areas: [],
  extensions: [],
  largestFiles: [],
  sensitiveFiles: [],
  isaacLab: null,
};

if (serverInventory.present) {
  const serverFiles = walkFiles(serverBackupSourceDir).sort((a, b) => a.localeCompare(b, 'en'));
  const areaMap = new Map();
  const extensionMap = new Map();

  for (const filename of serverFiles) {
    const sourcePath = path.join(serverBackupSourceDir, ...filename.split('/'));
    const stat = fs.statSync(sourcePath);
    const extension = path.extname(filename).toLowerCase() || '[none]';
    const area = serverArea(filename);
    const sensitive = isSensitiveServerPath(filename);
    const decision = serverIngestionDecision(filename, stat.size);
    const row = {
      path: filename,
      area,
      extension,
      bytes: stat.size,
      sensitive,
      corpusIncluded: decision.include,
      exclusionReason: decision.include ? null : decision.reason,
    };
    serverInventory.files.push(row);
    if (decision.include) serverInventory.selectedFiles.push(filename);
    if (sensitive) serverInventory.sensitiveFiles.push({ path: filename, bytes: stat.size, contentRead: false });

    const areaStats = areaMap.get(area) || { area, files: 0, bytes: 0, indexedFiles: 0 };
    areaStats.files += 1;
    areaStats.bytes += stat.size;
    if (decision.include) areaStats.indexedFiles += 1;
    areaMap.set(area, areaStats);

    const extensionStats = extensionMap.get(extension) || { extension, files: 0, bytes: 0 };
    extensionStats.files += 1;
    extensionStats.bytes += stat.size;
    extensionMap.set(extension, extensionStats);
  }

  serverInventory.areas = [...areaMap.values()].sort((a, b) => b.bytes - a.bytes);
  serverInventory.extensions = [...extensionMap.values()].sort((a, b) => b.files - a.files);
  serverInventory.largestFiles = [...serverInventory.files]
    .sort((a, b) => b.bytes - a.bytes)
    .slice(0, 25)
    .map(({ path: filePath, area, extension, bytes }) => ({ path: filePath, area, extension, bytes }));
  const isaacLabRoot = path.join(serverBackupSourceDir, 'IsaacLab');
  serverInventory.isaacLab = fs.existsSync(isaacLabRoot) ? {
    role: 'vendored_dependency_not_added_to_corpus',
    commit: safeGit(['-C', isaacLabRoot, 'rev-parse', 'HEAD']),
    description: safeGit(['-C', isaacLabRoot, 'describe', '--tags', '--always', '--dirty']),
  } : null;

  const importantFiles = [
    ['training/README.md', '예선 학습·플레이·제출 전체 흐름'],
    ['training/PRELIM_RL_GUIDE.md', '강화학습 평가 방식과 보상 튜닝 가이드'],
    ['training/FINALS_GUIDE.md', '본선 경기 규칙과 전략 가이드'],
    ['training/humanoid/humanoid_rewards.py', 'H1 보상 가중치 편집 지점'],
    ['training/humanoid/h1_task/env_cfg.py', 'H1 환경·지형·종료 조건 구성'],
    ['training/humanoid/h1_task/agent_cfg.py', 'H1 PPO 네트워크와 러너 구성'],
    ['training/quadruped/quadruped_rewards.py', 'Go2 보상 가중치 편집 지점'],
    ['training/quadruped/go2_task/env_cfg.py', 'Go2 환경·지형·종료 조건 구성'],
    ['training/quadruped/go2_task/agent_cfg.py', 'Go2 PPO 네트워크와 러너 구성'],
    ['practice_sim/practice_sim.py', '연습 경기 실행 진입점과 정책 로딩'],
    ['practice_sim/engine.py', '시뮬레이션·로봇·센서·게임 통합 엔진'],
    ['practice_sim/game_agent.py', '전략 해석과 큐브 선택 에이전트'],
    ['practice_sim/path_planner.py', '지형별 경로 계획과 A* 라우팅'],
    ['practice_sim/grid_nav.py', '점유 격자와 A* 탐색'],
    ['practice_sim/waypoint_controller.py', '월드 좌표 waypoint를 속도 명령으로 변환'],
    ['practice_sim/observation.py', '정책 입력 관측 벡터 구성'],
    ['practice_sim/backend_client.py', '운영 백엔드 통신 클라이언트'],
    ['practice_sim/strategy.txt', '현재 연습용 로봇·정책·자연어 전략 카드'],
  ].filter(([filename]) => fs.existsSync(path.join(serverBackupSourceDir, ...filename.split('/'))));

  const legacyPairs = [
    ['backend_client.py.txt', 'practice_sim/backend_client.py'],
    ['cube_game.txt', 'practice_sim/cube_game.py'],
    ['engine.txt', 'practice_sim/engine.py'],
    ['game agent.txt', 'practice_sim/game_agent.py'],
    ['grid nav.txt', 'practice_sim/grid_nav.py'],
    ['height scanner.txt', 'practice_sim/height_scanner.py'],
    ['observation.txt', 'practice_sim/observation.py'],
    ['particles.py', 'practice_sim/particles.py'],
    ['path_planner.py', 'practice_sim/path_planner.py'],
    ['practice_sim.py', 'practice_sim/practice_sim.py'],
    ['strategy.txt', 'practice_sim/strategy.txt'],
    ['waypoint_controller.py', 'practice_sim/waypoint_controller.py'],
  ];
  const legacyComparison = legacyPairs.flatMap(([legacyPath, backupPath]) => {
    const legacyFullPath = path.join(codeSourceDir, ...legacyPath.split('/'));
    const backupFullPath = path.join(serverBackupSourceDir, ...backupPath.split('/'));
    if (!fs.existsSync(legacyFullPath) || !fs.existsSync(backupFullPath)) return [];
    const legacyHash = crypto.createHash('sha256').update(fs.readFileSync(legacyFullPath)).digest('hex');
    const backupHash = crypto.createHash('sha256').update(fs.readFileSync(backupFullPath)).digest('hex');
    return [{ legacyPath: `data/raw/codebase/${legacyPath}`, backupPath, identical: legacyHash === backupHash }];
  });

  for (const filename of serverInventory.selectedFiles) {
    const sourcePath = path.join(serverBackupSourceDir, ...filename.split('/'));
    const content = fs.readFileSync(sourcePath, 'utf8').replace(/\r\n/g, '\n');
    const language = serverLanguage(filename, content);
    const area = serverArea(filename);
    const id = `server-${sha1(filename).slice(0, 12)}`;
    const processedPath = serverProcessedPath(filename, area);
    fs.mkdirSync(path.dirname(processedPath), { recursive: true });
    const markdown = [
      '---',
      `id: ${id}`,
      'source_type: server_backup',
      `area: ${area}`,
      `language: ${language}`,
      `source: ${JSON.stringify(relative(sourcePath))}`,
      '---',
      '',
      `# ${filename}`,
      '',
      `\`\`\`${language === 'text' ? '' : language}`,
      content,
      '\`\`\`',
      '',
    ].join('\n');
    fs.writeFileSync(processedPath, markdown, 'utf8');
    addDocument({
      id,
      sourceType: 'server_backup',
      area,
      title: filename,
      source: relative(sourcePath),
      processed: relative(processedPath),
      content,
      language,
      lineCount: content ? content.split('\n').length : 0,
    }, { code: language === 'python', language });
  }

  const totalBytes = serverInventory.files.reduce((sum, file) => sum + file.bytes, 0);
  const indexedBytes = serverInventory.files.filter((file) => file.corpusIncluded).reduce((sum, file) => sum + file.bytes, 0);
  const overview = [
    '# 서버 워크스페이스 백업 분석',
    '',
    '## 결론',
    '',
    '- 이 백업은 학습 완료 모델이 아니라 IsaacLab 개발 환경과 대회용 소스·3D 자산의 스냅샷이다.',
    '- 실제 작성·운영 범위는 `training`, `practice_sim`, `examples`이고 `IsaacLab`은 벤더 프레임워크로 분리한다.',
    '- `.pt`, `.onnx`, 학습 체크포인트, 제출 정책, 실행 MP4는 발견되지 않았다.',
    '- `practice_key.bin`과 `.env*`는 이름·크기만 기록했으며 내용을 읽거나 코퍼스에 넣지 않았다.',
    '',
    '## 규모',
    '',
    `- 전체: ${serverInventory.files.length}개 파일, ${(totalBytes / 1024 / 1024).toFixed(2)} MiB`,
    `- AI 코퍼스 포함: ${serverInventory.selectedFiles.length}개 텍스트 파일, ${(indexedBytes / 1024 / 1024).toFixed(2)} MiB`,
    `- IsaacLab 벤더 소스: ${serverInventory.areas.find((item) => item.area === 'vendored_isaaclab')?.files || 0}개 파일`,
    `- 민감 이름 후보: ${serverInventory.sensitiveFiles.length}개(본문 미수집)`,
    '',
    '## 실제 시스템 흐름',
    '',
    '1. `training/*/train.py`가 IsaacLab ManagerBasedRLEnv와 RSL-RL PPO로 H1 또는 Go2를 학습한다.',
    '2. 학생의 핵심 편집 지점은 `humanoid_rewards.py`와 `quadruped_rewards.py`의 `REWARD_WEIGHTS`다.',
    '3. `play.py`가 체크포인트를 검증하고 제출·연습용 TorchScript `policy.pt`를 내보내도록 설계되어 있다.',
    '4. `practice_sim.py`가 전략 카드와 정책을 읽고 `engine.py`에 로봇·맵·게임을 구성한다.',
    '5. 전략 해석/큐브 선택 → 지형별 경로 계획 → waypoint 속도 명령 → 학습 정책 → 로봇 관절 동작 순으로 실행된다.',
    '6. 점수는 큐브 +100, 낙상 -50, 차량 충돌 -30이며 연습 제한 시간 기본값은 180초다.',
    '',
    '## 핵심 파일',
    '',
    ...importantFiles.map(([filename, description]) => `- \`${filename}\`: ${description}`),
    '',
    '## 기존 수집 코드와의 관계',
    '',
    `- 이름을 대응할 수 있는 ${legacyComparison.length}개 중 ${legacyComparison.filter((item) => item.identical).length}개는 완전히 동일하다.`,
    `- 서버판과 달라진 파일: ${legacyComparison.filter((item) => !item.identical).map((item) => `\`${item.backupPath}\``).join(', ') || '없음'}`,
    '- 중복 파일은 양쪽 원본을 모두 보존하되, 현재 서버 상태를 묻는 질문에는 `server_backup` 쪽을 우선한다.',
    '',
    '## 보존·제외 원칙',
    '',
    '- 원본 tar와 추출본은 `data/raw/server_backup`에 그대로 둔다.',
    '- USD/USDZ, 이미지, ETLI 스트리밍 추적, Git 객체는 검색 본문에서 제외하고 인벤토리에만 남긴다.',
    '- 추출 시 절대 경로 `/isaac-sim`을 가리키던 `IsaacLab/_isaac_sim` 심볼릭 링크는 안전상 제외했다.',
    '- 3D 자산의 장면·지형 해석은 별도 시각/영상 분석 대상으로 취급한다.',
    '',
  ].join('\n');
  fs.writeFileSync(path.join(output.serverReports, 'OVERVIEW.md'), overview, 'utf8');

  const inventoryOutput = {
    schemaVersion: 1,
    generatedAt: new Date().toISOString(),
    source: relative(serverBackupSourceDir),
    extractionNotes: {
      sourceArchive: 'data/raw/server_backup/workspace-backupz.tar',
      excludedArchiveEntry: 'IsaacLab/_isaac_sim',
      exclusionReason: 'absolute symlink target /isaac-sim',
    },
    counts: {
      files: serverInventory.files.length,
      bytes: totalBytes,
      corpusIncludedFiles: serverInventory.selectedFiles.length,
      corpusIncludedBytes: indexedBytes,
      sensitiveFilesExcluded: serverInventory.sensitiveFiles.length,
    },
    isaacLab: serverInventory.isaacLab,
    areas: serverInventory.areas,
    extensions: serverInventory.extensions,
    largestFiles: serverInventory.largestFiles,
    sensitiveFiles: serverInventory.sensitiveFiles,
    legacyCodebaseComparison: legacyComparison,
    files: serverInventory.files,
  };
  fs.writeFileSync(path.join(output.serverCatalog, 'inventory.json'), JSON.stringify(inventoryOutput, null, 2), 'utf8');
}

const externalServerAnalysis = {
  documents: 0,
  archiveManifestEntries: 0,
};
const externalDeepAnalysisSource = path.join(externalServerAnalysisDir, 'workspace_backup_deep_analysis.md');
const externalGameEngineAnalysisSource = path.join(externalServerAnalysisDir, 'game_engine_full_analysis.md');
const externalArchiveManifestSource = path.join(externalServerAnalysisDir, 'workspace_backup_manifest.txt');
let externalDeepAnalysisContent = null;
let externalGameEngineAnalysisContent = null;

if (fs.existsSync(externalDeepAnalysisSource)) {
  const content = fs.readFileSync(externalDeepAnalysisSource, 'utf8').replace(/\r\n/g, '\n');
  externalDeepAnalysisContent = content;
  const processedPath = path.join(output.serverReports, 'EXTERNAL_DEEP_ANALYSIS.md');
  fs.writeFileSync(processedPath, content, 'utf8');
  addDocument({
    id: 'external-server-backup-deep-analysis',
    sourceType: 'external_analysis',
    title: '서버 워크스페이스 외부 심층 분석',
    source: relative(externalDeepAnalysisSource),
    processed: relative(processedPath),
    content,
    language: 'markdown',
    provenance: 'user_provided_external_analysis',
  });
  externalServerAnalysis.documents += 1;
}

if (fs.existsSync(externalGameEngineAnalysisSource)) {
  const content = fs.readFileSync(externalGameEngineAnalysisSource, 'utf8').replace(/\r\n/g, '\n');
  externalGameEngineAnalysisContent = content;
  const processedPath = path.join(output.serverReports, 'GAME_ENGINE_FULL_ANALYSIS.md');
  fs.writeFileSync(processedPath, content, 'utf8');
  addDocument({
    id: 'external-game-engine-full-analysis',
    sourceType: 'external_analysis',
    title: 'NAVER CONNECT Robotics Cup 경기 엔진 전체 분석',
    source: relative(externalGameEngineAnalysisSource),
    processed: relative(processedPath),
    content,
    language: 'markdown',
    provenance: 'user_provided_external_analysis',
  });
  externalServerAnalysis.documents += 1;
}

if (externalDeepAnalysisContent || externalGameEngineAnalysisContent) {
  const localOverviewPath = path.join(output.serverReports, 'OVERVIEW.md');
  const localOverview = fs.existsSync(localOverviewPath) ? fs.readFileSync(localOverviewPath, 'utf8').trim() : '';
  const unified = [
    '# 통합 서버 백업 분석',
    '',
    '이 문서는 로컬 구조화 분석과 사용자가 제공한 외부 심층 분석을 한 파일로 합친 것이다.',
    '충돌할 경우 원본 코드·인벤토리를 우선하고, 외부 분석의 추론은 해당 문맥과 한계를 함께 유지한다.',
    '',
    '---',
    '',
    localOverview,
    '',
    '---',
    '',
    ...(externalDeepAnalysisContent ? [
      '# 외부 심층 분석 원문',
      '',
      externalDeepAnalysisContent,
      '',
      '---',
      '',
    ] : []),
    ...(externalGameEngineAnalysisContent ? [
      '# 경기 엔진 전체 분석 원문',
      '',
      externalGameEngineAnalysisContent,
      '',
    ] : []),
  ].join('\n');
  fs.writeFileSync(path.join(output.serverReports, 'UNIFIED_ANALYSIS.md'), unified, 'utf8');
}

if (fs.existsSync(externalArchiveManifestSource)) {
  const content = fs.readFileSync(externalArchiveManifestSource, 'utf8').replace(/\r\n/g, '\n').trim();
  const rows = content.split('\n').filter(Boolean).map((line, index) => {
    const [type, bytes, modifiedAt, ...pathParts] = line.split('\t');
    return {
      id: `archive-entry-${String(index + 1).padStart(4, '0')}`,
      entryType: ({ f: 'file', d: 'directory', l: 'symlink' })[type] || type,
      bytes: Number(bytes),
      modifiedAt,
      path: pathParts.join('\t'),
    };
  });
  writeJsonl(path.join(output.serverCatalog, 'external_archive_manifest.jsonl'), rows);
  addDocument({
    id: 'external-server-backup-archive-manifest',
    sourceType: 'archive_manifest',
    title: '서버 백업 tar 전체 엔트리 목록',
    source: relative(externalArchiveManifestSource),
    processed: 'data/processed/server_backup/catalog/external_archive_manifest.jsonl',
    content,
    language: 'tsv',
    provenance: 'user_provided_external_analysis',
    entryCount: rows.length,
  });
  externalServerAnalysis.documents += 1;
  externalServerAnalysis.archiveManifestEntries = rows.length;
}

const planningDefinitions = [
  {
    filename: 'NCRC2026_solution_blueprint.md',
    id: 'planning-solution-blueprint',
    category: 'implementation_blueprint',
    processedName: '01_SOLUTION_BLUEPRINT.md',
    title: 'NCRC 2026 정책·본선 전략 구현 청사진',
    purpose: '정책 평가기, 보상 튜닝, 체크포인트 선택, 전략 계층의 전체 개발 로드맵',
  },
  {
    filename: '예선_대비_개인서버_검증환경_설계.md',
    id: 'planning-private-validation-environment',
    category: 'validation_environment_design',
    processedName: '02_PRIVATE_SERVER_VALIDATION_DESIGN.md',
    title: '예선 대비 개인 NVIDIA 서버 검증환경 설계안',
    purpose: 'H1·Go2 proxy evaluator, metric collector, batch runner의 구현 명세',
  },
  {
    filename: 'NCRC_예선_개인_NVIDIA_서버_운영안.md',
    id: 'planning-nvidia-server-operations',
    category: 'server_operations',
    processedName: '03_NVIDIA_SERVER_OPERATIONS.md',
    title: '예선 대비 개인 NVIDIA 서버 운영안',
    purpose: '공식 학습 서버와 개인 검증 서버의 역할 분리 및 반복 실험 운영 절차',
  },
];

const planningDocuments = [];
for (const definition of planningDefinitions) {
  const sourcePath = path.join(planningSourceDir, definition.filename);
  if (!fs.existsSync(sourcePath)) continue;
  const rawContent = fs.readFileSync(sourcePath, 'utf8').replace(/\r\n/g, '\n');
  const trustNotice = [
    '> [!IMPORTANT]',
    '> 이 문서는 사용자가 제공한 대회 준비 설계·권장안이다. 백업 코드에서 확인한 값과 구현 제안이 섞여 있다.',
    '> 코드 사실은 현재 서버 백업으로 교차검증하고, 대회 시간·허용 범위·제출 규정·Isaac 버전은 최신 공식 공지를 우선한다.',
    '',
  ].join('\n');
  const content = `${trustNotice}${rawContent}`;
  // 01-03 are historical source conversions; do not overwrite manually curated
  // canonical historical copies or compatibility stubs in planning/.
  const processedPath = path.join(output.planningGenerated, definition.processedName);
  const markdown = [
    '---',
    `id: ${definition.id}`,
    'source_type: planning_analysis',
    `category: ${definition.category}`,
    'trust_level: mixed_code_confirmed_facts_and_recommendations',
    `source: ${JSON.stringify(relative(sourcePath))}`,
    '---',
    '',
    content,
  ].join('\n');
  fs.writeFileSync(processedPath, markdown, 'utf8');
  addDocument({
    id: definition.id,
    sourceType: 'planning_analysis',
    category: definition.category,
    title: definition.title,
    purpose: definition.purpose,
    source: relative(sourcePath),
    processed: relative(processedPath),
    content,
    language: 'markdown',
    trustLevel: 'mixed_code_confirmed_facts_and_recommendations',
  });
  planningDocuments.push({ ...definition, source: relative(sourcePath), processed: relative(processedPath) });
}

const planningIndex = [
  '# 대회 준비 전략·검증·서버 운영 자료',
  '',
  '## 분류',
  '',
  ...planningDocuments.map((document) => `- [${document.title}](./${document.processedName}): ${document.purpose}`),
  '',
  '## 읽는 순서',
  '',
  '1. 구현 청사진으로 전체 우선순위와 평가 기준을 정한다.',
  '2. 검증환경 설계안으로 evaluator와 metric을 구현한다.',
  '3. 서버 운영안으로 정책 버전·실험·영상·결과 기록 절차를 고정한다.',
  '',
  '## 신뢰 규칙',
  '',
  '- `백업 확인` 또는 코드 상수는 현재 `training`·`practice_sim` 원본과 교차검증한다.',
  '- `권장`, 예시 score, curriculum, 시간 배분은 실행 제안이며 공식 규정이 아니다.',
  '- 학습 가능 장소, 제출 조건, 총 GPU 시간, Isaac Sim 버전은 최신 대회 공식 공지를 우선한다.',
  '- credential, practice key, backend 정보는 외부 AI나 공개 저장소에 제공하지 않는다.',
  '',
].join('\n');
// This generator owns only _generated outputs. Preserve hand-curated INDEX.md.
fs.writeFileSync(path.join(output.planningGenerated, 'INDEX.md'), planningIndex, 'utf8');

const deduplicatedVideoRequests = [...new Map(videoRequests.map((request) => [request.requestId, request])).values()];
const deduplicatedImageRequests = [...new Map(imageRequests.map((request) => [request.localSource || request.imageReference, request])).values()];
const analyzableImageRequests = deduplicatedImageRequests.filter((request) => request.sourceExists !== false);
const missingImageRequests = deduplicatedImageRequests.filter((request) => request.sourceExists === false);
writeJsonl(path.join(output.external, 'video_analysis_requests.jsonl'), deduplicatedVideoRequests);
writeJsonl(path.join(output.external, 'image_analysis_requests.jsonl'), deduplicatedImageRequests);
// This generator owns only _generated outputs. Preserve hand-curated README.md.
fs.writeFileSync(path.join(output.externalGenerated, 'README.md'), [
  '# 외부 분석 요청',
  '',
  '[video_analysis_requests.jsonl](../video_analysis_requests.jsonl)의 각 행을 영상 분석 전문 AI에 전달합니다.',
  '결과는 같은 `requestId`를 유지한 JSONL로 받아야 강의 문서와 다시 결합할 수 있습니다.',
  '',
  '필수 결과 필드: `requestId`, `summary`, `timestamped_scenes`, `technical_concepts`,',
  '`visible_code_or_commands`, `procedures`, `warnings`.',
  '',
  '[image_analysis_requests.jsonl](../image_analysis_requests.jsonl)은 강의 이미지 분석 요청입니다. `localSource`가 있는 파일을',
  '이미지 분석 전문 AI에 전달하고 같은 `requestId`로 결과를 받습니다.',
  '`status`가 `missing_source_file`인 항목은 실제 파일이 없으므로 분석 대상에서 제외합니다.',
  '',
].join('\n'), 'utf8');

const manifest = {
  schemaVersion: 1,
  generatedAt: new Date().toISOString(),
  generator: {
    script: 'tools/build_knowledge_base.js',
    scriptSha256: crypto.createHash('sha256').update(fs.readFileSync(__filename)).digest('hex'),
    requiredInputs: requiredInputs.map(([name, source]) => ({ name, path: relative(source) })),
    optionalSourcePresence: {
      serverBackup: fs.existsSync(serverBackupSourceDir),
      externalServerAnalysis: fs.existsSync(externalServerAnalysisDir),
      planning: fs.existsSync(planningSourceDir),
    },
    mode: 'full_non_atomic',
    automaticPrune: false,
  },
  project: 'NAVER CONNECT Robotics / Isaac Sim knowledge base',
  paths: {
    raw: '../naver-issacsim-originals/data/raw',
    processed: 'data/processed',
    serverBackupOverview: 'data/processed/server_backup/reports/OVERVIEW.md',
    unifiedServerBackupAnalysis: 'data/processed/server_backup/reports/UNIFIED_ANALYSIS.md',
    gameEngineAnalysis: 'data/processed/server_backup/reports/GAME_ENGINE_FULL_ANALYSIS.md',
    serverBackupInventory: 'data/processed/server_backup/catalog/inventory.json',
    externalArchiveManifest: 'data/processed/server_backup/catalog/external_archive_manifest.jsonl',
    planningIndex: 'data/processed/planning/_generated/INDEX.md',
    externalGeneratedReadme: 'data/processed/external_analysis/_generated/README.md',
    externalVideoRequests: 'data/processed/external_analysis/video_analysis_requests.jsonl',
    externalImageRequests: 'data/processed/external_analysis/image_analysis_requests.jsonl',
  },
  counts: {
    lectures: lessonFiles.length,
    glossaryTermsExtracted: glossaryTerms.length,
    glossaryTermsDeclaredByPage: declaredGlossaryCount,
    codebaseFiles: codeFiles.length,
    serverBackupFiles: serverInventory.files.length,
    serverBackupIndexedFiles: serverInventory.selectedFiles.length,
    serverBackupSensitiveFilesExcluded: serverInventory.sensitiveFiles.length,
    externalAnalysisDocuments: externalServerAnalysis.documents,
    externalArchiveManifestEntries: externalServerAnalysis.archiveManifestEntries,
    planningDocuments: planningDocuments.length,
    pendingExternalVideos: deduplicatedVideoRequests.length,
    pendingExternalImages: analyzableImageRequests.length,
    missingExternalImages: missingImageRequests.length,
  },
  outputOwnership: {
    handCuratedUntouched: ['data/processed/planning/INDEX.md', 'data/processed/external_analysis/README.md', 'data/processed/planning/historical/*.md', 'data/processed/planning/01_*.md', 'data/processed/planning/02_*.md', 'data/processed/planning/03_*.md'],
    generatedNavigation: ['data/processed/planning/_generated/INDEX.md', 'data/processed/external_analysis/_generated/README.md'],
    warning: 'Other generated text outputs are still written file-by-file. No automatic pruning or transactional rollback is performed.',
  },
  sourceQuality: {
    lectures: 'complete_saved_pages',
    codebase: 'complete_local_files',
    serverBackup: serverInventory.present ? 'project_text_indexed_binary_vendor_and_sensitive_content_excluded' : 'not_present',
    externalAnalysis: externalServerAnalysis.documents ? 'user_provided_analysis_preserved_and_indexed' : 'not_present',
    planning: planningDocuments.length ? 'user_provided_recommendations_with_trust_labels' : 'not_present',
    glossary: glossaryTerms.length < declaredGlossaryCount ? 'partial_first_saved_page_only' : 'complete',
    videos: deduplicatedVideoRequests.length ? 'metadata_only_pending_external_analysis' : 'none',
    images: missingImageRequests.length ? 'partial_local_files_pending_external_analysis' : 'local_files_pending_external_analysis',
  },
};
// Written at the end only: earlier failure must not produce a new completed manifest.
// This is a build receipt, not proof of external raw-archive integrity or atomic output replacement.
fs.writeFileSync(path.join(processedRoot, 'build_manifest.json'), JSON.stringify(manifest, null, 2) + '\n', 'utf8');
console.log(JSON.stringify(manifest, null, 2));
