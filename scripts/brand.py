#!/usr/bin/env python3
"""Local brand contracts, exact SVG integrity and CSS palette checks. Stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET

HEX = re.compile(r'^#[0-9a-fA-F]{6}$')
CSS_HEX = re.compile(r'(?<![\w-])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})(?![\w-])')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def local(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('Paths must be nonempty relative strings')
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Path leaves brand folder')
    return path

def load(path):
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('Expected object with schema_version 1')
    if not isinstance(data.get('name'), str) or not data['name'].strip():
        raise ValueError('Brand name is required')
    colors = data.get('colors')
    if not isinstance(colors, dict) or not colors or any(not isinstance(k,str) or not isinstance(v,str) or not HEX.fullmatch(v) for k,v in colors.items()):
        raise ValueError('colors must map names to six-digit hex values')
    for key in ['assets', 'css_files']:
        if not isinstance(data.get(key, []), list):
            raise ValueError(key + ' must be an array')
    for asset in data.get('assets', []):
        if not isinstance(asset,dict) or not isinstance(asset.get('path'),str):
            raise ValueError('Every asset needs a path')
        if asset.get('approval') not in ['draft', 'approved']:
            raise ValueError('Asset approval must be draft or approved')
        if 'sha256' in asset and not re.fullmatch('[a-f0-9]{64}', str(asset['sha256'])):
            raise ValueError('Invalid SHA256')
        for field in ['expected_fills','allowed_fonts']:
            if field in asset and (not isinstance(asset[field],list) or not all(isinstance(x,str) for x in asset[field])):
                raise ValueError(field + ' must be a string array')
    return data

def audit(manifest):
    data = load(manifest)
    root = manifest.parent
    rows = []
    def add(state, subject, message):
        rows.append({'status':state,'subject':subject,'message':message})
    if not data.get('assets'):
        add('UNKNOWN','assets','No assets declared; no asset integrity checked')
    for asset in data.get('assets', []):
        label=asset['path']; path=local(root,label)
        if not path.is_file():
            add('MISSING',label,'Declared asset is absent'); continue
        add('VERIFIED',label,'File exists')
        if asset.get('approval') != 'approved':
            add('UNKNOWN',label,'Draft asset; existence does not establish visual approval')
        expected=asset.get('sha256')
        if expected:
            add('VERIFIED' if sha(path)==expected else 'MISSING',label,'SHA256 matches declared baseline' if sha(path)==expected else 'Integrity mismatch against declared baseline')
        else:
            add('UNKNOWN',label,'No SHA256 baseline declared')
        if path.suffix.lower() == '.svg':
            try: tree=ET.fromstring(path.read_text())
            except (ET.ParseError, UnicodeError):
                add('MISSING',label,'Invalid SVG XML'); continue
            text=[node for node in tree.iter() if node.tag.split('}')[-1]=='text']
            if text:
                add('UNKNOWN',label,'Live SVG text requires font portability and visual verification')
            if asset.get('expected_fills') is not None:
                actual={n.get('fill').lower() for n in tree.iter() if n.get('fill') and n.get('fill')!='none'}
                wanted={v.lower() for v in asset['expected_fills']}
                add('VERIFIED' if actual==wanted else 'MISSING',label,'Explicit fill attributes match' if actual==wanted else 'Explicit fill attributes differ; styles/inheritance are not evaluated')
            if asset.get('allowed_fonts') is not None:
                wanted=set(asset['allowed_fonts']); actual={n.get('font-family') for n in text}
                add('VERIFIED' if actual.issubset(wanted) else 'MISSING',label,'Declared font-family attributes allowed' if actual.issubset(wanted) else 'Unexpected font-family attribute')
    palette={v.lower() for v in data['colors'].values()}
    for value in data.get('css_files', []):
        path=local(root,value)
        if not path.is_file():
            add('MISSING',value,'Declared CSS is absent'); continue
        # Lexical check only. Ignore comments; never claim computed-style coverage.
        css=re.sub(r'/\*.*?\*/','',path.read_text(),flags=re.S)
        found={x.lower() for x in CSS_HEX.findall(css)}
        unexpected=sorted(found-palette)
        add('MISSING' if unexpected else 'VERIFIED',value,'Hex literals outside palette: '+', '.join(unexpected) if unexpected else 'Hex literals use declared palette (not a computed-style audit)')
        if re.search(r'\b(?:rgb|hsl|hwb|lab|lch|oklab|oklch|color|color-mix)\s*\(',css,re.I) or re.search(r':\s*[a-zA-Z]+\s*[;}]',css):
            add('UNKNOWN',value,'Non-hex values may exist; no full CSS parser or variable resolution')
    if not data.get('css_files'):
        add('UNKNOWN','css','No CSS files declared')
    add('UNKNOWN','visual','No visual fidelity, small-size, contrast, 3D or physical production certification')
    return rows

def export(manifest, output):
    """Copy approved pinned SVG bytes only. Never redraw or auto-recolor."""
    data=load(manifest); root=manifest.parent
    selected=[a for a in data.get('assets',[]) if a.get('approval')=='approved' and a['path'].lower().endswith('.svg')]
    if not selected: raise ValueError('No approved SVG assets declared')
    items=[]; names=set()
    for asset in selected:
        src=local(root,asset['path']); name=src.name
        if name in names: raise ValueError('Duplicate export basename')
        names.add(name)
        if not src.is_file() or not asset.get('sha256'):
            raise ValueError('Approved SVG must exist and match its SHA256 baseline')
        body = src.read_bytes()
        if hashlib.sha256(body).hexdigest() != asset['sha256']:
            raise ValueError('Approved SVG must exist and match its SHA256 baseline')
        ET.fromstring(body)
        items.append((name, body))
    if output.exists(): raise ValueError('Output must be a new directory; existing work is preserved')
    output.mkdir(parents=True)
    for name,body in items:(output/name).write_bytes(body)
    return [name for name,_ in items]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('audit');a.add_argument('manifest',type=Path)
    a.add_argument('--json',action='store_true')
    e=sub.add_parser('export');e.add_argument('manifest',type=Path);e.add_argument('output',type=Path)
    args=p.parse_args()
    try:
        if args.command=='export':
            print(json.dumps({'exported':export(args.manifest.resolve(),args.output.resolve())}));return 0
        rows=audit(args.manifest.resolve())
        if args.json:print(json.dumps(rows,indent=2))
        else:
            for r in rows:print(f"{r['status']}: {r['subject']}: {r['message']}")
        return 1 if any(r['status']=='MISSING' for r in rows) else (2 if any(r['status']=='UNKNOWN' for r in rows) else 0)
    except (ValueError, OSError, ET.ParseError) as error:
        print('ERROR: '+str(error),file=sys.stderr);return 3

if __name__=='__main__':sys.exit(main())
