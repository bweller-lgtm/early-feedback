const { chromium } = require("playwright");
const path = require("path");

const ASSETS_DIR = __dirname;

async function screenshot(page, selector, filename) {
  const el = await page.$(selector);
  await el.screenshot({
    path: path.join(ASSETS_DIR, filename),
    omitBackground: true,
  });
  console.log(`  -> ${filename}`);
}

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 840, height: 1200 } });
  const htmlPath = "file:///" + path.join(ASSETS_DIR, "screenshots.html").replace(/\\/g, "/");
  await page.goto(htmlPath);
  await page.waitForLoadState("networkidle");

  console.log("Generating screenshots...");
  await screenshot(page, "#score-card", "demo_scores.png");
  await screenshot(page, "#interview-card", "demo_interview.png");
  await screenshot(page, "#experts-card", "demo_experts.png");

  await browser.close();
  console.log("Done.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
