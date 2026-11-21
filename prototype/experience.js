/* Keep previews visible while loading; show a message only on failure. */
(()=>{const seen=new WeakSet();function scan(){document.querySelectorAll('img').forEach(img=>{if(seen.has(img))return;seen.add(img);img.addEventListener('error',()=>{img.alt=img.alt||'Preview unavailable';},{once:true});});}new MutationObserver(scan).observe(document.body,{childList:true,subtree:true});scan();})();
