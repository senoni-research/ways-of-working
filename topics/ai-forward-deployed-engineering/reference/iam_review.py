"""Reading an IAM policy for routes to more permission, and a GitHub OIDC trust policy for who it lets in.

Standard library only. ESCALATION is a Senoni starting list of actions that let a principal grant itself or another
principal more than it was given; it is not complete, and a finding is a prompt for review, not a verdict.
"""
from __future__ import annotations

from fnmatch import fnmatchcase

ESCALATION = (
    'iam:AddUserToGroup', 'iam:AttachGroupPolicy', 'iam:AttachRolePolicy', 'iam:AttachUserPolicy',
    'iam:CreateAccessKey', 'iam:CreateLoginProfile', 'iam:CreatePolicyVersion', 'iam:PassRole',
    'iam:PutGroupPolicy', 'iam:PutRolePolicy', 'iam:PutUserPolicy', 'iam:SetDefaultPolicyVersion',
    'iam:UpdateAssumeRolePolicy', 'iam:UpdateLoginProfile', 'sts:AssumeRole',
)
GITHUB = 'token.actions.githubusercontent.com'


def _list(value) -> list:
    return value if isinstance(value, list) else [value]


def escalation(policy: dict) -> list[str]:
    """Allowed actions, after expanding wildcards, that are on the escalation list, and any Allow with NotAction."""
    findings = []
    for st in _list(policy['Statement']):
        if st.get('Effect') != 'Allow':
            continue
        if 'NotAction' in st:
            findings.append(f"NotAction allows everything except {', '.join(_list(st['NotAction']))}")
            continue
        resources = ', '.join(_list(st.get('Resource', '*')))
        for pattern in _list(st['Action']):
            for action in ESCALATION:
                if fnmatchcase(action.lower(), pattern.lower()):
                    findings.append(f'{action} on {resources} (from {pattern})')
    return findings


def oidc_trust(trust: dict) -> list[str]:
    """What a role's trust policy lets in from GitHub Actions: the audience must be sts.amazonaws.com and the subject
    one repository and branch or environment, compared exactly."""
    findings = []
    for st in _list(trust['Statement']):
        if st.get('Effect') != 'Allow' or not any(GITHUB in p for p in _list(st.get('Principal', {}).get('Federated', ''))):
            continue
        equals = st.get('Condition', {}).get('StringEquals', {})
        like = st.get('Condition', {}).get('StringLike', {})
        if equals.get(f'{GITHUB}:aud') != 'sts.amazonaws.com':
            findings.append('audience is not pinned to sts.amazonaws.com')
        subjects = _list(equals.get(f'{GITHUB}:sub') or like.get(f'{GITHUB}:sub') or [])
        if not subjects:
            findings.append('subject is not checked: any repository on GitHub can assume the role')
        for sub in subjects:
            if '*' in sub or '?' in sub:
                findings.append(f'subject has a wildcard: {sub}')
            elif not (':ref:refs/heads/' in sub or ':environment:' in sub):
                findings.append(f'subject is not pinned to a branch or environment: {sub}')
    return findings
