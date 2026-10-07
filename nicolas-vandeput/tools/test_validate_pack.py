#!/usr/bin/env python3
"""Positive control + exact-target corruption tests with expected diagnostics.

All mutations occur in temporary copies. No source tree changes, no network.
Fixture propagation uses pure rendering to keep unrelated derived artifacts
consistent when testing canonical structural or link invariants.
"""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
from build_pack import render
HERE=Path(__file__).resolve().parent

def run(root):return subprocess.run([sys.executable,'-B',str(root/'tools/validate_pack.py'),str(root)],capture_output=True,text=True,timeout=40)
def snap(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def append(root,path,text):
    p=root/path;p.write_text(p.read_text(encoding='utf-8')+text,encoding='utf-8')
def replace(root,path,old,new):
    p=root/path;t=p.read_text(encoding='utf-8');assert t.count(old)==1,(path,old,t.count(old));p.write_text(t.replace(old,new,1),encoding='utf-8')
def propagate(root):
    for path,data in render(root).items():
        p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
def wrong_manifest(root):
    p=root/'MANIFEST.json';j=json.loads(p.read_text());j['counts']['scenario_count']=0;p.write_text(json.dumps(j))
def false_hashes(root):
    for path in ['cursor.md','memory.md','cursor-project/cursor.md','portable-project/memory.md']:append(root,path,'\nUnsourced extra instruction.\n')
    p=root/'MANIFEST.json';j=json.loads(p.read_text())
    for path in ['cursor.md','memory.md','cursor-project/cursor.md','portable-project/memory.md']:
        b=(root/path).read_bytes();j['generated'][path].update(bytes=len(b),words=len(b.decode().split()),sha256=hashlib.sha256(b).hexdigest())
    p.write_text(json.dumps(j))
def empty_recipes(root):
    for pack in ['cursor-project','portable-project']:
        (root/pack/'.vandeput/recipes/M01-decision-and-risk-horizon.md').write_text('')
def canonical_heading_only(root):
    p=root/'canonical/recipes/M01-decision-and-risk-horizon.md';p.write_text(p.read_text().splitlines()[0]+'\n')
def duplicate_scenario(root):append(root,'canonical/modules/80-worked-examples-and-checks.md','\n| B20 | extra | extra |\n')
def missing_scenario(root):replace(root,'canonical/modules/80-worked-examples-and-checks.md','| B20 |','| BX0 |')
def broken_source_id(root):append(root,'canonical/modules/20-project-workflow.md','\n[[ABSENT99]]\n')
def broken_readme(root):
    append(root,'canonical/pages/README.md','\n[bad](nonexistent.md)\n');propagate(root)
def broken_anchor(root):
    append(root,'canonical/pages/README.md','\n[bad](SOURCE_COVERAGE.md#no-such-anchor)\n');propagate(root)
def bad_loader_target(root):
    append(root,'canonical/loader.md','\nRead `.vandeput/nonexistent.md`.\n');propagate(root)
def bad_source_alias(root):
    p=root/'canonical/sources.json';j=json.loads(p.read_text());next(r for r in j['records'] if r['id']=='R04')['origin_id']='R04';p.write_text(json.dumps(j,ensure_ascii=False));propagate(root)
def corrupted_preface(root):append(root,'canonical/prefaces/cursor.md','\nA new source preface, not rebuilt.\n')
def extra_file(root):(root/'portable-project/.vandeput/recipes/M99-unwanted.md').write_text('# Unexpected rule\n',encoding='utf-8')
def missing_recipe(root):(root/'canonical/recipes/M01-decision-and-risk-horizon.md').unlink()
def missing_module(root):(root/'canonical/modules/20-project-workflow.md').unlink()
def bad_template(root):replace(root,'canonical/modules/85-templates-and-prompts.md','## T01 —','## T00 —')

CASES=[
('canonical content changed; outputs stale',lambda r:append(r,'canonical/modules/20-project-workflow.md','\nNew actual instruction.\n'),'GENERATED_DRIFT','cursor.md'),
('both books edited; hashes refreshed',false_hashes,'GENERATED_DRIFT','cursor.md'),
('pack-local book stale',lambda r:append(r,'cursor-project/cursor.md','\nStale.\n'),'GENERATED_DRIFT','cursor-project/cursor.md'),
('both installed recipes empty',empty_recipes,'GENERATED_DRIFT','recipes/M01'),
('canonical recipe heading-only',canonical_heading_only,'RECIPE_EMPTY','M01'),
('canonical recipe missing',missing_recipe,'RECIPE_INVENTORY',''),
('canonical module missing',missing_module,'MODULE_INVENTORY',''),
('manifest count false',wrong_manifest,'MANIFEST_DRIFT',''),
('B20 missing, other content retained',missing_scenario,'SCENARIO_INVENTORY',''),
('duplicate scenario',duplicate_scenario,'SCENARIO_INVENTORY',''),
('unknown source reference',broken_source_id,'SOURCE_ID','ABSENT99'),
('broken root README link, generated consistently',broken_readme,'BROKEN_LINK','README.md'),
('broken explicit anchor, generated consistently',broken_anchor,'BROKEN_ANCHOR','README.md'),
('loader target missing, generated consistently',bad_loader_target,'LOADER_TARGET','nonexistent'),
('duplicate source origin corrupted',bad_source_alias,'SOURCE_ALIAS',''),
('preface changed without regeneration',corrupted_preface,'GENERATED_DRIFT','cursor.md'),
('extra stale recipe ships',extra_file,'UNEXPECTED_PACK_FILE','M99'),
('template inventory changed',bad_template,'TEMPLATE_INVENTORY',''),
]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',nargs='?',default=str(HERE.parent));a=p.parse_args();src=Path(a.root).resolve()
    before=snap(src)
    control=run(src)
    if control.returncode!=0:
        print('ERROR: positive control failed.\n'+control.stdout+control.stderr);return 2
    print('PASS positive control: unchanged release validates.')
    failures=0
    for label,mutator,code,target in CASES:
        with tempfile.TemporaryDirectory(prefix='vandeput-regression-') as tmp:
            root=Path(tmp)/'pack';shutil.copytree(src,root,ignore=shutil.ignore_patterns('__pycache__','.git'))
            fixture_before=snap(root)
            try:mutator(root)
            except Exception as exc:
                failures+=1;print(f'ERROR mutation {label}: {exc}');continue
            if snap(root)==fixture_before:
                failures+=1;print('ERROR no-op mutation:',label);continue
            response=run(root);output=response.stdout+response.stderr
            if response.returncode!=1 or f'FAIL [{code}]' not in output or target not in output or 'Traceback' in output:
                failures+=1;print(f'FAIL {label}: expected [{code}] {target}; got {response.returncode}: {output[:450]}')
            else:print(f'PASS {label}: [{code}] {target}')
    if snap(src)!=before:print('ERROR source tree content changed during regression tests');return 2
    print(f'REGRESSION RESULT: {len(CASES)-failures}/{len(CASES)} intended diagnostics; source contents unchanged.')
    return 1 if failures else 0
if __name__=='__main__':sys.exit(main())
