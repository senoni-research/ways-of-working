"""Scan normalized public text/paths using a private excluded-term file outside the tree.

Does not print matching terms. Not a semantic/IP audit or image/PDF inspection.
"""
import argparse,re,unicodedata,zipfile,sys
from pathlib import Path

def norm(t):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower())
def scan(root,terms):
    hits=[]
    def check(label,b):
        t=norm(label+'\n'+b.decode('utf-8','ignore'))
        if any(x in t for x in terms):hits.append(label)
    for p in root.rglob('*'):
        if not p.is_file() or '.git' in p.parts or '__pycache__' in p.parts:continue
        label=str(p.relative_to(root));check(label,p.read_bytes())
        if p.suffix.lower()=='.zip':
            with zipfile.ZipFile(p) as z:
                for x in z.infolist():
                    if not x.is_dir():check(label+'::'+x.filename,z.read(x))
    return hits

def main():
    a=argparse.ArgumentParser();a.add_argument('root');a.add_argument('--terms-file',required=True);args=a.parse_args()
    root=Path(args.root).resolve();termsfile=Path(args.terms_file).resolve()
    if termsfile.is_relative_to(root):raise SystemExit('Private exclusion configuration must be outside the public tree.')
    terms=[norm(x) for x in termsfile.read_text().splitlines() if x.strip()]
    if not terms or any(len(x)<3 for x in terms):raise SystemExit('A nonempty private exclusion list with meaningful terms is required.')
    hits=scan(root,terms)
    print('IDENTIFIER SCAN '+('FAILED' if hits else 'PASSED')+f' ({len(hits)} matching paths; {len(terms)} privately supplied patterns).')
    # Never echo paths because the forbidden identifier may be the filename itself.
    sys.exit(1 if hits else 0)
if __name__=='__main__':main()
