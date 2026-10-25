"""Preserve and verify both executed T2 source versions without rerunning science."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
final = (root / 'code/audit_comb_indices.py').read_text()
start = final.index('\ndef scalar_partial(')
end = final.index('\ndef certify(', start)
initial = final[:start] + final[end:]
removed = ('"scalar_trace_o_matches_Q"', '"scalar_trace_a_Q_equals_identity"',
           '"scalar_trace_o_completion"', '"explicit_teleportation_network_t_over_d"',
           '"teleportation_numerator_nonzero"', '"proofs/one_query_audit.md"')
initial = ''.join(line for line in initial.splitlines(keepends=True)
                  if not any(marker in line for marker in removed))
records = []
for name, source in [('T2', initial), ('T2_final', final)]:
    report = json.loads((root / 'results' / name / 'comb_index_audit.json').read_text())
    actual = hashlib.sha256(source.encode()).hexdigest()
    expected = report['source_hashes']['audit_comb_indices.py']
    assert actual == expected, (name, actual, expected)
    target = root / 'results' / name / 'audit_comb_indices.py'
    with target.open('x') as f:
        f.write(source)
    records.append({'snapshot': str(target.relative_to(root)), 'sha256': actual,
                    'matches_executed_output_source_hash': True})
proof = root / 'proofs/one_query_audit.md'
record = json.loads((root / 'results/T2_final/comb_index_audit.json').read_text())
assert hashlib.sha256(proof.read_bytes()).hexdigest() == record['source_hashes']['proofs/one_query_audit.md']
with (root / 'results/T2_final/one_query_audit_executed.md').open('xb') as f:
    f.write(proof.read_bytes())
records.append({'snapshot': 'results/T2_final/one_query_audit_executed.md',
                'sha256': record['source_hashes']['proofs/one_query_audit.md'],
                'matches_executed_output_source_hash': True})
with (root / 'results/T2_executed_source_manifest.json').open('x') as f:
    json.dump({'status': 'verified_source_preservation', 'sources': records}, f, indent=2)
    f.write('\n')
print(json.dumps({'status': 'verified_source_preservation', 'sources': records}))
