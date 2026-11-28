const { chromium } = require('playwright');
const fs = require('fs');
const S = '/tmp/claude-0/-home-user-aaa/8f7db5b8-5a69-55d2-b941-b1906915517c/scratchpad';
const P = S + '/deck/project';
const OUT = S + '/deckcheck';
const css = fs.readFileSync(P + '/deck.css', 'utf8');
const order = JSON.parse(fs.readFileSync(P + '/deck.json', 'utf8')).order;
const only = process.argv.slice(2);
const harness = `
html,body{margin:0;padding:0;background:#888}
section{width:1920px;height:1080px;position:relative;overflow:hidden}
section[hidden]{display:flex}
aside{display:none}
*{animation:none !important}
x-shape{display:block}
x-shape[kind="arrow-right"]{clip-path:polygon(0 30%,60% 30%,60% 0,100% 50%,60% 100%,60% 70%,0 70%)}
x-icon,x-connector{display:block}
h1,h2,h3,p,ul{margin:0}
`;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const report = {};
  const list = only.length ? only : order;
  for (let i = 0; i < list.length; i++) {
    const id = list[i];
    const html = fs.readFileSync(`${P}/slides/${id}.html`, 'utf8');
    const idx = order.indexOf(id);
    // counter: set page counter so page number equals position
    const pre = `<style>body{counter-reset: page ${idx}}</style>`;
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>${css}</style><style>${harness}</style>${pre}</head><body>${html}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: `${OUT}/shots/${id}.png` });
    report[id] = await page.evaluate(() => {
      const sec = document.querySelector('section');
      const res = { overflowRight: [], overflowBottom: [], smallFont: [], textPastBox: [], title: null, contentBottom: 0, gaps: [] };
      const t = sec.querySelector('.title, .head');
      const tt = sec.querySelector('.title');
      if (tt) { const r = tt.getBoundingClientRect(); res.title = [Math.round(r.top), Math.round(r.bottom)]; }
      const walker = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = walker.nextNode())) {
        if (!n.textContent.trim()) continue;
        const el = n.parentElement;
        if (el.closest('aside')) continue;
        const cs = getComputedStyle(el);
        const fs = parseFloat(cs.fontSize);
        const txt = n.textContent.trim().slice(0, 30);
        if (fs < 24) res.smallFont.push([txt, fs]);
        const range = document.createRange(); range.selectNodeContents(n);
        const rects = [...range.getClientRects()];
        const isFooter = !!el.closest('.footer');
        for (const r of rects) {
          if (r.right > 1792.5) res.overflowRight.push([txt, Math.round(r.right)]);
          if (!isFooter && r.bottom > 920.5) res.overflowBottom.push([txt, Math.round(r.bottom)]);
          if (!isFooter) res.contentBottom = Math.max(res.contentBottom, Math.round(r.bottom));
        }
        // text past its own block box
        const block = el.closest('p,h1,h2,h3,li,td,th,div');
        const br = block.getBoundingClientRect();
        for (const r of rects) {
          if (r.right > br.right + 1 || r.left < br.left - 1) res.textPastBox.push([txt, Math.round(r.left), Math.round(r.right), Math.round(br.left), Math.round(br.right)]);
        }
      }
      // non-text elements bottoms/right
      for (const el of sec.querySelectorAll('div,svg,x-shape,table,hr,img')) {
        const r = el.getBoundingClientRect();
        if (r.width === 0) continue;
        if (r.right > 1792.5 && !el.matches('svg') ) res.overflowRight.push(['<' + el.tagName + ' ' + el.className + '>', Math.round(r.right)]);
        if (el.matches('svg') && r.right > 1792.5) res.overflowRight.push(['<svg>', Math.round(r.right)]);
        if (r.bottom > 920.5 && !el.closest('.footer')) res.overflowBottom.push(['<' + el.tagName + ' ' + (el.className.baseVal ?? el.className) + '>', Math.round(r.bottom)]);
        const painted = el.matches('.card,.card-ink,.tile,.step,.step-hl,.chart,table,hr,x-shape,.bar,.bar-up,.bar-down,.bar-focus,.track,.chip,img') || (el.matches('svg') && !el.closest('.chart') && !sec.classList.contains('s-dark'));
        if (painted && !el.closest('.footer')) res.contentBottom = Math.max(res.contentBottom, Math.round(r.bottom));
        if (el.matches('.body,.row,.col,.grid-2,.grid-3,.grid-4') && el.scrollHeight > el.clientHeight + 1) res.overflowBottom.push(['scroll '+el.className, el.scrollHeight - el.clientHeight]);
      }
      const body = sec.querySelector('.body');
      if (body) {
        const kids = [...body.children].filter(k => k.tagName !== 'ASIDE');
        for (let i = 1; i < kids.length; i++) {
          const a = kids[i - 1].getBoundingClientRect(), b = kids[i].getBoundingClientRect();
          res.gaps.push(Math.round(b.top - a.bottom));
        }
        const br = body.getBoundingClientRect();
        res.body = [Math.round(br.top), Math.round(br.bottom)];
      }
      return res;
    });
  }
  await browser.close();
  fs.writeFileSync(`${OUT}/report${only.length ? '-partial' : ''}.json`, JSON.stringify(report, null, 1));
  for (const [id, r] of Object.entries(report)) {
    const issues = [];
    if (r.overflowRight.length) issues.push('RIGHT ' + JSON.stringify(r.overflowRight));
    if (r.overflowBottom.length) issues.push('BOTTOM ' + JSON.stringify(r.overflowBottom));
    if (r.smallFont.length) issues.push('SMALL ' + JSON.stringify(r.smallFont));
    if (r.textPastBox.length) issues.push('PASTBOX ' + JSON.stringify(r.textPastBox));
    console.log(id, 'title', JSON.stringify(r.title), 'bottom', r.contentBottom, 'gaps', JSON.stringify(r.gaps), issues.join(' | '));
  }
})();
