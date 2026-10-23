// CPU static inspection of delivered UI; no browser, GPU or evaluator execution.
const fs=require('fs');const assert=require('assert');
const html=fs.readFileSync(require('path').join(__dirname,'..','index.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new (require('vm').Script)(script);
assert(script.includes("'/api/ask'"));
assert(script.includes("'/api/record'"));
assert(script.includes("'/api/tell'"));
assert(script.includes("'/api/abandon'"));
assert(!script.includes('tell-and-ask'));
assert(!script.includes('/api/evaluate/start'));
assert(!script.includes('calibrated_proxy_70'));
assert(!script.includes('ncrc_optuna_calibrator.py'));
assert(script.includes("$('value').value=''"));
assert(script.includes('window.confirm'));
console.log('UI syntax, separate endpoints, blank score on trial selection, explicit confirmations: PASS');
