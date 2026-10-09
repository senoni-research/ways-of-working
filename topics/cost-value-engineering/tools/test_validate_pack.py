"""Intentional-corruption tests on complete temporary package copies."""
from pathlib import Path
import argparse,json,shutil,tempfile,sys
sys.dont_write_bytecode=True
from build_pack import render,manifest,dump
from validate_pack import validate

def write(p,t):p.write_text(t,encoding='utf8')
def replace(p,a,b):
    t=p.read_text();assert a in t,(p,a);write(p,t.replace(a,b,1))
def rebuild(r):
    for k,v in render(r).items():
        p=r/k;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v)
    write(r/'MANIFEST.json',dump(manifest(r)))
def fresh_manifest(r):write(r/'MANIFEST.json',dump(manifest(r)))
def run(root):
    validate(root)  # An invalid positive control raises before running any negative case.
    def stale(r):replace(r/'canonical/modules/10-workflow.md','First session','First relevant session')
    def books(r):
        for p in [r/'cursor.md',r/'memory.md',r/'cursor-project/cursor.md',r/'portable-project/memory.md']:write(p,p.read_text()+'\nUndocumented manual addition.\n')
        fresh_manifest(r)
    def extract(r):
        for host in ['cursor','portable']:write(next((r/f'{host}-project/.costvalue/recipes').glob('M01-*.md')),'')
        fresh_manifest(r)
    def empty(r):write(next((r/'canonical/recipes').glob('M01-*.md')),'# M01 — Empty\n')
    def extra(r):write(r/'portable-project/.costvalue/rogue.md','# Not an expected installed file\n');fresh_manifest(r)
    def link(r):write(r/'canonical/pages/README.md',(r/'canonical/pages/README.md').read_text()+'\n[Broken](missing-file.md)\n');rebuild(r)
    def loader(r):replace(r/'canonical/loader.md','.costvalue/10-workflow.md','.costvalue/missing.md');rebuild(r)
    def missingcase(r):
        p=r/'canonical/cases/cases.json';a=json.loads(p.read_text());a.pop();write(p,json.dumps(a))
    def source(r):replace(r/'canonical/modules/10-workflow.md','[[CV01]]','[[CV99]]')
    def behavior(r):replace(r/'canonical/modules/70-evaluation.md','| B24 |','| B23 |')
    def hashbad(r):
        p=r/'MANIFEST.json';d=json.loads(p.read_text());d['files']['memory.md']['sha256']='0'*64;write(p,json.dumps(d))
    def countbad(r):
        p=r/'MANIFEST.json';d=json.loads(p.read_text());d['counts']['cases']=400;write(p,json.dumps(d))
    def wordbad(r):
        p=r/'MANIFEST.json';d=json.loads(p.read_text());d['files']['memory.md']['words']+=1;write(p,json.dumps(d))
    def preface(r):write(r/'canonical/prefaces/cursor.md',(r/'canonical/prefaces/cursor.md').read_text()+'\nNew preface text\n')
    def duplicate_recipe(r):shutil.copyfile(next((r/'canonical/recipes').glob('M01-*.md')),r/'canonical/recipes/M01-duplicate.md')
    def duplicate_template(r):replace(r/'canonical/modules/80-templates-and-prompts.md','## T05 ','## T04 ')
    def missing_prompt(r):replace(r/'canonical/modules/80-templates-and-prompts.md','## P04 ','## P99 ')
    def loader_via_symlink(r):
        # Regression for the macOS /var -> /private/var root-resolution fix:
        # the validator must reach the package through a symlinked root and
        # still report the intended loader-target diagnostic (not a spurious
        # link-escape). The runner calls validate(r) afterwards; r itself is
        # replaced by a symlink to the copied tree.
        parent=r.parent
        real=parent/'real-pack'
        shutil.move(str(r),str(real))
        r.symlink_to(real)
        # r is now a symlink; mutate the canonical loader through it.
        t=(real/'canonical/loader.md').read_text()
        (real/'canonical/loader.md').write_text(t.replace('.costvalue/10-workflow.md','.costvalue/missing.md',1))
        rebuild(real)
    specs=[('duplicate canonical recipe ID',duplicate_recipe,'recipes:'),('duplicate template ID',duplicate_template,'templates:'),('missing expected prompt ID',missing_prompt,'prompts:'),('stale canonical source',stale,'canonical-drift:'),('coordinated handbook edits',books,'canonical-drift:'),('empty installed extracts',extract,'canonical-drift:'),('heading-only canonical recipe',empty,'recipe-content:'),('extra installed file',extra,'installed-inventory:'),('broken root link',link,'link:'),('nonexistent loader target',loader,'loader-target:'),('loader target via symlinked root (macOS path fix)',loader_via_symlink,'loader-target:'),('missing case',missingcase,'cases:'),('unknown source ref',source,'source-reference:'),('duplicate behavior ID',behavior,'behaviors:'),('changed hash',hashbad,'manifest:'),('wrong count',countbad,'manifest:'),('wrong word count',wordbad,'manifest:'),('stale preface',preface,'canonical-drift:')]
    for title,mut,diag in specs:
        with tempfile.TemporaryDirectory() as td:
            r=Path(td)/'pack';shutil.copytree(root,r,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            mut(r)
            try:validate(r)
            except Exception as e:
                assert diag in str(e),f'{title}: wrong diagnostic {e!r} expected {diag}'
            else:raise AssertionError(title+': mutation accepted')
            print('PASS:',title,'->',diag)
    print(f'ALL {len(specs)} CORRUPTION REGRESSIONS PASSED; positive control passed.')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('root',nargs='?',default='.');args=a.parse_args();run(Path(args.root).resolve())
