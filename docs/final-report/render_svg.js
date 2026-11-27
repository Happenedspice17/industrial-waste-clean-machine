// Render build-docx/svg_N.svg to build-docx/svg_N.png (2x) for the Word version.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const [dir, n] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  for (let i = 0; i < Number(n); i++) {
    const svg = fs.readFileSync(path.join(dir, `svg_${i}.svg`), 'utf8');
    await page.setContent(`<html><body style="margin:0;background:#fff;width:900px">${svg}</body></html>`);
    await page.locator('svg').first().screenshot({ path: path.join(dir, `svg_${i}.png`) });
  }
  await browser.close();
})();
