#!/usr/bin/env python3
"""CPU-only schema/evidence inventory for an EXISTING independent evaluation archive.
No assumptions about the user's undocumented Windows evaluator field names.
Does not score, estimate official results, or overwrite input. Parses JSON <= 4MB;
JSONL streaming with no row materialization. Use for schema mapping preflight.
"""
import argparse
import collections
import json
from pathlib import Path
import zipfile


def shape(value):
    if isinstance(value,dict):
        return {'type':'object','keys':sorted(value)[:150]}
    if isinstance(value,list):
        return {'type':'array','length':len(value),
                'first_item':shape(value[0]) if value else None}
    return {'type':type(value).__name__}


def audit(src: Path):
    result={'input_filename':src.name,'file_count':0, 'entries':[],
            'warnings':[], 'important_files':[]}
    with zipfile.ZipFile(src) as z:
        for f in z.infolist():
            if f.is_dir(): continue
            result['file_count']+=1
            name=f.filename
            ext=Path(name).suffix.lower()
            info={'name':name,'size_bytes':f.file_size}
            if ext in ('.json','.jsonl'):
                info['json_kind']=ext
                if ext=='.json' and f.file_size <= 4_000_000:
                    try: info['schema']=shape(json.loads(z.read(f).decode('utf-8-sig')))
                    except (UnicodeDecodeError,ValueError) as e: info['parse_error']=str(e)
                elif ext=='.jsonl':
                    counts=collections.Counter();lines=0;broken=0;first=None
                    with z.open(f) as raw:
                        for b in raw:
                            if not b.strip():continue
                            lines+=1
                            try:
                                x=json.loads(b.decode('utf-8-sig'))
                                if first is None:first=shape(x)
                                if isinstance(x,dict):counts.update(x.keys())
                            except (ValueError,UnicodeDecodeError):broken+=1
                    info['rows']=lines
                    info['invalid_rows']=broken
                    info['first_row_schema']=first
                    info['top_level_field_counts']=dict(counts.most_common(100))
                elif ext=='.json': info['note']='large JSON not parsed (size limit)'
            if any(k in name.lower() for k in ['manifest','diagnostic','episodes','protocol','config']):
                result['important_files'].append(name)
            result['entries'].append(info)
    if not result['important_files']:result['warnings'].append('No obvious manifest/diagnostics/episodes/protocol filenames: inspect manually.')
    result['warnings'].append('Schema discovery only; identity, first-cohort, metric definitions and cross-policy comparability require manual field mapping.')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('input_zip',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    r=audit(args.input_zip)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'files':r['file_count'],'important_files':r['important_files'],
                     'warnings':r['warnings']},ensure_ascii=False,indent=2))
