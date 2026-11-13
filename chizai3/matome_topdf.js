const {chromium}=require('playwright');
(async()=>{
  const [,,src,css,out]=process.argv;
  const b=await chromium.launch(); const p=await b.newPage();
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r=>r.abort());
  await p.goto('file://'+src,{waitUntil:'load'});
  await p.addStyleTag({path:css});
  await p.emulateMedia({media:'print'});
  await p.pdf({path:out, format:'A4', printBackground:true, preferCSSPageSize:true,
    displayHeaderFooter:true, headerTemplate:'<span></span>',
    footerTemplate:'<div style="width:100%;font-size:8px;color:#666;text-align:center;font-family:IPAPGothic">知財検定3級 法令まとめ　<span class="pageNumber"></span> / <span class="totalPages"></span></div>'});
  await b.close();
})();
