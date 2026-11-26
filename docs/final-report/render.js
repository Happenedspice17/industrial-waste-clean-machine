// Render the pandoc HTML to an A4 PDF with page numbers (Chromium via Playwright).
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [src, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(src), { waitUntil: 'load' });
  await page.pdf({
    path: out,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate:
      '<div style="font:7.5px Inter,sans-serif;color:#7a828c;width:100%;padding:0 18mm;display:flex;justify-content:space-between">' +
      '<span>Autonomous Robot for Industrial Waste Cleaning and Separation · Technical report</span>' +
      '<span>github.com/Happenedspice17/industrial-waste-clean-machine</span></div>',
    footerTemplate:
      '<div style="font:7.5px Inter,sans-serif;color:#7a828c;width:100%;padding:0 18mm;display:flex;justify-content:space-between">' +
      '<span>Universidad Panamericana · Proyecto Mecatrónico I · Fall 2026</span>' +
      '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: '18mm', bottom: '18mm', left: '18mm', right: '18mm' },
  });
  await browser.close();
})();
