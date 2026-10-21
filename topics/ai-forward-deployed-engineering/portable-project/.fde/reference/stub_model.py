"""A scripted stand-in for a chat model. Tests never call a real model.

A reply is a dict shaped like a chat completion's message: `content`, `tool_calls` (each with `id`, `name` and
JSON-encoded `arguments`), `finish_reason`, and optionally `refusal`.
"""
from __future__ import annotations

import copy
import json


class StubModel:
    def __init__(self, replies):
        self.replies = list(replies)
        self.requests = []

    def __call__(self, messages, tools):
        self.requests.append({'messages': copy.deepcopy(messages), 'tools': [t['name'] for t in tools]})
        if not self.replies:
            raise AssertionError('the stub model ran out of scripted replies')
        return self.replies.pop(0)


def call(call_id, name, **arguments):
    return {'content': None, 'finish_reason': 'tool_calls',
            'tool_calls': [{'id': call_id, 'name': name, 'arguments': json.dumps(arguments)}]}


def raw_call(call_id, name, arguments):
    return {'content': None, 'finish_reason': 'tool_calls', 'tool_calls': [{'id': call_id, 'name': name, 'arguments': arguments}]}


def text(content, finish_reason='stop', refusal=None):
    return {'content': content, 'tool_calls': [], 'finish_reason': finish_reason, 'refusal': refusal}


def from_script(script):
    """Turn a case's scripted replies into stub replies."""
    return [raw_call(r['id'], r['tool'], r.get('raw_arguments', json.dumps(r.get('arguments', {})))) if 'tool' in r
            else text(r.get('content'), r.get('finish_reason', 'stop'), r.get('refusal')) for r in script]
