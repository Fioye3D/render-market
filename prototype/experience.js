/* Keep previews visible while loading; show a message only on failure. */
(()=>{const seen=new WeakSet();function scan(){document.querySelectorAll('img').forEach(img=>{if(seen.has(img))return;seen.add(img);img.addEventListener('error',()=>{img.alt=img.alt||'Preview unavailable';},{once:true});});}new MutationObserver(scan).observe(document.body,{childList:true,subtree:true});scan();})();

/* Only one header disclosure may be open at a time, including dynamically rendered routes. */
document.addEventListener('toggle',event=>{
 const menu=event.target;
 if(!(menu instanceof HTMLDetailsElement)||!menu.open||!menu.closest('.wc-header'))return;
 menu.closest('.wc-header').querySelectorAll('details[open]').forEach(other=>{if(other!==menu)other.open=false;});
},true);
