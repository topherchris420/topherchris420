import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from draw_assets import motion_coverage
from svgkit import PALETTES


class MotionCoverageTests(unittest.TestCase):
    def test_published_figure_matches_the_original_simulation(self):
        # V3D-EXP-0001: 31 reported, 40 required, 160 scheduled in heavy motion.
        for mode, palette in PALETTES.items():
            with self.subTest(mode=mode):
                published = (ROOT / "assets" / f"motion-coverage-{mode}.svg").read_text()
                self.assertEqual(published, motion_coverage(mode))
                figure = ET.fromstring(published)
                windows = figure.findall(".//{*}g[@id='scheduled-windows']/{*}circle")
                self.assertEqual(len(windows), 160)
                reported = sum(dot.get("fill") == palette["accent"] for dot in windows)
                shortfall = sum(dot.get("stroke") == palette["warm"] for dot in windows)
                self.assertEqual(reported, 31)
                self.assertEqual(reported + shortfall, 40)
