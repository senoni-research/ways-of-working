"""Read-only canonical validation, not live-agent or industrial validation."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
from urllib.parse import unquote,urlsplit
sys.dont_write_bytecode=True
from build_pack import render,manifest,available_files,PackError,read

def anchors(txt):
    ids=set(re.findall(r'<a\s+id="([^"]+)"',txt));seen={}
    for line in txt.splitlines():
        m=re.match(r'^#{1,6}\s+(.+)',line)
        if m:
            s=re.sub(r'[^\w\- ]','',m.group(1).lower()).replace(' ','-');n=seen.get(s,0);seen[s]=n+1;ids.add(s if not n else f'{s}-{n}')
    return ids

def validate(root:Path):
    root=root.resolve()  # macOS temp dirs symlink /var -> /private/var; compare consistently
    outputs=render(root)
    for rel,data in outputs.items():
        p=root/rel
        if not p.is_file() or p.read_bytes()!=data:raise PackError('canonical-drift: '+rel)
    for group in ['cursor-project','portable-project','cases']:
        actual={str(p.relative_to(root)) for p in available_files(root/group)}
        expected={x for x in outputs if x.startswith(group+'/')}
        if actual!=expected:raise PackError('installed-inventory: '+group)
    # Check generated and root/template documentation, not raw canonical [[tokens]].
    docs=[p for p in available_files(root) if p.suffix in {'.md','.mdc'} and 'canonical' not in p.relative_to(root).parts]
    for p in docs:
        txt=read(p)
        for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^\s)]+)\)',txt):
            if urlsplit(target).scheme or target.startswith('//'):continue
            path,_,anchor=unquote(target).partition('#')
            dest=(p.parent/path).resolve() if path else p
            if not dest.is_relative_to(root):raise PackError('link: escapes package: '+str(p.relative_to(root)))
            if not dest.exists():raise PackError('link: missing '+target+' in '+str(p.relative_to(root)))
            if anchor and dest.is_file() and dest.suffix in {'.md','.mdc'} and anchor not in anchors(read(dest)):
                raise PackError('link-anchor: '+target+' in '+str(p.relative_to(root)))
    # All project-rule path mentions must resolve at the installed project root.
    for host,rel in [('cursor','cursor-project/.cursor/rules/20-costvalue-method.mdc'),('portable','portable-project/AGENTS.md')]:
        for target in re.findall(r'`(\.costvalue/[^`]+\.md)`',read(root/rel)):
            if not (root/(host+'-project')/target).is_file():raise PackError('loader-target: '+target)
    if 'alwaysApply: true' not in read(root/'cursor-project/.cursor/rules/20-costvalue-method.mdc'):
        raise PackError('loader-frontmatter: missing activation setting')
    if json.loads(read(root/'MANIFEST.json'))!=manifest(root):raise PackError('manifest: count, file, hash, bytes or words mismatch')
    return len(outputs)

def main():
    a=argparse.ArgumentParser();a.add_argument('root',nargs='?',default='.');args=a.parse_args()
    try:
        n=validate(Path(args.root).resolve());print(f'STATIC VALIDATION PASSED ({n} canonical artifacts, links, loaders, inventories and manifest).')
    except (PackError,ValueError,KeyError,OSError) as e:print('FAIL:',e);sys.exit(1)
if __name__=='__main__':main()
