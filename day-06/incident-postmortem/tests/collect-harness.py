"""Extract harness-written evidence; never ask the evaluated model for a trace."""
from pathlib import Path
import hashlib
import json

SESSIONS = {
    'a': '01a18fa7-1e0f-7b61-b0ec-4ec134055ead',
    'b': '01a18fa7-394d-7de1-a985-f2937c32c85d',
    'c': '01a18fa7-4b37-7003-bd59-b9aa2e4082ae',
    'd': '01a18fa7-5869-7571-848f-82273f8c40d2',
    'c-followup': '01a18faa-6a6a-70e2-8db0-f7fc6b751528',
}
tests = Path(__file__).resolve().parent
destination = tests / 'harness-review'
destination.mkdir(exist_ok=True)
manifest = {}
for case, session_id in SESSIONS.items():
    sources = list((Path.home() / '.codex/sessions').rglob(f'*{session_id}.jsonl'))
    if len(sources) != 1:
        raise ValueError(f'{case}: expected one session log, got {sources}')
    source = sources[0]
    raw = source.read_bytes()
    records = [(line, json.loads(line)) for line in raw.splitlines(keepends=True)]
    complete = [event['payload'] for _, event in records
                if event.get('type') == 'event_msg'
                and event.get('payload', {}).get('type') == 'task_complete']
    if not complete:
        print(f'{case}: pending ({len(records)} harness events)')
        continue
    calls = [event['payload'] for _, event in records
             if event.get('type') == 'response_item'
             and event.get('payload', {}).get('type') in ('function_call', 'custom_tool_call')]
    # Tool-metadata discovery cannot read incident files. Exclude its large results;
    # retain every call request so the exclusion remains inspectable.
    discovery_ids = {p.get('call_id') for p in calls
                     if 'ALL_TOOLS.' in p.get('input', '')
                     and 'await tools.' not in p.get('input', '')}
    tool_types = {'function_call', 'function_call_output', 'custom_tool_call',
                  'custom_tool_call_output'}
    selected = b''.join(line for line, event in records
                        if event.get('type') == 'response_item'
                        and event.get('payload', {}).get('type') in tool_types
                        and not (event['payload'].get('type') in ('function_call_output', 'custom_tool_call_output')
                                 and event['payload'].get('call_id') in discovery_ids)
                        and event.get('payload', {}).get('name') != 'create_thread')
    (destination / f'{case}-tools.jsonl').write_bytes(selected)
    message = complete[-1].get('last_agent_message')
    if not isinstance(message, str):
        raise ValueError(f'{case}: no final message string')
    (tests / f'output-{case}-review.md').write_text(message + '\n', encoding='utf-8', newline='\n')
    contexts = [event['payload'] for _, event in records if event.get('type') == 'turn_context']
    manifest[case] = {
        'session_id': session_id,
        'source_file': source.name,
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'tool_excerpt_sha256': hashlib.sha256(selected).hexdigest(),
        'model': contexts[-1].get('model') if contexts else None,
        'checklist_revision': 'count-and-repair' if case == 'c-followup' else 'five-field assertion',
        'omitted_metadata_only_result_call_ids': sorted(discovery_ids),
        'prompt': f'Use the skill at C:/Workspaces/ai-skill-practice/day-06/incident-postmortem to draft a postmortem from C:/Workspaces/ai-skill-practice/day-06/incident-postmortem/tests/input-{case.split("-")[0]}.md.',
    }
    print(f'{case}: extracted {len(selected)} bytes from {source.name}')
(destination / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
