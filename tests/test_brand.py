import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('brand',Path(__file__).resolve().parents[1]/'scripts/brand.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

class BrandAuditTests(unittest.TestCase):
    def setup_brand(self,root):
        (root/'mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><path fill="#112233" d="M0 0H10V10Z"/></svg>')
        (root/'site.css').write_text('body{color:#112233}')
        data={'schema_version':1,'name':'Test','colors':{'ink':'#112233'},'assets':[{'path':'mark.svg','approval':'approved','sha256':b.sha(root/'mark.svg'),'expected_fills':['#112233']}],'css_files':['site.css']}
        p=root/'brand.json';p.write_text(json.dumps(data));return p,data
    def test_detects_byte_drift(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);p,d=self.setup_brand(r);(r/'mark.svg').write_text('<svg/>')
            self.assertTrue(any('Integrity mismatch' in x['message'] for x in b.audit(p)))
    def test_detects_css_palette_drift(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);p,d=self.setup_brand(r);(r/'site.css').write_text('body{color:#445566}')
            self.assertTrue(any(x['status']=='MISSING' and x['subject']=='site.css' for x in b.audit(p)))
    def test_nonhex_is_unknown(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);p,d=self.setup_brand(r);(r/'site.css').write_text('body{color:red}')
            self.assertTrue(any(x['status']=='UNKNOWN' and x['subject']=='site.css' for x in b.audit(p)))
    def test_export_preserves_bytes_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);p,d=self.setup_brand(r);out=r/'export'
            b.export(p,out);self.assertEqual((out/'mark.svg').read_bytes(),(r/'mark.svg').read_bytes())
            with self.assertRaises(ValueError):b.export(p,out)
    def test_export_rejects_unpinned_before_writing(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);p,d=self.setup_brand(r);d['assets'][0].pop('sha256');p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):b.export(p,r/'export')
            self.assertFalse((r/'export').exists())
    def test_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);p,d=self.setup_brand(r);d['assets'][0]['path']='../private.svg';p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):b.audit(p)
    def test_invalid_contract(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);p,d=self.setup_brand(r);d['colors']=['red'];p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):b.audit(p)
    def test_live_text_requires_review(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);p,d=self.setup_brand(r);(r/'mark.svg').write_text('<svg><text>Test</text></svg>')
            self.assertTrue(any('Live SVG text' in x['message'] for x in b.audit(p)))

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t); home=r/'brand';home.mkdir();p,d=self.setup_brand(home)
            outside=r/'private.svg';outside.write_text('<svg/>')
            (home/'link.svg').symlink_to(outside)
            d['assets'][0]['path']='link.svg';p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):b.audit(p)
            with self.assertRaises(ValueError):b.export(p,r/'out')
            self.assertFalse((r/'out').exists())
    def test_export_reads_verified_snapshot_once(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);p,d=self.setup_brand(r);original=Path.read_bytes
            reads=[]
            def read(path):
                if path.name=='mark.svg':
                    reads.append(path)
                    if len(reads)>1:return b'<svg>changed</svg>'
                return original(path)
            with patch.object(Path,'read_bytes',read):b.export(p,r/'out')
            self.assertEqual(len(reads),1)
            self.assertEqual((r/'out/mark.svg').read_bytes(),(r/'mark.svg').read_bytes())
    def test_invalid_optional_attribute_arrays(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);p,d=self.setup_brand(r)
            for field in ['expected_fills','allowed_fonts']:
                d['assets'][0][field]='not-an-array';p.write_text(json.dumps(d))
                with self.assertRaises(ValueError):b.load(p)
                d['assets'][0].pop(field)

if __name__=='__main__':unittest.main()
