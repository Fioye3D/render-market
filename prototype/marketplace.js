/* Responsive, semantic home and asset library. Shared catalogue/state with the design prototype. */

window.renderMarketplace=(page,{state,matches,go,action})=>{

 const e=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

 const count=type=>RM_ASSETS.filter(a=>a.cat===type).length;

 const mark='<svg viewBox="0 0 32 36" aria-hidden="true"><path fill="#dce4ec" d="M2 7 16 0l14 8-14 8Z"/><path fill="#7995ad" d="m2 7 14 9v20L2 28Z"/><path fill="#477da4" d="m16 16 14-8v14l-7 4 7 10H19L9 22Z"/><path fill="#c4ccd3" d="m16 16 7 4 7-4v6l-7 4-7-4Z"/></svg>';

 const search=(label,hero=false)=>'<form class="m-search '+(hero?'m-search-hero':'')+'" role="search"><input class="m-search-field" aria-label="'+label+'" value="'+e(state.fields.search||'')+'" placeholder="'+(hero?'Search models, materials and scenes':'Search the library')+'" autocomplete="off"><button aria-label="'+(hero?'Search library':'Submit search')+'">'+(hero?'Search assets':'Search')+'</button></form>';

 const card=a=>'<article class="m-card"><div class="m-card-preview"><a href="asset.html?id='+a.id+'" aria-label="View '+e(a.title)+'"><img loading="lazy" decoding="async" width="560" height="420" src="../assets/thumbnails/'+a.file+'.webp" alt="'+e(a.title)+'"></a><button class="m-save" data-save="'+a.id+'" aria-label="'+(state.saved.has(a.id)?'Remove saved ':'Save ')+e(a.title)+'" aria-pressed="'+state.saved.has(a.id)+'">'+(state.saved.has(a.id)?'-':'+')+'</button></div><div class="m-card-info"><a class="m-card-title" href="asset.html?id='+a.id+'">'+e(a.title)+'</a><a class="m-card-creator" href="#'+a.creatorRoute+'">'+e(a.creator)+' <span>↗</span></a><div class="m-card-meta"><span>BLEND · GLB</span><strong>'+(a.price===null?'Portfolio scene':'₦'+a.price.toLocaleString('en-NG'))+'</strong></div><div class="m-card-place">'+(a.collection==='rural-worlds'?'Procedural study · ':'')+e(a.placeLabel||a.region||'Object study')+'</div></div></article>';

 const radio=(group,label,value,selected)=>'<label class="m-option"><input type="radio" name="'+group+'" value="'+e(value)+'" '+(selected?'checked':'')+'><span>'+e(label)+'</span></label>';

 const nav='<header class="m-header"><a href="#home" class="m-brand">'+mark+'<span>RenderMarket</span></a><nav aria-label="Marketplace navigation"><a href="#home" '+(page==='home'?'aria-current="page"':'')+'>Home</a><a href="#explore" '+(page==='explore'?'aria-current="page"':'')+'>Marketplace</a><a href="#creator">Creators</a></nav>'+search('Search marketplace')+'<a href="#saved" class="m-saved-link">Saved <span>'+state.saved.size+'</span></a><a href="#register" class="m-studio-link">Creator studio ↗</a></header>';

 const categories=[['Models & props','3D models',count('3D models')],['Materials & textiles','Materials',count('Materials')],['Environments','Environments',count('Environments')],['All assets','All assets',RM_ASSETS.length]];

 let content='';


 if(page==='home'){
 content=`<section class="w-listing" aria-labelledby="listing-title"><div class="w-listing-header"><img class="w-app-icon" src="../assets/logo/logo-dark.svg" width="88" height="88" alt="RenderMarket"><div><h1 id="listing-title">RenderMarket</h1><a class="w-publisher" href="#creator:owner">Adefioye Favour / fioye_3d</a><div class="w-tags"><a href="#explore">3D assets</a><button data-category="Environments">Environments</button><button data-category="Materials">Materials</button></div></div></div><div class="w-actions"><a class="w-primary" href="#explore">Explore the marketplace</a><a href="asset.html?id=sanctuary">Open the 3D viewer</a></div><p class="w-summary">Discover 3D scenes, models and materials inspired by African places, objects and creative perspectives.</p><p class="w-note">Independent UI/UX portfolio project. Purchasing and account services are being prepared.</p></section>
 <section class="w-description" aria-label="About RenderMarket"><p>RenderMarket brings together environments, props and material studies for artists building digital worlds. Browse the collection, review file information and inspect actual geometry in the browser.</p><p>The catalogue includes contemporary Lagos settings, rural environments, agricultural scenes and original imagined worlds. Sanctuary Temple is the featured original scene by Adefioye Favour.</p><p>Each listing explains its formats, source and limitations. Generated catalogue studies are labelled as samples. The library currently contains ${RM_ASSETS.length} listings; checkout is unavailable while secure paid delivery is configured.</p><p class="w-categories">Categories: <button data-category="3D models">3D models</button><button data-category="Materials">Materials &amp; textures</button><button data-category="Environments">Environments</button></p></section>
 <section class="w-related" aria-labelledby="related-heading"><div class="m-section-heading"><h2 id="related-heading">Explore the collection</h2><a href="#explore">View all ${RM_ASSETS.length} listings</a></div><div class="m-grid">${['sanctuary','rural-village','royal-courtyard','river-landscape','yam-farm','cocoa-farm','courtyard-mosque','herbalist-shrine'].map(id=>RM_ASSETS.find(a=>a.id===id)).map(card).join('')}</div></section><section class="w-related"><div class="m-section-heading"><h2>Related collections</h2></div><div class="w-collection-links"><a href="#explore?search=lagos%20everyday">Everyday Lagos <span>Canteens, markets and neighbourhood spaces</span></a><a href="#explore?search=rural%20worlds">Rural Worlds <span>Villages, farms and gathering places</span></a></div></section>`;
 }else{

  const list=page==='saved'?RM_ASSETS.filter(a=>state.saved.has(a.id)):matches();

  content='<section class="m-library-heading"><p class="m-eyebrow">ASSET LIBRARY</p><h1>Explore assets</h1><p class="m-muted">Models, materials and environments with downloadable source files.</p>'+search('Search assets',true)+'<div class="m-suggestions"><span>Browse</span><button data-query="lagos everyday">Everyday Lagos · 10 assets</button><button data-query="characters">With characters</button></div></section><div class="m-library"><aside class="m-filters"><div class="m-filter-heading"><strong>Filters</strong><button data-reset>Reset</button></div><fieldset><legend>Asset type</legend>'+['All assets','3D models','Materials','Environments'].map(c=>radio('category',c,c,state.category===c)).join('')+'</fieldset><fieldset><legend>Price</legend>'+[['Any price',0],['Under ₦10,000',1],['₦10,000 and above',2]].map(([label,v])=>radio('price',label,v,state.price===v)).join('')+'</fieldset><fieldset><legend>Place reference</legend>'+['All places','Nigeria','Ghana','Mali','Tanzania','Kenya','Guinea','Senegal'].map(c=>radio('region',c,c,state.region===c)).join('')+'</fieldset><div class="m-compatibility"><span>Source software</span><strong>Blender 4.2</strong><small>Portable GLB, OBJ and FBX exports are listed on each asset page.</small></div></aside><section class="m-results" aria-label="Asset results"><div class="m-results-header"><strong role="status">'+list.length+' '+(list.length===1?'asset':'assets')+'</strong><label>Sort by <select aria-label="Sort assets"><option value="featured" '+(state.sort==='featured'?'selected':'')+'>Featured</option><option value="price-asc" '+(state.sort==='price-asc'?'selected':'')+'>Price: low to high</option><option value="price-desc" '+(state.sort==='price-desc'?'selected':'')+'>Price: high to low</option></select></label></div>'+(list.length?'<div class="m-grid">'+list.map(card).join('')+'</div>':'<div class="m-empty"><h2>No matching assets</h2><p>Try a different search or reset the filters.</p><button data-reset>Reset filters</button></div>')+'</section></div>';

 }

 document.body.dataset.page=page;const root=document.querySelector('#artboard');root.classList.add('native-artboard');root.classList.toggle('mobile',state.forcedMobile);root.innerHTML='<div class="m-shell">'+nav+'<div class="m-main">'+content+'<footer class="m-footer"><span>RenderMarket · Independent portfolio project</span><span>Portfolio catalogue. Purchasing is not available yet.</span></footer></div><nav class="m-mobile-nav" aria-label="Mobile navigation"><a href="#home" '+(page==='home'?'aria-current="page"':'')+'>Home</a><a href="#explore" '+(page==='explore'?'aria-current="page"':'')+'>Explore</a><a href="#saved">Saved '+state.saved.size+'</a><a href="#register">Creator studio</a></nav></div>';

 root.querySelectorAll('.m-search').forEach(form=>form.onsubmit=event=>{event.preventDefault();state.fields.search=form.querySelector('.m-search-field').value;go('explore')});

 root.querySelectorAll('[data-save]').forEach(b=>b.onclick=()=>action('save:'+b.dataset.save));

 root.querySelectorAll('[data-query]').forEach(b=>b.onclick=()=>action('query:'+b.dataset.query));

 root.querySelectorAll('[data-category]').forEach(b=>b.onclick=()=>{state.fields.search='';state.region='All places';state.price=0;action('category:'+b.dataset.category)});

 root.querySelectorAll('input[type=radio]').forEach(input=>input.onchange=()=>{state[input.name]=input.name==='price'?Number(input.value):input.value;window.renderMarketplace(page,{state,matches,go,action})});

 const sort=root.querySelector('select');if(sort)sort.onchange=()=>{state.sort=sort.value;window.renderMarketplace(page,{state,matches,go,action})};

 root.querySelectorAll('[data-reset]').forEach(b=>b.onclick=()=>{state.fields.search='';state.region='All places';state.category='All assets';state.price=0;state.sort='featured';history.replaceState(null,'','#explore');window.renderMarketplace(page,{state,matches,go,action})});

 document.querySelector('#screen-title').textContent=page==='home'?'RenderMarket marketplace':'Explore assets';document.title=(page==='home'?'RenderMarket':'Explore assets')+' | 3D asset portfolio';

};
