"""Audit v10 plan and compile notation/MIDI into a disposable temp directory only."""
from pathlib import Path
from decimal import Decimal as D
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
assert len(rows) == 26
last = D(0)
for name, start, end, duration, picture in rows:
    minimum = D('2.5') if 'CARD 8' in picture else D(4) if name == 'S26' else D(2)
    assert start == last and end - start == duration and duration >= minimum
    assert start * 24 == int(start * 24) and end * 24 == int(end * 24)
    print(f'{name}: {start:.3f}–{end:.3f}, duration {duration:.3f}s, minimum {minimum:.3f}s PASS', flush=True)
    last = end
assert last == 71
print('TIMELINE: 26 segments, 71.000s, 1704 frames; minimum 2.000s PASS', flush=True)

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
with tempfile.TemporaryDirectory(prefix='teaser-score10-') as temp:
    result = subprocess.run(['lilypond', '-o', str(Path(temp)/'score10'), str(ROOT/'score/score10.ly')], text=True, capture_output=True)
    print(result.stdout, end='', flush=True)
    print(result.stderr, end='', flush=True)
    assert result.returncode == 0, 'LilyPond compilation failed'
    assert 'warning:' not in result.stderr.lower(), 'Review LilyPond warning'
    for name in ['global','pianoRH','pianoLH','strings','brass']:
        assert f'AUDIT {name}: 71.000 quarter notes PASS' in result.stdout
    assert (Path(temp)/'score10.pdf').exists()
    assert (Path(temp)/'score10.midi').exists()
print('LILYPOND: successful temporary PDF/MIDI compile; all 4 parts + global = 71 quarters at quarter=60 PASS', flush=True)
print('No video or synthesized audio built. Rendered-artifact QC remains a future delivery gate.', flush=True)
