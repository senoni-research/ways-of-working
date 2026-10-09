"""Run a pre-entered synthetic case. This does not interpret any source document."""
from pathlib import Path
import argparse,json
try:from .core import review_case,serializable
except ImportError:from core import review_case,serializable

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case",choices=[f"C{i:02d}" for i in range(1,7)],default="C01")
    parser.add_argument("--quantity",type=int)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    cases=json.loads((root/"cases"/"cases.json").read_text())
    result=review_case(next(c for c in cases if c["case_id"]==args.case),args.quantity)
    print(json.dumps(serializable(result),indent=2))
if __name__=="__main__":main()
