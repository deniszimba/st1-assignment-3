"""Staff-maintained, contract-based Stage 8 preparation. Not application code."""

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import xml.etree.ElementTree as ET

VERSION = '1.1'
TARGET = Path('smartcare/data_store.py')
RECORD = '.stage8_faults'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
EXPECTED = {'test_f8_01_conflict', 'test_f8_02_history'}
PROBES = '''
from datetime import datetime
import pytest
from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService, PractitionerService, AppointmentService


def project():
    store = SmartCareDataStore()
    PatientService(store).register_patient("probe-p", "Synthetic Probe")
    PractitionerService(store).register_practitioner("probe-d", "Synthetic Probe", "General")
    return store, AppointmentService(store)


def test_f8_01_conflict():
    store, service = project()
    when = datetime(2026, 10, 1, 9)
    service.book_appointment("probe-1", "probe-p", "probe-d", when)
    before = store.list_appointments()
    with pytest.raises(ValueError):
        service.book_appointment("probe-2", "probe-p", "probe-d", when)
    assert store.list_appointments() == before


def test_f8_02_history():
    store, service = project()
    a = service.book_appointment("probe-history", "probe-p", "probe-d", datetime(2026, 10, 1, 9))
    service.cancel_appointment(a.appointment_id)
    assert a.status.value == "cancelled"
    assert a in store.list_appointments()
    assert service.find_appointment(a.appointment_id) is a
'''
# This diagnostic validates the exact faulty outcomes, not merely arbitrary failures.
SIGNATURE = '''
from datetime import datetime
from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService, PractitionerService, AppointmentService

def project():
    s = SmartCareDataStore()
    PatientService(s).register_patient("P", "Synthetic")
    PractitionerService(s).register_practitioner("D", "Synthetic", "General")
    PractitionerService(s).register_practitioner("E", "Synthetic", "General")
    return s, AppointmentService(s)

s, v = project()
t = datetime(2026, 10, 1, 9)
v.book_appointment("A", "P", "D", t)
b = v.book_appointment("B", "P", "D", t)
assert b in s.list_appointments(), "Same-practitioner fault not observable"
try:
    v.book_appointment("C", "P", "E", t)
except ValueError:
    pass
else:
    raise AssertionError("Different-practitioner fault signature missing")
s, v = project()
a = v.book_appointment("H", "P", "D", t)
v.cancel_appointment("H")
assert a in s.list_appointments() and a.status.value == "cancelled"
assert s.find_appointment("H") is None
try:
    v.find_appointment("H")
except LookupError:
    pass
else:
    raise AssertionError("History lookup fault not observable")
print("Both approved symptom signatures confirmed")
'''
FAULT_BODIES = {
    'find_appointment': '''
if not isinstance(appointment_id, str) or not appointment_id.strip():
    raise ValueError("Appointment ID cannot be blank")
for appointment in self.list_appointments():
    if (appointment.appointment_id == appointment_id.strip()
            and appointment.status.value != "cancelled"):
        return appointment
return None
''',
    'has_practitioner_conflict': '''
for appointment in self.list_appointments():
    if (appointment.appointment_id != exclude_appointment_id
            and appointment.practitioner.practitioner_id != practitioner_id
            and appointment.date_time == date_time
            and appointment.status.value == "scheduled"):
        return True
return False
'''
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(command, cwd, timeout=60):
    return subprocess.run(command, cwd=cwd, env=ENV, text=True,
                          capture_output=True, timeout=timeout)


def ensure_project(project):
    if not project.is_dir() or not (project / TARGET).is_file():
        raise ValueError('Required smartcare/data_store.py was not found')
    if any(p.is_symlink() for p in project.rglob('*')):
        raise ValueError('Use a regular project copy without symbolic links')
    required = ['smartcare/domain.py', 'smartcare/services.py', 'tests']
    if not all((project / p).exists() for p in required):
        raise ValueError('Required public project structure is missing')


def transformed(source):
    tree = ast.parse(source)
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'SmartCareDataStore']
    if len(classes) != 1:
        raise ValueError('Expected exactly one SmartCareDataStore class')
    methods = [n for n in classes[0].body if isinstance(n, ast.FunctionDef)]
    names = [n.name for n in methods]
    contracts = {
        'find_appointment': ['self', 'appointment_id'],
        'has_practitioner_conflict': ['self', 'practitioner_id', 'date_time', 'exclude_appointment_id'],
        'list_appointments': ['self'],
    }
    edits = []
    for name, signature in contracts.items():
        if names.count(name) != 1:
            raise ValueError(f'Missing or duplicate public method: {name}')
        node = next(n for n in methods if n.name == name)
        args = node.args
        if ([a.arg for a in args.args] != signature or args.posonlyargs or args.kwonlyargs
                or args.vararg or args.kwarg or node.decorator_list):
            raise ValueError(f'Unexpected public signature: {name}')
        if name == 'has_practitioner_conflict':
            if len(args.defaults) != 1 or not isinstance(args.defaults[0], ast.Constant) or args.defaults[0].value is not None:
                raise ValueError('Expected optional exclude_appointment_id=None')
        if name in FAULT_BODIES:
            if node.body[0].lineno <= node.lineno:
                raise ValueError('Use a multi-line method body for controlled preparation')
            body = textwrap.indent(textwrap.dedent(FAULT_BODIES[name]).lstrip(), ' ' * (node.col_offset + 4))
            edits.append((node.body[0].lineno - 1, node.end_lineno, body))
    lines = source.splitlines(keepends=True)
    for start, stop, body in sorted(edits, reverse=True):
        lines[start:stop] = [body]
    candidate = ''.join(lines)
    compile(candidate, str(TARGET), 'exec')
    return candidate


def copy_project(project, destination):
    shutil.copytree(project, destination, ignore=shutil.ignore_patterns(
        '.git', RECORD, '__pycache__', '.pytest_cache', '.venv'))


def probes(project, output_dir):
    # Keep infrastructure outside the project's source/tests but import that project.
    probe = output_dir / 'test_stage8_contract.py'
    probe.write_text(PROBES)
    xml = output_dir / 'probes.xml'
    env = dict(ENV, PYTHONPATH=str(project))
    result = subprocess.run([sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
        str(probe), '--junitxml=' + str(xml)], cwd=project, env=env,
        capture_output=True, text=True, timeout=60)
    if not xml.exists():
        raise ValueError('Probe collection/execution failed: ' + result.stderr)
    root = ET.parse(xml).getroot()
    cases = root.findall('.//testcase')
    errors = root.findall('.//error')
    failed = {c.attrib['name'] for c in cases if c.find('failure') is not None}
    if errors or {c.attrib['name'] for c in cases} != EXPECTED:
        raise ValueError('Unexpected probe collection/import failure')
    return result.returncode, failed


def verify_faults(project, temporary):
    code, failed = probes(project, temporary)
    if code != 1 or failed != EXPECTED:
        raise ValueError('The two intended failing tests were not reproduced')
    result = run([sys.executable, '-B', '-c', SIGNATURE], project)
    if result.returncode != 0:
        raise ValueError('Failures did not match the approved symptom signatures: ' + result.stderr)


def git_baseline(project):
    if shutil.which('git') is None:
        return None
    top = run(['git', 'rev-parse', '--show-toplevel'], project)
    if top.returncode != 0:
        return None
    repository = Path(top.stdout.strip()).resolve()
    if project != repository / 'project':
        raise ValueError('Git application must be the repository root project/ directory')
    branch_result = run(['git', 'branch', '--show-current'], repository)
    if branch_result.returncode:
        raise ValueError('Cannot establish Git branch')
    branch = branch_result.stdout.strip()
    if not branch or branch in ('main', 'master'):
        raise ValueError('Create a named debugging branch before preparation')
    status = run(['git', 'status', '--porcelain', '--untracked-files=all'], repository)
    if status.returncode or status.stdout.strip():
        raise ValueError('Commit or move repository changes before preparation')
    head = run(['git', 'rev-parse', '--verify', 'HEAD'], repository)
    if head.returncode:
        raise ValueError('A committed Stage 7 baseline is required')
    return head.stdout.strip()


def prepare(project, apply):
    ensure_project(project)
    if (project / RECORD).exists():
        raise ValueError('A preparation/recovery record already exists; do not stack faults or overwrite repairs')
    sha = git_baseline(project)
    original = (project / TARGET).read_bytes()
    candidate = transformed(original.decode('utf-8')).encode('utf-8')
    with tempfile.TemporaryDirectory(prefix='.stage8-check-', dir=project.parent) as name:
        tmp = Path(name)
        copy = tmp / 'project'
        copy_project(project, copy)
        suite = run([sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'tests'], copy)
        if suite.returncode != 0:
            raise ValueError('Baseline tests must pass before preparation: ' + suite.stdout[-2000:])
        code, failed = probes(copy, tmp)
        if code != 0 or failed:
            raise ValueError('Baseline does not meet the two correct Stage 7 service contracts')
        (copy / TARGET).write_bytes(candidate)
        verify_faults(copy, tmp)
    print(f'Stage 8 tool {VERSION}; preflight PASS; baseline SHA256 {digest(original)}')
    if sha:
        print('Baseline Git SHA ' + sha)
    if not apply:
        print('CHECK ONLY: project unchanged; both proposed fault signatures verified in a temporary copy')
        return
    # Check again before mutation; do not overwrite changes made during preflight.
    if (project / TARGET).read_bytes() != original:
        raise ValueError('Source changed during preflight; no faults applied')
    if sha and git_baseline(project) != sha:
        raise ValueError('Git state changed during preflight')
    record = project / RECORD
    record.mkdir()
    (record / 'data_store.before.py').write_bytes(original)
    metadata = {'tool_version': VERSION, 'baseline_sha256': digest(original),
                'fault_sha256': digest(candidate), 'git_sha': sha, 'status': 'prepared'}
    (record / 'record.json').write_text(json.dumps(metadata, indent=2) + '\n')
    staged = record / 'data_store.pending'
    staged.write_bytes(candidate)
    os.replace(staged, project / TARGET)
    try:
        with tempfile.TemporaryDirectory(prefix='.stage8-verify-', dir=project.parent) as name:
            verify_faults(project, Path(name))
    except Exception:
        # Automatic rollback only for this tool's unchanged candidate bytes.
        if (project / TARGET).read_bytes() == candidate:
            (project / TARGET).write_bytes(original)
        metadata['status'] = 'rolled-back'
        (record / 'record.json').write_text(json.dumps(metadata, indent=2) + '\n')
        raise
    print('PREPARED: F8-01 practitioner conflict; F8-02 retained-history lookup')
    print('Verified expected failures: test_f8_01_conflict; test_f8_02_history (2 failed)')
    print('Backup/hash recorded in .stage8_faults; use --restore for setup recovery only')


def restore(project):
    ensure_project(project)
    record = project / RECORD
    meta = json.loads((record / 'record.json').read_text())
    original = (record / 'data_store.before.py').read_bytes()
    current = (project / TARGET).read_bytes()
    if digest(original) != meta['baseline_sha256']:
        raise ValueError('Backup hash mismatch; refusing restoration')
    if meta['status'] != 'prepared' or digest(current) != meta['fault_sha256']:
        raise ValueError('File has changed since preparation; preserve your repairs, restore manually from the baseline if intended')
    (project / TARGET).write_bytes(original)
    meta['status'] = 'restored'
    (record / 'record.json').write_text(json.dumps(meta, indent=2) + '\n')
    print('RESTORED: original data_store.py bytes verified; preparation record retained')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    for option in ['check', 'apply', 'verify', 'restore']:
        mode.add_argument('--' + option, action='store_true')
    args = parser.parse_args()
    project = args.project.resolve()
    try:
        if args.restore:
            restore(project)
        elif args.verify:
            ensure_project(project)
            with tempfile.TemporaryDirectory(prefix='.stage8-verify-', dir=project.parent) as name:
                verify_faults(project, Path(name))
            print('VERIFIED: exactly 2 expected failures; both approved symptom signatures present')
        else:
            prepare(project, args.apply)
    except (ValueError, OSError, SyntaxError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print('REFUSED: ' + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
