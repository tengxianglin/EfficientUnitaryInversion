"""Restore earlier exact source text by reversing the recorded additive edits.

Every reconstructed source must match its original run's ledger SHA256 before
being written. This does not alter previous outputs or rerun mathematics.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / 'code/audit_rref.py').read_text()


def replace_once(text, old, new):
    assert text.count(old) == 1, repr(old)
    return text.replace(old, new, 1)


def drop_section(text, start, end):
    assert text.count(start) == text.count(end) == 1
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + text[b:]


v2 = drop_section(source, 'def word_physical(word):\n', 'def physical_omega(a, b, n):\n')
v2 = replace_once(v2, "    (args.output / 'source_audit_rref.py.txt').write_text(Path(__file__).read_text())\n", '')
v2 = replace_once(v2, "    (args.output / 'source_rref_census.cpp.txt').write_text(Path(__file__).with_name('rref_census.cpp').read_text())\n", '')
v2 = drop_section(v2, "    given_grid = ['YIII'", "    subprocess.run([str(args.backend), '2'")

v1 = replace_once(v2, 'def compare_source(source, output, census, census_n2):', 'def compare_source(source, output, census):')
v1 = replace_once(v1, "        records = data.get('cases', data.get('types', data.get('records', data.get('rows', []))))", "        records = data.get('types', data.get('records', data.get('rows', [])))")
start = "            comparison = {'Bmask': b, 'qmask': q, 'source_allowed': allowed, 'independent_allowed': ours}\n"
end = "            assert ours == allowed\n"
a, b = v1.index(start), v1.index(end, v1.index(start))
v1 = v1[:a] + "            compared.append({'Bmask': b, 'qmask': q, 'source_allowed': allowed, 'independent_allowed': ours})\n" + v1[b:]
v1 = replace_once(v1, "            row['nine_q_plus_phase_defect'] = [quadratic(b, q, v) for v in GRID] + [sum((b >> k) & 1 for k in (0, 1, 2, 4, 5)) % 2]\n", '')
v1 = replace_once(v1, "    gate('nine_q_plus_phase_defect_bijection', len({tuple(r['nine_q_plus_phase_defect']) for r in types}) == 1024, {'signatures': len({tuple(r['nine_q_plus_phase_defect']) for r in types})})\n", '')
v1 = replace_once(v1, "    delta_one = {v for v in range(16) if delta(v)}\n    assert {a[9] for a in group} == delta_one\n", '')
start = "    physical_B = {t // 16 for t in range(1024) if n3['type_counts'][t]}\n"
end = "    write(args.output / 'quadratic_orbits.json'"
a, b = v1.index(start), v1.index(end, v1.index(start))
v1 = v1[:a] + "    write(args.output / 'incidence_group72.json', {'actions': group, 'tests': {'order': 72, 'closed': True, 'inverses': True, 'canonical_invariance_checks': 1024 * 72}})\n" + v1[b:]
v1 = replace_once(v1, '    compare_source(args.source, args.output, n3, n2)', '    compare_source(args.source, args.output, n3)')

records = []
for directory, text in [('T1', v1), ('T1_verified', v2), ('T1_final', source)]:
    ledger = json.loads((ROOT / 'results' / directory / 'ledger.json').read_text())
    actual = hashlib.sha256(text.encode()).hexdigest()
    expected = ledger['code_sha256']['audit_rref.py']
    assert actual == expected, (directory, actual, expected)
    target = ROOT / 'results' / directory / 'source_audit_rref.py.txt'
    if target.exists():
        assert target.read_text() == text
    else:
        target.write_text(text)
    cpp = (ROOT / 'code/rref_census.cpp').read_bytes()
    assert hashlib.sha256(cpp).hexdigest() == ledger['code_sha256']['rref_census.cpp']
    target_cpp = ROOT / 'results' / directory / 'source_rref_census.cpp.txt'
    if target_cpp.exists():
        assert target_cpp.read_bytes() == cpp
    else:
        target_cpp.write_bytes(cpp)
    records.append({'output_directory': directory, 'source_sha256': actual,
                    'snapshot_matches_original_run_ledger': True})
target = Path(__file__).with_name('snapshot_provenance.json')
assert not target.exists()
target.write_text(json.dumps({'method': 'Reverse recorded additive edits; every snapshot hash is checked against the original run ledger before write.', 'records': records}, indent=2) + '\n')
print(json.dumps(records))
