"""Run with Python, Playwright and Chromium. All feed responses are fixtures."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
GAME = {"away_team": "Test Away", "home_team": "Test Home",
        "best_home": {"price": -110, "bookmaker": "Example"}}


class OverlayTest(unittest.TestCase):
    def setUp(self):
        playwright = sync_playwright().start()
        self.addCleanup(playwright.stop)
        browser = playwright.chromium.launch(channel=os.getenv("CHROMIUM_CHANNEL"))
        self.addCleanup(browser.close)
        self.page = browser.new_page(viewport={"width": 1920, "height": 1080})
        self.page.clock.install()

    def test_rehearsal_stays_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            standalone = Path(tmp, "renamed.html")
            subprocess.run([sys.executable, ROOT / "build_rehearsal.py", standalone], check=True)
            addresses = [(standalone, "?mode=preview"), (ROOT / "overlay.html", "?mode=rehearsal")]
            requests = []
            def block(route):
                requests.append(route.request.url)
                route.abort()
            self.page.route("https://**/*", block)
            self.page.route("http://**/*", block)
            for file, options in addresses:
                self.page.goto(file.as_uri() + options)
                expect(self.page.locator("#mode-label")).to_have_text("REHEARSAL")
                expect(self.page.locator(".note")).to_have_text("Fictional teams and prices")
                expect(self.page.locator(".card.on")).to_contain_text("Harbor Owls")
                self.page.clock.fast_forward(8000)
                expect(self.page.locator(".card.on")).to_contain_text("Cedar Kites")
                self.page.clock.fast_forward(8000)
                expect(self.page.locator(".card.on")).to_contain_text("Ridge Comets")
                self.page.clock.fast_forward(120000)
            self.assertEqual(requests, [])

    def test_failed_empty_and_recovered_snapshots(self):
        replies = iter([{"games": [GAME]}, None, {}, {"games": []}, {"games": [GAME]}])
        def send(route):
            self.assertTrue(route.request.url.endswith("/live/api/command_center?sport=nba"))
            data = next(replies)
            if data is None:
                route.abort()
            else:
                route.fulfill(json=data, headers={"Access-Control-Allow-Origin": "*"})
        self.page.route("https://**/*", send)
        self.page.goto((ROOT / "overlay.html").as_uri() + "?sport=nba")
        note = self.page.locator(".note")
        card = self.page.locator(".card.on")
        expect(card).to_contain_text("Test Home")
        expect(note).to_have_text("Public preview")
        for _ in range(2):
            with self.page.expect_console_message(lambda msg: "overlay fetch failed" in msg.text):
                self.page.clock.fast_forward(60000)
            expect(note).to_have_text("Cached · refresh failed")
            expect(card).to_contain_text("Test Home")
        self.page.clock.fast_forward(60000)
        expect(note).to_have_text("Feed checked")
        expect(self.page.locator(".card")).to_have_count(0)
        expect(self.page.locator("#empty")).to_be_visible()
        self.page.clock.fast_forward(60000)
        expect(note).to_have_text("Public preview")
        expect(card).to_contain_text("Test Home")


if __name__ == "__main__":
    unittest.main()
