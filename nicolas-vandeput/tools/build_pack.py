#!/usr/bin/env python3
"""Deterministic build of original guide artifacts from canonical inputs.

render(root) is pure with respect to files: it returns expected bytes.
Only main without --check writes them. No downloaded source is executed.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

MODULE_INPUTS = [
 '00-operating-contract.md','10-thirteen-practices.md','20-project-workflow.md',
 '30-forecast-design.md','40-inventory-decisions.md','50-human-value-added.md',
 '60-memory-and-engineering.md','80-worked-examples-and-checks.md',
 '85-templates-and-prompts.md','90-source-interpretation.md','95-source-observations.md']
MUTATION_EXCLUDED = {'__pycache__'}

class PackError(ValueError):
    def __init__(self, code: str, detail: str):
        self.code, self.detail = code, detail
        super().__init__(f'{code}: {detail}')

def read(path: Path) -> str:
    try:return path.read_bytes().decode('utf-8')
    except (OSError,UnicodeError) as exc:raise PackError('INPUT',str(path)) from exc

def sha(payload: bytes) -> str:return hashlib.sha256(payload).hexdigest()
def words(text: str) -> int:return len(re.findall(r'\S+',text))
def load_json(path: Path):
    try:return json.loads(read(path))
    except json.JSONDecodeError as exc:raise PackError('JSON',str(path)) from exc

def source_links(text: str, ids: set[str], destination: str) -> str:
    def repl(match):
        sid=match.group(1)
        if sid not in ids:raise PackError('SOURCE_ID',sid)
        return f'[{sid}]({destination}#{sid.lower()})'
    return re.sub(r'\[\[([A-Z][A-Z0-9-]*)\]\]',repl,text)

def demote(text: str, levels: int=1) -> str:
    result=[]; fence=None
    for line in text.splitlines():
        fm=re.match(r'^\s*(`{3,}|~{3,})',line)
        if fm:
            mark=fm.group(1)
            if fence is None:fence=(mark[0],len(mark))
            elif mark[0]==fence[0] and len(mark)>=fence[1]:fence=None
            result.append(line);continue
        hm=None if fence else re.match(r'^(#{1,6}) (.*)$',line)
        result.append('#'*min(6,len(hm.group(1))+levels)+' '+hm.group(2) if hm else line)
    return '\n'.join(result)+'\n'

def require_ids(found, expected, code):
    if found!=expected:raise PackError(code,f'expected {expected}; found {found}')

def canonical_inputs(root: Path):
    version=read(root/'VERSION').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+',version):raise PackError('VERSION','invalid semver')
    meta=load_json(root/'canonical/metadata.json')
    registry=load_json(root/'canonical/sources.json');records=registry['records']
    ids=[r['id'] for r in records]
    if len(ids)!=len(set(ids)):raise PackError('SOURCE_INVENTORY','duplicate source IDs')
    prim=[r for r in records if re.fullmatch(r'(?:V|P|A|R|D|O)\d{2}|N[12]-\d{2}',r['id'])]
    if len(prim)!=53 or len(set(r['url'] for r in prim))!=52:raise PackError('SOURCE_INVENTORY','expected 53 entries and 52 primary URLs')
    expected=set(MODULE_INPUTS);actual=set(p.name for p in (root/'canonical/modules').glob('*.md'))
    if actual!=expected:raise PackError('MODULE_INVENTORY',str(sorted(actual^expected)))
    modules={name:read(root/'canonical/modules'/name) for name in MODULE_INPUTS}
    for name,body in modules.items():
        if not body.startswith('# '):raise PackError('MODULE_HEADING',name)
    paths=sorted((root/'canonical/recipes').glob('*.md'))
    require_ids([p.name[:3] for p in paths],[f'M{i:02}' for i in range(1,21)],'RECIPE_INVENTORY')
    recipes={p.name:read(p) for p in paths}
    for name,body in recipes.items():
        lines=body.strip().splitlines()
        if not lines or not lines[0].startswith('# '+name[:3]+' — '):raise PackError('RECIPE_HEADING',name)
        content=[l for l in lines[1:] if l.strip() and not re.match(r'^#{1,6} ',l)]
        if not content or words('\n'.join(content))<30:raise PackError('RECIPE_EMPTY',name)
    scenarios=re.findall(r'^\| (B\d{2}) \|',modules['80-worked-examples-and-checks.md'],re.M)
    require_ids(scenarios,[f'B{i:02}' for i in range(1,41)],'SCENARIO_INVENTORY')
    templates=re.findall(r'^## (T\d{2}) — ',modules['85-templates-and-prompts.md'],re.M)
    prompts=re.findall(r'^## (P\d{2}) — ',modules['85-templates-and-prompts.md'],re.M)
    require_ids(templates,[f'T{i:02}' for i in range(1,10)],'TEMPLATE_INVENTORY')
    require_ids(prompts,[f'P{i:02}' for i in range(1,9)],'PROMPT_INVENTORY')
    examples=re.findall(r'^## Example ([A-Z]) — ',modules['80-worked-examples-and-checks.md'],re.M)
    require_ids(examples,list('ABCDEFGHIJ'),'EXAMPLE_INVENTORY')
    counts=dict(module_count=12,recipe_count=20,scenario_count=40,template_count=9,prompt_count=8,example_count=10,primary_count=53,distinct_primary_urls=52)
    for key,val in [('primary_entries',53),('distinct_urls',52),('recipes',20),('scenarios',40),('templates',9),('prompts',8)]:
        if meta.get('expected_'+key)!=val:raise PackError('METADATA_COUNT',key)
    return version,meta,registry,modules,recipes,counts

def source_register_section(records):
    result=['\n## Compact source register\n']
    for r in records:
        sid=r['id']; url=r.get('url','')
        result += [f'<a id="{sid.lower()}"></a>\n',f'### {sid} — {r["title"]}\n',
                   f'**Origin:** {r["creator"]}. **Role:** `{r["role"]}`. **This review:** `{r["status"]}`.\n']
        if url:result.append(f'[Original reference]({url}).\n')
        else:result.append('User-supplied reference; no public canonical URL asserted.\n')
        result.append(r['limits']+'\n')
    return '\n'.join(result)

def coverage(registry):
    lines=['# Download coverage and inspection record\n','Prepared 7 October 2026. This report replaces prior access assumptions with inspection of the supplied archive, without claiming new public availability.\n',
           '**53 catalogue entries / 52 distinct primary URLs.** R04 and N2-07 are one source. Alternate access IDs are aliases, not extra corroboration. No source models, APIs, notebooks or checkpoints were executed.\n',
           'The original catalogue dates and access labels are retained as historical metadata, not independent verification of every source date. Source locators below refer to paths inside the supplied archive; original files are not shipped.\n',
           '**Newly useful access:** three English caption transcripts; sixteen raw notebook files, two Python fragments/scripts, two printed-code PDFs, two snapshot documents; selected contents of two downloaded repositories.\n',
           '**Still limited:** V04 spoken transcript; P02 full Foresight paper; R03 dataset; full discussion threads; A06 external result-table image; one N2-13 EMF visual; uninspected repository internals and complete official simulator environment.\n']
    for r in registry['records']:
        lines += [f'## {r["id"]} — {r["title"]}\n',f'**Role:** `{r["role"]}` · **Inspection:** `{r["status"]}` · **Origin ID:** `{r["origin_id"]}`\n',
                  r['reviewed']+'\n','**Limits:** '+r['limits']+'\n','**Locator:** '+r['locator']+'\n']
        if r.get('url'):lines.append(f'[Canonical reference]({r["url"]})\n')
        for a in r['assets']:lines.append(f'- Archive path: `{a["path"]}`; bytes: {a["bytes"]}; SHA-256: `{a["sha256"]}`.\n')
    lines += ['\n## Alternate-access aliases\n','\n'.join(f'- {k} → {v}' for k,v in registry['alternate_access'].items()),'\n']
    return '\n'.join(lines)

def render(root: Path) -> dict[str, bytes]:
    root=root.resolve()
    version,meta,registry,rawmodules,recipes,counts=canonical_inputs(root)
    ids=set(r['id'] for r in registry['records'])
    rawmodules=dict(rawmodules)
    rawmodules['90-sources.md']=rawmodules.pop('90-source-interpretation.md')+source_register_section(registry['records'])
    recparts=['# 70 — Technical recipes\n\nRead the relevant recipe, not this entire reference for every task. The individual installed files and this reference are generated from the same canonical text. Source mechanisms, participant configurations and Senoni safeguards retain separate attribution.\n']
    for name,body in recipes.items():recparts += [f'\n<a id="{name[:3].lower()}"></a>\n\n',demote(body)]
    rawmodules['70-method-recipes.md']=''.join(recparts)
    rawmodules=dict(sorted(rawmodules.items()))
    counts['module_count']=len(rawmodules)
    modules={name:source_links(body,ids,'90-sources.md' if name!='90-sources.md' else '') for name,body in rawmodules.items()}
    recipe_outputs={name:source_links(body,ids,'../90-sources.md') for name,body in recipes.items()}
    nav='\n'.join(f'- [{body.splitlines()[0][2:]}](#sec-{name[:2]})' for name,body in rawmodules.items())
    parts=[]
    for name,body in rawmodules.items():
        parts.append(f'<a id="sec-{name[:2]}"></a>\n\n'+demote(source_links(body,ids,'')))
    shared='\n---\n\n'.join(parts)
    subs={'VERSION':version,'DATE':meta['prepared'],'NAVIGATION':nav,**{k.upper():str(v) for k,v in counts.items()}}
    def expand(text):
        for key,val in subs.items():text=text.replace('@@'+key+'@@',val)
        if re.search(r'@@[A-Z_]+@@',text):raise PackError('TEMPLATE_TOKEN',text[:50])
        return text
    out={}
    def add(path,text):out[path]=text.encode('utf-8') if isinstance(text,str) else text
    for stem in ('cursor','memory'):
        pre=expand(read(root/'canonical/prefaces'/f'{stem}.md'))
        book=pre.rstrip()+'\n\n'+shared
        if not book.endswith('\n'):book+='\n'
        add(f'{stem}.md',book);subs[stem.upper()+'_WORDS']=str(words(book))
    for p in sorted((root/'canonical/pages').glob('*.md')):add(p.name,expand(read(p)))
    cover=coverage(registry);add('SOURCE_COVERAGE.md',cover)
    add('SOURCE_REVIEW.md',source_links(rawmodules['95-source-observations.md'],ids,'portable-project/.vandeput/90-sources.md'))
    regbytes=(json.dumps(registry,indent=2,ensure_ascii=False)+'\n').encode('utf-8');add('SOURCE_REGISTER.json',regbytes)
    loader=read(root/'canonical/loader.md')
    for pack,stem in [('cursor-project','cursor'),('portable-project','memory')]:
        for name,body in modules.items():add(f'{pack}/.vandeput/{name}',body)
        for name,body in recipe_outputs.items():add(f'{pack}/.vandeput/recipes/{name}',body)
        index='# Select one technical recipe\n\n'+ '\n'.join(f'- [{body.splitlines()[0][2:]}]({name})' for name,body in recipes.items())+'\n'
        add(f'{pack}/.vandeput/recipes/README.md',index)
        add(f'{pack}/.vandeput/loader.md',loader)
        add(f'{pack}/{stem}.md',out[f'{stem}.md'])
        add(f'{pack}/SOURCE_REGISTER.json',regbytes);add(f'{pack}/SOURCE_COVERAGE.md',cover)
        add(f'{pack}/VALIDATION.md',out['VALIDATION.md'])
        for p in sorted((root/'reference').glob('*')):
            if p.is_file() and p.suffix in ('.md','.py'):
                payload=read(p)
                if p.suffix=='.md':payload=payload.replace('../SOURCE_COVERAGE.md','../90-sources.md')
                add(f'{pack}/.vandeput/reference/{p.name}',payload)
        install=('Merge `.vandeput/` and `.cursor/rules/10-vandeput-method.mdc` into your project. Check the rule is active. A plain `cursor.md` is not auto-loaded.' if stem=='cursor' else 'Merge `.vandeput/` and the content of `AGENTS.md` into your project. Optional Cline/OpenCode adapters are alternatives, not duplicate loading routes.')
        add(f'{pack}/README.md',f'# {"Cursor" if stem=="cursor" else "Portable"} Vandeput project pack\n\nVersion {version} · {meta["prepared"]}\n\n{install}\n\nPreserve existing rules and user changes. Keep an existing Carey pack under `.carey/`; this pack uses `.vandeput/`. Use the small entry point and selective reads rather than putting the entire handbook into context.\n\nRead [{stem}.md]({stem}.md) for the complete method, [source coverage](SOURCE_COVERAGE.md) for limits, and [validation](VALIDATION.md) for tests actually run. Source originals and checkpoints are not included.\n\nStart a fresh credential-free session and ask which paths were read, what the thirteen practices imply for the current problem, and how the agent would verify scoring and lost-sales timing. Run relevant B01–B40 scenarios in [.vandeput/80-worked-examples-and-checks.md](.vandeput/80-worked-examples-and-checks.md). No live host behavior is certified.\n\nThe complete methods bundle contains canonical sources and build/validation tools. In a project, review local changes before upgrading; do not overwrite project evidence with a new method release. The arithmetic examples under `.vandeput/reference/` are optional synthetic demonstrations, not trained models or a full challenge simulator.\n')
    add('cursor-project/.cursor/rules/10-vandeput-method.mdc','---\ndescription: Source-grounded demand forecasting and inventory planning method\nalwaysApply: true\n---\n\n'+loader)
    add('portable-project/AGENTS.md',loader)
    add('portable-project/optional-adapters/cline/10-vandeput-method.md',loader)
    add('portable-project/optional-adapters/opencode/opencode.instructions.example.json',json.dumps({'instructions':['.vandeput/loader.md']},indent=2)+'\n')
    inputs={str(p.relative_to(root)):sha(p.read_bytes()) for p in sorted((root/'canonical').rglob('*')) if p.is_file()}
    inputs['VERSION']=sha((root/'VERSION').read_bytes())
    support={str(p.relative_to(root)):sha(p.read_bytes()) for folder in ('tools','reference') for p in sorted((root/folder).glob('*')) if p.is_file() and p.suffix in ('.py','.md')}
    manifest={'version':version,'prepared':meta['prepared'],'counts':counts,'modules':list(modules),'recipes':list(recipes),
              'canonical_sha256':inputs,'support_sha256':support,'generated':{path:{'bytes':len(data),'sha256':sha(data),**({'words':words(data.decode('utf-8'))} if path.endswith(('.md','.mdc')) else {})} for path,data in sorted(out.items())}}
    add('MANIFEST.json',json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',nargs='?',default=str(Path(__file__).resolve().parents[1]));parser.add_argument('--check',action='store_true');args=parser.parse_args()
    root=Path(args.root).resolve()
    try:expected=render(root)
    except (PackError,OSError,KeyError,TypeError) as exc:print(f'FAIL: {exc}',file=sys.stderr);return 1
    changed=[p for p,data in expected.items() if not (root/p).is_file() or (root/p).read_bytes()!=data]
    if args.check:
        for p in changed:print('DRIFT:',p)
        print('BUILD CHECK PASSED' if not changed else 'BUILD CHECK FAILED')
        return bool(changed)
    for p in changed:
        target=root/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(expected[p])
    print(f'Build: {len(expected)} generated artifacts; {len(changed)} changed; {len(expected)-len(changed)} unchanged.')
    return 0
if __name__=='__main__':sys.exit(main())
