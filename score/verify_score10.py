"""Audit v10 plan and compile notation/MIDI into a disposable temp directory only."""
from pathlib import Path
from decimal import Decimal as D
import hashlib
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
plan = (ROOT / 'EDIT_PLAN_V10.md').read_text()
rows = []
for line in plan.splitlines():
    match = re.match(r'\| (S\d+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| (.*?) \| (.*?) \|$', line)
    if match:
        name, start, end, duration, picture, dialogue = match.groups()
        rows.append((name, D(start), D(end), D(duration), picture))
assert len(rows) == 27
assert [row[0] for row in rows] == [f'S{i:02}' for i in range(1, 28)]
# Locked S01–S26 boundaries; S27 extends the film without funding it elsewhere.
expected_ends = list(map(D, '4 6 8 10 12.5 14.5 17 20 22 27 30 32 34.5 39.5 42 47 49 51 54 56 58.5 60.5 62.5 65 67 71 76'.split()))
assert [row[2] for row in rows] == expected_ends
assert rows[-1][3] == D(5)
assert min(row[3] for row in rows) == D(2)
last = D(0)
for name, start, end, duration, picture in rows:
    minimum = D('2.5') if 'CARD 8' in picture else D(4) if name == 'S26' else D(2)
    assert start == last and end - start == duration and duration >= minimum
    assert start * 24 == int(start * 24) and end * 24 == int(end * 24)
    print(f'{name}: {start:.3f}–{end:.3f}, duration {duration:.3f}s, minimum {minimum:.3f}s PASS', flush=True)
    last = end
assert last == 76
print('TIMELINE: 27 segments, 76.000s, 1824 frames; minimum 2.000s PASS', flush=True)

def seconds(stamp):
    h, m, s = stamp.replace(',', '.').split(':')
    return D(h) * 3600 + D(m) * 60 + D(s)

speech = [(seconds(a), seconds(b)) for a,b in re.findall(r'(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})', (ROOT/'build/v7/teaser.srt').read_text())]
assert len(speech) == 11
cards = [row for row in rows if row[4].startswith('CARD ')]
for name, start, end, duration, picture in cards:
    assert all(not (start < b and a < end) for a,b in speech)
    print(f'{name} {picture.split(" — ")[0]}: no intersection with any of 11 SRT windows PASS', flush=True)
gaps = [cards[i+1][1]-cards[i][2] for i in range(7)]
assert all(a>b for a,b in zip(gaps,gaps[1:]))
print('CARD GAPS: ' + ', '.join(f'{g:.3f}s' for g in gaps) + ' strictly decreasing PASS', flush=True)
old = (ROOT/'score/score.ly').read_text()
new = (ROOT/'score/score10.ly').read_text()
# Compare every musical token before section D; ignore comments only.
for name in ['global','pianoRH','pianoLH','strings','brass']:
    def prefix(source):
        body = re.search(rf'{name} = (.*?)\n\}}', source, re.S).group(1)
        marker = {'global':'  % D:', 'pianoRH':'  % 42–46:', 'pianoLH':'  % 42–55:', 'strings':'  % 42–55:', 'brass':'  % Late entrance'}[name]
        body = body[:body.index(marker)]
        return re.sub(r'\s+', ' ', re.sub(r'%[^\n]*','',body)).strip()
    assert prefix(old) == prefix(new), name
    print(f'A–C {name}: all notation tokens unchanged PASS', flush=True)
# Frozen pre-revision A–E notation: only section F may change.
expected_ae = {'global': '2cb0551fe201a0896b17e4cc41509be1ed920be54853bf9c12ceacf24ca57f21', 'pianoRH': '4e67557fae4d12012aa0229541a8ddc7b3fb2f4aeb48525cddb5a95077a5689b', 'pianoLH': 'f1f98d5330203eacf9738be851bcf0b9b2534cd6dc380421364020bfb2a692c8', 'strings': '2b6a771dfe73a9e2feb541914496a1bf4b52683163bdd36847f5769a47302ef6', 'brass': '130d28eab0b60d42a72a718f6ff5570772b2e8ab0cdfa7047e19e88f79167b6a'}
for name, expected in expected_ae.items():
    body = re.search(rf'{name} = (.*?)\n\}}', new, re.S).group(1)
    if name == 'global':
        body = body[:body.index('  % F:')]
    else:
        # Section E ends at the final all-staff rest before the title chord.
        body = body[:body.index('  % 65–67:')] + '  r2 |'
    tokens = re.sub(r'\s+', ' ', re.sub(r'%[^\n]*', '', body)).strip()
    assert hashlib.sha256(tokens.encode()).hexdigest() == expected, name
    print(f'A–E {name}: all notation tokens unchanged PASS', flush=True)
for name in ['pianoRH', 'pianoLH', 'strings', 'brass']:
    body = re.search(rf'{name} = (.*?)\n\}}', new, re.S).group(1)
    tail = body.split('  % 65–67:')[1].split('r2 |', 1)[1]
    tail = re.sub(r'%[^\n]*', '', tail)
    tail = re.sub(r'\^\\markup\s*\{[^}]*\}', '', tail)
    assert re.fullmatch(r"\s*(<[^>]+>)1~\\fff\s*\|\s*\1(?:)" + r"1~\s*\|\s*\1(?:)" + r"4\s*\|\s*", tail), name
    print(f'F {name}: one attack, tied 4+4+1 quarters PASS', flush=True)
with tempfile.TemporaryDirectory(prefix='teaser-score10-') as temp:
    result = subprocess.run(['lilypond', '-o', str(Path(temp)/'score10'), str(ROOT/'score/score10.ly')], text=True, capture_output=True)
    print(result.stdout, end='', flush=True)
    print(result.stderr, end='', flush=True)
    assert result.returncode == 0, 'LilyPond compilation failed'
    assert 'warning:' not in result.stderr.lower(), 'Review LilyPond warning'
    for name in ['global','pianoRH','pianoLH','strings','brass']:
        assert f'AUDIT {name}: 76.000 quarter notes PASS' in result.stdout
    assert (Path(temp)/'score10.pdf').exists()
    assert (Path(temp)/'score10.midi').exists()
print('LILYPOND: successful temporary PDF/MIDI compile; all 4 parts + global = 76 quarters at quarter=60 PASS', flush=True)
print('No video or synthesized audio built. Rendered-artifact QC remains a future delivery gate.', flush=True)
