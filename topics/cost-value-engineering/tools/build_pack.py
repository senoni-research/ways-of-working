"""Deterministic, standard-library builder. No network, source execution or hosting."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode=True

class PackError(ValueError):pass

def read(p:Path)->str:return p.read_text(encoding="utf-8")
def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def dump(obj)->str:return json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
def available_files(root:Path):
    return sorted(p for p in root.rglob('*') if p.is_file() and not any(x in {'__pycache__','.git','.pytest_cache'} for x in p.parts) and p.suffix!='.pyc' and p.name not in {'MANIFEST.json','EXECUTION_REPORT.txt','.DS_Store'})

def canonical(root:Path):
    m=json.loads(read(root/'canonical/metadata.json'))
    mods={p.stem:read(p) for p in sorted((root/'canonical/modules').glob('*.md'))}
    recipe_files=sorted((root/'canonical/recipes').glob('*.md'))
    recipe_ids=[p.stem.split('-')[0] for p in recipe_files]
    if len(recipe_ids)!=len(set(recipe_ids)):raise PackError('recipes: duplicate canonical ID')
    rec={p.stem.split('-')[0]:(p.name,read(p)) for p in recipe_files}
    src=json.loads(read(root/'canonical/sources.json'))
    cases=json.loads(read(root/'canonical/cases/cases.json'))
    def match(actual,expected,label):
        if len(actual)!=len(set(actual)) or sorted(actual)!=sorted(expected):raise PackError(label+': inventory mismatch')
    match(list(mods),m['module_ids'],'modules');match(list(rec),m['recipe_ids'],'recipes')
    match([s['id'] for s in src],m['source_ids'],'sources');match([c['case_id'] for c in cases],m['case_ids'],'cases')
    for rid,(name,txt) in rec.items():
        if len(txt.split())<80 or not txt.startswith('# '+rid+' '):raise PackError('recipe-content: empty, truncated or invalid heading: '+rid)
    b=re.findall(r'^\| (B\d{2}) \|',mods['70-evaluation'],re.M)
    match(b,m['behavior_ids'],'behaviors')
    match(re.findall(r'^## (T\d{2}) ',mods['80-templates-and-prompts'],re.M),m['template_ids'],'templates')
    match(re.findall(r'^## (P\d{2}) ',mods['80-templates-and-prompts'],re.M),m['prompt_ids'],'prompts')
    for c in cases:
        if c.get('synthetic') is not True:raise PackError('case-contract: only synthetic records permitted')
        if not (root/'canonical/cases'/c['source_sheet']).is_file():raise PackError('case-source: missing packet')
    return m,mods,rec,src,cases

def source_text(src):
    t=['# Public sources and inspection limits','',
       'Independently attributed sources. Inspection recorded 8 October 2026; not a claim of full review, code execution, endorsement or redistributed rights. Detailed rules and examples not specified in a source are Senoni implementation choices.','']
    for s in src:
        t += [f'<a id="{s["id"].lower()}"></a>',f'## {s["id"]} — {s["title"]}','',
              '**Authors:** '+', '.join(s['authors'])+'.',
              '**Publication/version:** '+str(s.get('date') or 'not established')+'.',
              f'**Source:** [{s["title"]}]({s["url"]})',
              '**Inspected:** '+s['scope'],
              '**Use here:** '+s['role'],
              '**Limit:** '+s['note'],'']
    return '\n'.join(t).strip()+'\n'

def render(root:Path)->dict[str,bytes]:
    m,mods,rec,src,cases=canonical(root);out={};source_ids={s['id'] for s in src}
    def put(path,t):out[path]=(t.strip()+'\n').encode()
    def resolve(txt,style,depth=0):
        def link(mt):
            key=mt.group(1)
            if key in source_ids:
                dest=('#'+key.lower()) if style=='book' else ('../' if depth else '')+'90-sources.md#'+key.lower()
            elif key in mods:
                dest=('#mod-'+key) if style=='book' else ('../' if depth else '')+key+'.md'
            elif key in rec:
                dest=('#'+key.lower()) if style=='book' else ('' if depth else 'recipes/')+rec[key][0]
            else:raise PackError('source-reference: unknown reference '+key)
            return f'[{key}]({dest})'
        return re.sub(r'\[\[([^\]]+)\]\]',link,txt)
    body=[]
    for key,txt in mods.items():body += [f'<a id="mod-{key}"></a>\n\n'+resolve(txt,'book')]
    for key,(name,txt) in rec.items():body += [f'<a id="{key.lower()}"></a>\n\n'+resolve(txt,'book')]
    body.append(source_text(src))
    body='\n\n---\n\n'.join(body)
    for host,book in [('cursor','cursor.md'),('portable','memory.md')]:
        pre=read(root/f'canonical/prefaces/{host}.md');put(book,pre+'\n\n---\n\n'+body)
        prefix=host+'-project/'
        put(prefix+book,pre+'\n\n---\n\n'+body)
        for key,txt in mods.items():put(prefix+'.costvalue/'+key+'.md',resolve(txt,'module'))
        for key,(name,txt) in rec.items():put(prefix+'.costvalue/recipes/'+name,resolve(txt,'module',1))
        put(prefix+'.costvalue/90-sources.md',source_text(src))
        put(prefix+'.costvalue/README.md','# Cost & Value Engineering\n\nStart with [operating contract](00-operating-contract.md) and [workflow](10-workflow.md). Read only relevant recipes. [Sources](90-sources.md).\n\nSynthetic reference arithmetic is in `reference/`; [case packets](cases/README.md) are public regression examples, not blind tests. No live-agent or industrial validation is claimed.')
        for p in sorted((root/'canonical/cases').iterdir()):out[prefix+'.costvalue/cases/'+p.name]=p.read_bytes()
        for p in sorted((root/'reference').glob('*.py')):out[prefix+'.costvalue/reference/'+p.name]=p.read_bytes()
        out[prefix+'LICENSE']=(root/'LICENSE').read_bytes()
        put(prefix+'README.md',f'# {host.title()} project pack\n\nMerge `.costvalue/` and '+('`.cursor/rules/20-costvalue-method.mdc`' if host=='cursor' else 'the supplied `AGENTS.md` section')+' into the working project. Preserve existing files. Do not install both alternative loaders.\n\nRead the complete ['+book+']('+book+') as a reference, not always-loaded context. Start with [.costvalue/10-workflow.md](.costvalue/10-workflow.md). Check actual loading in a fresh session. [Attribution](.costvalue/90-sources.md). No source publications or customer records are included.')
    loader=read(root/'canonical/loader.md')
    put('cursor-project/.cursor/rules/20-costvalue-method.mdc','---\ndescription: Cost and value engineering, part evidence and supplier quote review\nalwaysApply: true\n---\n\n'+loader)
    put('portable-project/AGENTS.md','<!-- BEGIN COSTVALUE -->\n'+loader+'\n<!-- END COSTVALUE -->')
    put('portable-project/optional-adapters/.clinerules/20-costvalue.md',loader)
    put('portable-project/optional-adapters/README.md','# Alternative Cline loader\n\nCopy `.clinerules/20-costvalue.md` to the project root only instead of the supplied AGENTS section. The `.costvalue/` modules must still be merged. Do not install duplicate active entry routes.')
    for p in sorted((root/'canonical/pages').glob('*.md')):put(p.name,read(p))
    for p in sorted((root/'canonical/cases').iterdir()):out['cases/'+p.name]=p.read_bytes()
    put('SOURCE_REGISTER.md',source_text(src));put('SOURCE_REGISTER.json',dump(src));put('VERSION',m['version'])
    return out

def manifest(root:Path,outputs:dict[str,bytes]|None=None):
    m,mods,rec,src,cases=canonical(root)
    current={str(p.relative_to(root)):p.read_bytes() for p in available_files(root)}
    if outputs:current.update(outputs)
    words=lambda b:len(b.decode('utf-8').split())
    return {'version':m['version'],'date':m['date'],'counts':{'modules':len(mods),'recipes':len(rec),'sources':len(src),'cases':len(cases),'behaviors':len(m['behavior_ids']),'templates':len(re.findall(r'^## T\d{2} ',mods['80-templates-and-prompts'],re.M)),'prompts':len(re.findall(r'^## P\d{2} ',mods['80-templates-and-prompts'],re.M))},
        'files':{k:{'bytes':len(v),'sha256':sha(v),**({'words':words(v)} if k.endswith(('.md','.mdc')) else {})} for k,v in sorted(current.items())}}

def main():
    a=argparse.ArgumentParser();a.add_argument('root',nargs='?',default='.');a.add_argument('--check',action='store_true');args=a.parse_args();root=Path(args.root).resolve()
    try:
        outputs=render(root)
        changes=[k for k,v in outputs.items() if not (root/k).is_file() or (root/k).read_bytes()!=v]
        expected_manifest=dump(manifest(root,outputs)).encode()
        mismatch=not (root/'MANIFEST.json').is_file() or (root/'MANIFEST.json').read_bytes()!=expected_manifest
        if args.check:
            if changes or mismatch:raise PackError('generated-drift: '+', '.join(changes[:5]+(['MANIFEST.json'] if mismatch else [])))
            print('BUILD CHECK PASSED');return
        for k,v in outputs.items():
            p=root/k;p.parent.mkdir(parents=True,exist_ok=True)
            if not p.is_file() or p.read_bytes()!=v:p.write_bytes(v)
        (root/'MANIFEST.json').write_bytes(dump(manifest(root)).encode())
        print(f'Built {len(outputs)} generated artifacts; {len(changes)} changed.')
    except (PackError,ValueError,KeyError,OSError) as e:print('FAIL:',e);sys.exit(1)
if __name__=='__main__':main()
