"""Regression tests for provenance, evidence boundaries and generated exports."""
import copy
import hashlib
import json
import re
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_observatory as build
import check_profile


class Page(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.tags = []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class ObservatoryTests(unittest.TestCase):
    def setUp(self):
        self.atlas = json.loads((ROOT / "docs/atlas.json").read_text())
        self.ledger = json.loads((ROOT / "experiments/ledger.json").read_text())

    def test_join_keeps_every_ledger_record_exactly_once_and_unchanged(self):
        data = build.build_data(self.atlas, self.ledger)
        entries = [r["ledger"] for r in data["records"] if r["ledger"]]
        self.assertEqual(sorted(entries, key=lambda e: e["id"]), sorted(self.ledger["experiments"], key=lambda e: e["id"]))
        self.assertEqual(len(data["records"]), len(self.atlas["projects"]))
        self.assertEqual(len({r["id"] for r in data["records"]}), len(data["records"]))

    def test_maturity_does_not_invent_an_evidence_state(self):
        self.atlas["projects"].append(dict(name="Future", repo="future", theme="artist", status="active", maturity="Research instrument", description="An unreviewed experiment.", do="Read"))
        record = build.build_data(self.atlas, self.ledger)["records"][-1]
        self.assertIsNone(record["ledger"])

    def test_unlisted_evidence_is_not_silently_dropped(self):
        self.atlas["projects"] = [p for p in self.atlas["projects"] if p.get("repo") != "triad"]
        records = build.build_data(self.atlas, self.ledger)["records"]
        self.assertEqual(sum(r["id"] == "triad" for r in records), 1)

    def test_repository_matching_handles_case_and_trailing_slashes(self):
        entry = self.ledger["experiments"][0]
        entry["repo"] = entry["repo"].upper().replace("HTTPS:", "https:") + "/"
        records = build.build_data(self.atlas, self.ledger)["records"]
        self.assertEqual(len(records), len(self.atlas["projects"]))

    def test_ambiguous_source_mapping_fails_closed(self):
        duplicate = copy.deepcopy(self.ledger["experiments"][0])
        duplicate["id"] = "ambiguous"
        self.ledger["experiments"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "Ambiguous"):
            build.build_data(self.atlas, self.ledger)

    def test_unsafe_links_are_rejected(self):
        for url in ["javascript:alert(1)", "data:text/html,hi", "https://", "https://name:password@example.com/", "https://example.com/\n", 'https://example.com/"onclick="x', "https://example.com\\@evil.test/"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                build.safe_url(url)

    def test_private_source_is_not_exposed(self):
        self.ledger["experiments"][0]["evidence"].append("https://github.com/topherchris420/resonance-flow-nexus/blob/main/README.md")
        with self.assertRaisesRegex(ValueError, "Non-public"):
            build.build_data(self.atlas, self.ledger)

    def test_extra_catalog_link_cannot_reintroduce_private_source(self):
        self.atlas["projects"][0]["links"] = [{"label": "Old source", "url": "https://github.com/topherchris420/resonance-flow-nexus"}]
        with self.assertRaisesRegex(ValueError, "Non-public"):
            build.build_data(self.atlas, self.ledger)

    def test_html_and_json_escape_hostile_content_without_losing_it(self):
        payload = '</script><script>alert("x")</script> & @@JS@@'
        self.atlas["projects"][0]["name"] = payload
        data = build.build_data(self.atlas, self.ledger)
        encoded = build.script_json(data)
        self.assertNotIn("</script", encoded.lower())
        self.assertEqual(json.loads(encoded)["records"][0]["name"], payload)
        tags = Page(build.cards(data)).tags
        self.assertFalse(any(tag == "script" for tag, _ in tags))
        self.assertTrue(any(tag == "article" for tag, _ in tags))

    def test_build_is_deterministic_and_hashes_match_exact_bytes(self):
        outputs = build.outputs()
        self.assertEqual(outputs, build.outputs())
        manifest = json.loads(outputs["docs/observatory-manifest.json"])
        for path, expected in manifest["inputs"].items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), expected)
        for path, expected in manifest["outputs"].items():
            self.assertEqual(hashlib.sha256(outputs[path]).hexdigest(), expected)

    def test_page_is_readable_without_scripts_and_has_no_remote_dependencies(self):
        markup = build.outputs()["docs/observatory.html"].decode()
        page = Page(markup)
        cards = [attrs for tag, attrs in page.tags if tag == "article" and "data-record" in attrs]
        self.assertEqual(len(cards), len(self.atlas["projects"]))
        self.assertFalse(any("hidden" in attrs for attrs in cards))
        self.assertFalse(any("src" in attrs for tag, attrs in page.tags if tag in ("script", "img", "iframe")))
        self.assertFalse(any(attrs.get("rel") == "stylesheet" for tag, attrs in page.tags))
        self.assertIn("connect-src 'none'", markup)
        self.assertNotRegex(markup, r"@@(?:CSS|JS|DATA|CARDS)@@")
        self.assertLess(len(markup.encode()), 300_000)

    def test_media_check_still_requires_pins_but_allows_download_links(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text('[Download](https://raw.githubusercontent.com/me/profile/main/docs/observatory.html)\n![Unpinned](https://raw.githubusercontent.com/me/repo/main/image.png)\n<img src="https://raw.githubusercontent.com/me/repo/' + 'a' * 40 + '/image.png">')
            report = check_profile.Report()
            with patch.object(check_profile, "markdown_files", return_value=[path]), patch.object(check_profile, "ROOT", Path(directory)):
                check_profile.check_pins(report)
            self.assertEqual(len(report.failures), 1)
            self.assertIn("README.md:2", report.failures[0])
            self.assertEqual(report.counts["pinned media"], 1)

    def test_document_scan_ignores_installed_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ["README.md", "docs/guide.md", "node_modules/package/README.md", ".venv/README.md"]:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# Test")
            with patch.object(check_profile, "ROOT", root):
                found = [str(path.relative_to(root)) for path in check_profile.markdown_files()]
            self.assertEqual(found, ["README.md", "docs/guide.md"])


if __name__ == "__main__":
    unittest.main()
