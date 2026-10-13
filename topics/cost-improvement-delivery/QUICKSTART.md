# Quickstart

## 1. Install the base first

This companion needs **Cost & Value Engineering 0.3.3** in the same project, installed as `.costvalue/` with its own loader (`.cursor/rules/20-costvalue-method.mdc` for Cursor, or its `AGENTS.md` section). Install it from that pack's own instructions. The companion does not copy or replace any base file.

The base files the companion relies on are listed with their hashes in `.valuedelivery/REQUIRES.json`: eleven modules and the templates module, recipes M14 and M15, the source register and two reference files.

## 2. Add the companion without overwriting anything

Every file in the companion trees has a name that differs from the base trees, so copying cannot overwrite a base file. Copy only what is listed here.

**Cursor:** from `cursor-project/`, copy `.valuedelivery/` and `.cursor/rules/30-valuedelivery-method.mdc` into the project. Keep `20-costvalue-method.mdc` and all other rules. `VALUEDELIVERY-INSTALL.md` and `valuedelivery-cursor.md` are for reading; they do not need to be copied.

**OpenCode, Cline or another `AGENTS.md` reader:** from `portable-project/`, copy `.valuedelivery/` and append the whole of `AGENTS.valuedelivery.md` to the project's existing `AGENTS.md`, after the base section. Do not replace the file. Cline users may instead copy `optional-adapters/.clinerules/30-valuedelivery.md`; use one companion entry route, not both.

## 3. Check the installation

From the project root:

```bash
python3 .valuedelivery/check_install.py
```

It reads only. It confirms that every required base file is present and identical to the pinned 0.3.3 release, that a base loader is installed, and that exactly one companion entry route exists. A locally adapted base file fails the check; review compatibility before relying on the companion. Then run the companion's synthetic tests in place:

```bash
python3 -m unittest discover -s .valuedelivery/reference -p 'test_*.py'
```

## 4. First prompt

> Read the installed Cost & Value operating contract and workflow, then `.valuedelivery/00-activation-and-boundary.md`. Using the synthetic SYN-VD01 case, explain why the run rate stays at 36000 while the first-year effect falls from 3000 to minus 6000 when go-live moves from July to October, and what the three-day engineering shortfall does and does not tell us. Name the files you read. Do not call an external service or publish anything. Finish with the commands you ran and what remains unverified.

## 5. Fresh-session check

Ask the assistant which loader and module paths it used, why a cancelled initiative stays in the original baseline view, and whether the base engine accepts the companion annex. The correct answer to the last question is no. A plausible explanation does not prove the rules were loaded; give it a new small case without the expected answer and check the result yourself.

The [cases](cases/README.md) include their expected answers, so they are regressions, not blind tests.
