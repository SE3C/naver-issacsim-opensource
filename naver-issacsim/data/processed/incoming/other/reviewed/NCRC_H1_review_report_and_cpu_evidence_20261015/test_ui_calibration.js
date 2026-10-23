#!/usr/bin/env node
/* Read ONLY constant and pure-function snippets from the original UI; no browser/network/API.
 * This uses Node's vm for evaluation of reviewed source snippets and writes reproducible fixture calculations.
 */
const fs=require('fs'),vm=require('vm'),path=require('path');
const sourceRoot=process.env.NCRC_SOURCE_DIR||path.join(__dirname,'..','source','ncrc_h1_end_to_end');
const src=fs.readFileSync(path.join(sourceRoot,'index.html'),'utf8');
const code=src.slice(src.indexOf('    const SCENARIOS = [',src.indexOf('<script>')),
                     src.indexOf('    const scenarioRows =',src.indexOf('<script>')));
const pure=src.slice(src.indexOf('    function getScenarioLogDelta('),src.indexOf('    function updateAll()'));
const context={};
vm.runInNewContext(code+'\n'+`const clamp=(n,lo,hi)=>Math.max(lo,Math.min(hi,n));\n`+pure+
  '\nthis.EXPORTED={SCENARIOS,PROFILES,B_EXAMPLE,LOG_ANCHOR,LOG_COEFFS,getScenarioLogDelta,clamp};',context,{timeout:1000});
const {SCENARIOS,PROFILES,B_EXAMPLE,LOG_ANCHOR,getScenarioLogDelta,clamp}=context.EXPORTED;
const emptyLog={enabled:false,terrainLevel:null,fallRatePct:null,explorationStd:null,xyError:null,yawError:null};
function calc(scores,profile,log=emptyLog){
 let raw=0,base=0,final=0;const per=[];
 for(const s of SCENARIOS){
  const x=Number.isFinite(scores[s.id])?clamp(scores[s.id],0,1):0;
  const b=clamp(x+profile.perScenarioDeltaNorm[s.id],0,1),d=getScenarioLogDelta(s.id,log);
  const f=clamp(b+d,0,1);
  raw+=x*s.max;base+=b*s.max;final+=f*s.max;
  per.push({id:s.id,raw:x*s.max,base:b*s.max,final:f*s.max,delta_norm:d});
 }
 return {raw70:raw,base70:base,final70:final,objective:final/70,per};
}
const example={},profiles={};
for(const [id,p] of Object.entries(PROFILES)){
 const c=calc(B_EXAMPLE,p);
 profiles[id]={declared_globalDelta70:p.globalDelta70,actual_example_raw_delta70:c.base70-c.raw70,
  example:c,blank:calc({},p),mean_delta_on_interior:p.perScenarioDeltaNorm && SCENARIOS.reduce((n,s)=>n+p.perScenarioDeltaNorm[s.id]*s.max,0)};
}
const anchorState={enabled:true,terrainLevel:LOG_ANCHOR.terrainLevel,fallRatePct:LOG_ANCHOR.fallRatePct,
 explorationStd:null,xyError:LOG_ANCHOR.xyError,yawError:LOG_ANCHOR.yawError};
const lowFall={...anchorState,fallRatePct:LOG_ANCHOR.fallRatePct};
const higherFall={...anchorState,fallRatePct:35};
const a=Object.fromEntries(SCENARIOS.map(s=>[s.id,0.81])),b=Object.fromEntries(SCENARIOS.map(s=>[s.id,0.80]));
const rank={a:calc(a,PROFILES.term50_official_anchor_5637,higherFall),
            b:calc(b,PROFILES.term50_official_anchor_5637,lowFall)};
// Search a transparent pair of crossing vectors where per-scenario clipping changes order for fixed profile.
let clipReversal=null;
for(let i=0;i<=100&&!clipReversal;i++)for(let j=0;j<=100&&!clipReversal;j++){
 const a=Object.fromEntries(SCENARIOS.map(s=>[s.id,0.5]));
 const b={...a};a.H5=i/100;a.H2=1-j/100;b.H5=0.5;b.H2=0.5;
 const ca=calc(a,PROFILES.term50_official_anchor_5637),cb=calc(b,PROFILES.term50_official_anchor_5637);
 if(ca.raw70>cb.raw70+0.03 && ca.base70<cb.base70-0.03)clipReversal={a_inputs:a,b_inputs:b,a_raw:ca.raw70,b_raw:cb.raw70,a_base:ca.base70,b_base:cb.base70};
}
const result={source:'ZIP index.html pure source constants/formula',scenario_weight_sum:SCENARIOS.reduce((n,s)=>n+s.max,0),
 anchor_target_official70:56.37,anchor_B_calculated:profiles.term50_official_anchor_5637.example,
 profiles,log_at_anchor:calc(B_EXAMPLE,PROFILES.term50_official_anchor_5637,anchorState),
 log_rank_flip:{A_raw:rank.a.raw70,B_raw:rank.b.raw70,A_final:rank.a.final70,B_final:rank.b.final70,
 A_fall_pct:higherFall.fallRatePct,B_fall_pct:lowFall.fallRatePct},clipped_fixed_delta_rank_flip:clipReversal,
 fixed_delta_max_adjustment70:SCENARIOS.reduce((n,s)=>n+s.max*0.05,0)};
fs.writeFileSync(path.join(__dirname,'ui_calibration_results.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify({scenario_weight_sum:result.scenario_weight_sum,anchor_B_calculated:result.anchor_B_calculated,
 profile_global_vs_example:Object.fromEntries(Object.entries(profiles).map(([k,v])=>[k,[v.declared_globalDelta70,v.actual_example_raw_delta70]])),
 log_rank_flip:result.log_rank_flip,clipped_fixed_delta_rank_flip:clipReversal},null,2));
