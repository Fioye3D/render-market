/* Responsive, semantic home and asset library. Shared catalogue/state with the design prototype. */

window.renderMarketplace=(page,{state,matches,go,action})=>{

 const e=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

 const count=type=>RM_ASSETS.filter(a=>a.cat===type).length;

 const mark='<svg viewBox="0 0 32 36" aria-hidden="true"><path fill="#dce4ec" d="M2 7 16 0l14 8-14 8Z"/><path fill="#7995ad" d="m2 7 14 9v20L2 28Z"/><path fill="#477da4" d="m16 16 14-8v14l-7 4 7 10H19L9 22Z"/><path fill="#c4ccd3" d="m16 16 7 4 7-4v6l-7 4-7-4Z"/></svg>';

 const search=(label,hero=false)=>'<form class="m-search '+(hero?'m-search-hero':'')+'" role="search"><input class="m-search-field" aria-label="'+label+'" value="'+e(state.fields.search||'')+'" placeholder="'+(hero?'Search models, materials and scenes':'Search the library')+'" autocomplete="off"><button aria-label="'+(hero?'Search library':'Submit search')+'">'+(hero?'Search assets':'Search')+'</button></form>';

 const card=a=>'<article class="m-card"><div class="m-card-preview"><a href="asset.html?id='+a.id+'" aria-label="View '+e(a.title)+'"><img loading="lazy" decoding="async" width="560" height="420" src="../assets/thumbnails/'+a.file+'.webp" alt="'+e(a.title)+'"></a><button class="m-save" data-save="'+a.id+'" aria-label="'+(state.saved.has(a.id)?'Remove saved ':'Save ')+e(a.title)+'" aria-pressed="'+state.saved.has(a.id)+'">'+(state.saved.has(a.id)?'-':'+')+'</button></div><div class="m-card-info"><a class="m-card-title" href="asset.html?id='+a.id+'">'+e(a.title)+'</a><a class="m-card-creator" href="#'+a.creatorRoute+'">'+e(a.creator)+' <span>↗</span></a><div class="m-card-meta"><span>BLEND · GLB</span><strong>'+(a.price===null?'Portfolio scene':'₦'+a.price.toLocaleString('en-NG'))+'</strong></div><div class="m-card-place">'+e(a.placeLabel||a.region||'Object study')+'</div></div></article>';

 const radio=(group,label,value,selected)=>'<label class="m-option"><input type="radio" name="'+group+'" value="'+e(value)+'" '+(selected?'checked':'')+'><span>'+e(label)+'</span></label>';

 const nav='<header class="m-header"><a href="#home" class="m-brand">'+mark+'<span>RenderMarket</span></a><nav aria-label="Marketplace navigation"><a href="#explore" '+(page==='explore'?'aria-current="page"':'')+'>Explore</a><a href="#creator">Creators</a></nav>'+search('Search marketplace')+'<a href="#saved" class="m-saved-link">Saved <span>'+state.saved.size+'</span></a><a href="#register" class="m-studio-link">Creator studio ↗</a></header>';

 const categories=[['Models & props','3D models',count('3D models')],['Materials & textiles','Materials',count('Materials')],['Environments','Environments',count('Environments')],['All assets','All assets',RM_ASSETS.length]];

 let content='';

 if(page==='home'){

  const picks=['canteen','barbershop','market','suya','church','school','classroom','akara-vendor'];

  content='<section class="m-hero"><div class="m-hero-copy"><p class="m-eyebrow">THE AFRICAN DIGITAL ASSET LIBRARY</p><h1>African creativity.<br>Built in 3D.</h1><p class="m-description">Scenes, models and materials from African creative worlds. Inspect the details, meet the creators and download the source files.</p><div class="m-hero-actions"><a class="m-primary" href="#explore">Explore assets</a><a href="asset.html?id=sanctuary">Try the 3D viewer</a></div>'+search('Find your next asset',true)+'<div class="m-suggestions"><span>Try</span><button data-query="danfo">Danfo</button><button data-query="stripe">Woven textiles</button><button data-query="lagos everyday">Lagos scenes</button></div></div><a class="m-feature" href="asset.html?id=sanctuary"><img src="../assets/previews/sanctuary-temple-960.webp" srcset="../assets/previews/sanctuary-temple-480.webp 480w, ../assets/previews/sanctuary-temple-960.webp 960w, ../assets/previews/sanctuary-temple-1440.webp 1440w" sizes="(max-width:700px) 100vw, 55vw" fetchpriority="high" decoding="async" width="960" height="540" alt="Sanctuary Temple forest scene"><div><span>FEATURED ENVIRONMENT</span><strong>Sanctuary Temple</strong><small>Inspect scene in 3D ↗</small></div></a></section><section class="m-section"><div class="m-section-heading"><h2>Browse asset categories</h2><a href="#explore">View all assets ↗</a></div><div class="m-categories">'+categories.map(([title,type,n],i)=>'<button data-category="'+type+'"><img src="../assets/thumbnails/'+['danfo-minibus','kente-strip-study','lagos-canteen','sanctuary-temple'][i]+'.webp" alt="" width="64" height="64" loading="lazy"><span>'+title+'<small>'+n+' assets</small></span></button>').join('')+'</div></section><section class="m-section"><div class="m-section-heading"><div><p class="m-eyebrow">NEW COLLECTION</p><h2>Everyday Lagos</h2><p class="m-muted">Canteens, neighbourhood spaces and food scenes.</p></div><a href="#explore?search=lagos%20everyday">View all 10 ↗</a></div><div class="m-grid">'+picks.map(id=>card(RM_ASSETS.find(a=>a.id===id))).join('')+'</div></section><section class="m-section"><div class="m-section-heading"><h2>Creator profiles</h2><span class="m-muted">Browse each catalogue</span></div><div class="m-creators">'+[['AF','Adefioye Favour','Sanctuary Temple','creator:owner'],['NF','Nia Forms','Spaces & objects','creator'],['SM','Sefi Materials','Procedural textiles','creator:sefi']].map(([initials,name,role,to])=>'<a href="#'+to+'"><span class="m-avatar">'+initials+'</span><div><strong>'+name+'</strong><small>'+role+'</small></div><span>↗</span></a>').join('')+'</div></section><section class="m-creator-cta"><div><h2>Publish your work</h2><p>Prepare files, previews and licensing in one listing workflow.</p></div><a href="#register">View creator workflow →</a></section>';

  content+='<section class="m-section"><div class="m-section-heading"><div><p class="m-eyebrow">OBJECTS / MATERIALS / CRAFT</p><h2>Explore the collection</h2></div><a href="#explore">Browse all '+RM_ASSETS.length+' assets</a></div><div class="m-grid">'+["orbit", "loop", "kente", "baobab"].map(id=>RM_ASSETS.find(a=>a.id===id)).filter(Boolean).map(card).join('')+'</div></section>';
 }else{

  const list=matches();

  content='<section class="m-library-heading"><p class="m-eyebrow">ASSET LIBRARY</p><h1>Explore assets</h1><p class="m-muted">Models, materials and environments with downloadable source files.</p>'+search('Search assets',true)+'<div class="m-suggestions"><span>Browse</span><button data-query="lagos everyday">Everyday Lagos · 10 assets</button><button data-query="characters">With characters</button></div></section><div class="m-library"><aside class="m-filters"><div class="m-filter-heading"><strong>Filters</strong><button data-reset>Reset</button></div><fieldset><legend>Asset type</legend>'+['All assets','3D models','Materials','Environments'].map(c=>radio('category',c,c,state.category===c)).join('')+'</fieldset><fieldset><legend>Price</legend>'+[['Any price',0],['Under ₦10,000',1],['₦10,000 and above',2]].map(([label,v])=>radio('price',label,v,state.price===v)).join('')+'</fieldset><fieldset><legend>Place reference</legend>'+['All places','Nigeria','Ghana','Mali','Tanzania','Kenya','Guinea','Senegal'].map(c=>radio('region',c,c,state.region===c)).join('')+'</fieldset><div class="m-compatibility"><span>Source software</span><strong>Blender 4.2</strong><small>Portable GLB, OBJ and FBX exports are listed on each asset page.</small></div></aside><section class="m-results" aria-label="Asset results"><div class="m-results-header"><strong role="status">'+list.length+' '+(list.length===1?'asset':'assets')+'</strong><label>Sort by <select aria-label="Sort assets"><option value="featured" '+(state.sort==='featured'?'selected':'')+'>Featured</option><option value="price-asc" '+(state.sort==='price-asc'?'selected':'')+'>Price: low to high</option><option value="price-desc" '+(state.sort==='price-desc'?'selected':'')+'>Price: high to low</option></select></label></div>'+(list.length?'<div class="m-grid">'+list.map(card).join('')+'</div>':'<div class="m-empty"><h2>No matching assets</h2><p>Try a different search or reset the filters.</p><button data-reset>Reset filters</button></div>')+'</section></div>';

 }

 const root=document.querySelector('#artboard');root.classList.add('native-artboard');root.classList.toggle('mobile',state.forcedMobile);root.innerHTML='<div class="m-shell">'+nav+'<div class="m-main">'+content+'<footer class="m-footer"><span>RenderMarket · Independent portfolio project</span><span>Sample catalogue prices and creator profiles. File downloads are available.</span></footer></div><nav class="m-mobile-nav" aria-label="Mobile navigation"><a href="#home" '+(page==='home'?'aria-current="page"':'')+'>Home</a><a href="#explore" '+(page==='explore'?'aria-current="page"':'')+'>Explore</a><a href="#saved">Saved '+state.saved.size+'</a><a href="#register">Creator studio</a></nav></div>';

 root.querySelectorAll('.m-search').forEach(form=>form.onsubmit=event=>{event.preventDefault();state.fields.search=form.querySelector('.m-search-field').value;go('explore')});

 root.querySelectorAll('[data-save]').forEach(b=>b.onclick=()=>action('save:'+b.dataset.save));

 root.querySelectorAll('[data-query]').forEach(b=>b.onclick=()=>action('query:'+b.dataset.query));

 root.querySelectorAll('[data-category]').forEach(b=>b.onclick=()=>{state.fields.search='';state.region='All places';state.price=0;action('category:'+b.dataset.category)});

 root.querySelectorAll('input[type=radio]').forEach(input=>input.onchange=()=>{state[input.name]=input.name==='price'?Number(input.value):input.value;window.renderMarketplace(page,{state,matches,go,action})});

 const sort=root.querySelector('select');if(sort)sort.onchange=()=>{state.sort=sort.value;window.renderMarketplace(page,{state,matches,go,action})};

 root.querySelectorAll('[data-reset]').forEach(b=>b.onclick=()=>{state.fields.search='';state.region='All places';state.category='All assets';state.price=0;state.sort='featured';history.replaceState(null,'','#explore');window.renderMarketplace(page,{state,matches,go,action})});

 document.querySelector('#screen-title').textContent=page==='home'?'RenderMarket marketplace':'Explore assets';document.title=(page==='home'?'RenderMarket':'Explore assets')+' | 3D asset portfolio';

};
