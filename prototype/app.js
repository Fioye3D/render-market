/* Design prototype. Local files/viewer use HTTP; accounts and payments are simulated. */
const scenes=new Map();let sceneRequest;
function loadSupportingScenes(){
 if(scenes.size)return Promise.resolve();
 if(sceneRequest)return sceneRequest;
 sceneRequest=new Promise((resolve,reject)=>{
  const script=document.createElement('script');script.src='scenes.js';script.async=true;
  script.onload=()=>{RM_SCENES.forEach(s=>scenes.set(s.id,s));resolve()};
  script.onerror=()=>{script.remove();sceneRequest=null;reject(Error('Supporting screens could not load.'))};
  document.head.append(script);
 });return sceneRequest;
}
const state={saved:new Set(),fields:{},category:'All assets',region:'All places',price:0,sort:'featured',forcedMobile:false,files:false};
let currentScene, toastTimer;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function notify(message){const el=document.querySelector('#toast');el.textContent=message;el.classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.classList.remove('visible'),4200)}
function go(id){if(id.startsWith('detail:')){location.href='asset.html?id='+encodeURIComponent(id.slice(7));return}if(location.hash.slice(1)===id)render();else location.hash=id;}
function matches(){const q=(state.fields.search||'').toLowerCase().trim();return RM_ASSETS.filter(a=>(state.category==='All assets'||a.cat===state.category)&&(state.region==='All places'||(a.region||'').includes(state.region))&&(!q||(a.title+' '+a.creator+' '+a.cat+' '+a.tag+' '+(a.region||'')+' '+(a.desc||'')).toLowerCase().includes(q))&&(!state.price||(a.price!==null&&(state.price===1?a.price<10000:a.price>=10000)))).sort((a,b)=>state.sort==='featured'?0:a.price===null?1:b.price===null?-1:state.sort==='price-asc'?a.price-b.price:b.price-a.price)}
function transformed(source){const s=JSON.parse(JSON.stringify(source));const id=s.id;
 if(id==='explore'||id==='mobile-explore'||id==='saved'){
  const list=id==='saved'?RM_ASSETS.filter(a=>state.saved.has(a.id)):matches();
  const allCards=s.nodes.filter(n=>n.name&&n.name.startsWith('Asset card /'));
  // Remove the contiguous eight-node card groups and their item-specific controls.
  s.nodes=s.nodes.filter((n,i,arr)=>!allCards.some(c=>i>=arr.indexOf(c)&&i<arr.indexOf(c)+8));
  s.hotspots=s.hotspots.filter(h=>!h.assetId&&!h.label.startsWith('View ')&&!h.label.startsWith('Save ')&&!h.label.startsWith('Meet '));
 const mobile=id==='mobile-explore';const cols=mobile?1:id==='saved'?3:4;const w=mobile?350:id==='saved'?428:249;const x0=mobile?20:id==='saved'?56:316;const y0=mobile?457:id==='saved'?305:470;const pitch=mobile?372:id==='saved'?448:314;
 if(mobile&&list.length>2){const oldHeight=s.height;s.height=457+list.length*pitch+130;const delta=s.height-oldHeight;s.nodes.forEach(n=>{if(n.y>=oldHeight-76)n.y+=delta});s.hotspots.forEach(h=>{if(h.y>=oldHeight-76)h.y+=delta});}
 if(id==='saved'&&list.length>3){const oldHeight=s.height;s.height=y0+Math.ceil(list.length/cols)*pitch+120;const delta=s.height-oldHeight;s.nodes.forEach(n=>{if(n.y>=oldHeight-100)n.y+=delta});s.hotspots.forEach(h=>{if(h.y>=oldHeight-100)h.y+=delta});}
  list.forEach((a,i)=>{
   const template=RM_SCENES.find(z=>z.id==='explore');const start=template.nodes.findIndex(n=>n.name==='Asset card / '+a.title);const group=template.nodes.slice(start,start+8);const old=group[0];const x=x0+(i%cols)*(w+24),y=y0+Math.floor(i/cols)*pitch;const dw=w-old.w;
   group.forEach((node,j)=>{const n=JSON.parse(JSON.stringify(node));n.x=x+(n.x-old.x);n.y=y+(n.y-old.y);if(j===0||j===1)n.w+=dw;if(j===0)n.h+=(w-old.w)*.7;if(j===1)n.h=w*.7;if(j>=4)n.y+=(w-old.w)*.7;if(j===2||j===3||j===7)n.x+=dw;if(w>=300&&j>=4)n.size=({4:16,5:12,6:11,7:14})[j];s.nodes.push(n)});
   s.hotspots.push({x,y,w:w-48,h:w*.7+110,label:'View '+a.title,to:'detail:'+a.id},{x:x+w-48,y:y+7,w:44,h:44,label:'Save '+a.title,action:'save:'+a.id},{x:x+12,y:y+w*.7+52,w:w-122,h:32,label:'Meet '+a.creator,to:a.creatorRoute});
  });
 const count=s.nodes.find(n=>n.name==='Results count');if(count)count.text=list.length+' asset'+(list.length===1?'':'s')+(state.category!=='All assets'?' / '+state.category:'');
 const sortLabel=s.nodes.find(n=>n.text==='Sort: Featured  ↓');if(sortLabel)sortLabel.text=state.sort==='price-asc'?'Sort: Price, low to high  ↓':state.sort==='price-desc'?'Sort: Price, high to low  ↓':'Sort: Featured  ↓';
 ['All assets','3D models','Materials','Environments'].forEach((label,i)=>{const box=s.nodes.find(n=>n.type==='rect'&&n.x===56&&n.y===554+i*43);if(box)box.fill=state.category===label?'#285c82':'#101112';});
 const prices=['Any price','Under ₦10,000','₦10,000 and above'];s.nodes.forEach(n=>{const i=prices.findIndex(p=>n.text==='○  '+p);if(i>=0)n.text=(state.price===i?'●  ':'○  ')+prices[i]});
 ['All places','Nigeria','Ghana','Mali'].forEach(label=>{const n=s.nodes.find(n=>n.text==='○  '+label);if(n)n.text=(state.region===label?'●  ':'○  ')+label});
  const mobileCount=s.nodes.find(n=>n.name==='Mobile results count');if(mobileCount)mobileCount.text=list.length+' result'+(list.length===1?'':'s')+' · '+state.category;
  if(!list.length)s.nodes.push({type:'text',x:x0,y:y0+56,text:id==='saved'?'Nothing saved yet. Explore assets and use a save button.':mobile?'No matches. Try a new term or reset filters.':'No matches. Try another search or reset your filters.',size:mobile?14:19,color:'#B2B7C1',font:'Arial',weight:400});
 }
 if(id==='upload-preview'){
  const title=state.fields.title;if(title){const texts=s.nodes.filter(n=>n.type==='text');const a=texts.find(n=>n.text==='Courtyard /'),b=texts.find(n=>n.text==='Earthen scene kit');if(a)a.text=title.split(' / ')[0];if(b)b.text=title.split(' / ')[1]||'';}
  const p=s.nodes.find(n=>n.text==='₦24,000 · Standard licence');if(p&&state.fields.price)p.text='₦'+Number(state.fields.price).toLocaleString('en-NG')+' · Standard licence';
 }
 s.nodes.forEach((n,i)=>{if(n.name&&n.name.startsWith('Asset card /')){const a=RM_ASSETS.find(a=>n.name==='Asset card / '+a.title);if(a&&s.nodes[i+3])s.nodes[i+3].text=state.saved.has(a.id)?'-':'+';}});
 return s;
}
function draw(s){let out=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${s.width} ${s.height}" aria-hidden="true" focusable="false"><rect width="100%" height="100%" fill="${s.background}"/>`;
 s.nodes.forEach((n,i)=>{const {x,y}=n;if(n.type==='rect')out+=`<rect x="${x}" y="${y}" width="${n.w}" height="${n.h}" rx="0" fill="${n.fill}" stroke="${n.stroke||'none'}"/>`;
 else if(n.type==='text')out+=`<text x="${x}" y="${y+n.size*.83}" font-family="${n.font},Arial,sans-serif" font-size="${n.size}" font-weight="${n.weight}" fill="${n.color}">${n.text.split('\n').map((t,j)=>`<tspan x="${x}" dy="${j?n.size*1.2:0}">${esc(t)}</tspan>`).join('')}</text>`;
 else if(n.type==='vector')out+=`<path d="${n.path}" fill="${n.fill}" fill-rule="evenodd" transform="translate(${x},${y}) scale(${n.w/28})"/>`;
 else if(n.type==='image')out+=`<defs><clipPath id="im${i}"><rect x="${x}" y="${y}" width="${n.w}" height="${n.h}" rx="0"/></clipPath></defs><image x="${x}" y="${y}" width="${n.w}" height="${n.h}" href="../assets/${n.w<500?'thumbnails/'+n.file+'.webp':'previews/'+n.file+'-960.webp'}" preserveAspectRatio="xMidYMid slice" clip-path="url(#im${i})"/>`;
 });return out+'</svg>'}
function style(el,r,s){Object.assign(el.style,{left:r.x/s.width*100+'%',top:r.y/s.height*100+'%',width:r.w/s.width*100+'%',height:r.h/s.height*100+'%'})}
function action(a){if(a.startsWith('save:')){const id=a.split(':')[1];if(state.saved.has(id)){state.saved.delete(id);notify('Removed from your sample collection.')}else{state.saved.add(id);notify('Saved to this prototype session.')}render();return;}
 if(a.startsWith('category:')){state.category=a.slice(9);go('explore');render();return}
 if(a.startsWith('query:')){state.fields.search=a.slice(6);state.category='All assets';state.region='All places';state.price=0;go('explore');render();return}
 if(a.startsWith('region:')){state.region=a.slice(7);render();return}
 if(a.startsWith('price:')){state.price=Number(a.slice(6));render();return}
 if(a==='search'){go('explore');render();return}
 if(a==='sort'){state.sort=state.sort==='featured'?'price-asc':'featured';render();return}
 if(a==='draft'){notify('Demo draft kept in this browser session.');return}
 if(a==='attach'){state.files=true;notify('Sample files attached for this simulation. No real upload occurred.');return}
 if(a==='menu'){document.querySelector('#menu-dialog').showModal();return}
 if(a==='mobile-filter'){document.querySelector('#filter-dialog').showModal()}
}
function validate(to){if(to==='upload-2'&&!(state.fields.title??'Courtyard / Earthen scene kit').trim()){notify('Add an asset title before continuing.');return false}
 if(to==='upload-3'&&!state.files){notify('Attach the supplied sample files to continue.');return false}
 if(to==='upload-preview'&&(state.fields.price!==undefined)&&(!Number.isFinite(Number(state.fields.price))||Number(state.fields.price)<0||state.fields.price.trim()==='')){notify('Enter a price of zero or greater.');return false}return true}
function render(){const [route,query]=location.hash.slice(1).split('?');const requested=decodeURIComponent(route||'home');if(query&&new URLSearchParams(query).has('search'))state.fields.search=new URLSearchParams(query).get('search');const mobile=state.forcedMobile||innerWidth<=600;let id=requested;
 if((requested==='home'||requested==='explore')&&window.renderMarketplace){window.renderMarketplace(requested,{state,matches,go,action});document.querySelector('#size-toggle').textContent=state.forcedMobile?'Desktop view':'Mobile view';return}
 if(!scenes.size){
  const host=document.querySelector('#artboard');host.classList.add('native-artboard');
  host.innerHTML='<section class="route-loading" role="status" aria-busy="true"><h1>Loading workspace</h1><div class="route-skeleton"><span></span><span></span><span></span></div></section>';
  loadSupportingScenes().then(render).catch(()=>{host.innerHTML='<section class="route-loading" role="alert"><h1>Connection interrupted</h1><p>Reload to retry, or return to the asset library.</p><a href="#explore">Explore assets</a></section>'});return;
 }
 if(mobile&&scenes.has('mobile-'+requested))id='mobile-'+requested;
 const src=scenes.get(id)||scenes.get('home');currentScene=transformed(src);const s=currentScene;const el=document.querySelector('#artboard');el.classList.remove('native-artboard');el.classList.toggle('mobile',s.width===390);el.innerHTML=draw(s);el.setAttribute('aria-label',s.title);
 const description=document.createElement('section');description.className='sr-only';description.innerHTML='<h1>'+esc(s.title)+'</h1>'+s.nodes.filter(n=>n.type==='text').map(n=>'<p>'+esc(n.text)+'</p>').join('');el.append(description);
 s.hotspots.forEach(h=>{const b=document.createElement(h.to||h.url?'a':'button');b.className='hotspot';b.setAttribute('aria-label',h.label);b.title=h.label;if(h.url){b.href=h.url;b.target='_blank';b.rel='noopener noreferrer'}else if(h.to)b.href='#'+h.to;else b.type='button';style(b,h,s);if(!h.url)b.onclick=e=>{e.preventDefault();if(h.action)action(h.action);else if(h.to&&validate(h.to)){if(h.label==='Reset filters'){state.category='All assets';state.region='All places';state.price=0;state.fields.search='';state.sort='featured';}go(h.to)}};el.append(b)});
 const scale=el.getBoundingClientRect().width/s.width;
 (s.inputs||[]).forEach(r=>{const input=document.createElement(r.multiline?'textarea':'input');input.setAttribute('aria-label',r.label);input.name=r.key;input.value=state.fields[r.key]??r.value;input.placeholder=r.placeholder;style(input,r,s);input.style.fontSize=(14*scale)+'px';input.style.padding=(r.multiline?12*scale+'px':'0')+' '+14*scale+'px';input.oninput=()=>{state.fields[r.key]=input.value;el.querySelectorAll('[name="'+r.key+'"]').forEach(other=>{if(other!==input)other.value=input.value})};input.onkeydown=e=>{if(e.key==='Enter'&&r.key==='search'){e.preventDefault();action('search')}};el.append(input)});
 (s.selects||[]).forEach(r=>{const select=document.createElement('select');select.setAttribute('aria-label',r.label);r.options.forEach(([value,label])=>{const option=document.createElement('option');option.value=value;option.textContent=label;select.append(option)});select.value=state[r.key];style(select,r,s);select.style.fontSize=14*scale+'px';select.style.padding='0 '+14*scale+'px';select.onchange=()=>{state[r.key]=select.value;render()};el.append(select)});
 document.querySelector('#screen-title').textContent=s.title;document.title=s.title+'  /  RenderMarket';document.querySelector('#size-toggle').textContent=state.forcedMobile?'Desktop view':'Mobile view';
}
document.querySelector('#size-toggle').onclick=()=>{state.forcedMobile=!state.forcedMobile;render()};document.querySelector('#close-menu').onclick=()=>document.querySelector('#menu-dialog').close();document.querySelectorAll('dialog a').forEach(a=>a.onclick=()=>document.querySelector('#menu-dialog').close());
document.querySelector('.skip').onclick=e=>{e.preventDefault();document.querySelector('#artboard').focus();document.querySelector('#artboard').scrollIntoView()};
const filterDialog=document.createElement('dialog');filterDialog.id='filter-dialog';filterDialog.setAttribute('aria-label','Filter by asset type');filterDialog.innerHTML='<h2>Find your asset type</h2>'+['All assets','3D models','Materials','Environments'].map(c=>'<button type="button" data-category="'+c+'" style="display:block;width:100%;margin-top:12px">'+c+'</button>').join('')+'<button type="button" id="close-filter">Close filters</button>';document.body.append(filterDialog);filterDialog.querySelectorAll('[data-category]').forEach(b=>b.onclick=()=>{state.category=b.dataset.category;filterDialog.close();render();notify('Filter: '+state.category)});filterDialog.querySelector('#close-filter').onclick=()=>filterDialog.close();
addEventListener('hashchange',()=>{render();scrollTo(0,0);document.querySelector('#artboard').focus({preventScroll:true})});let viewportWidth=innerWidth,resizeTimer;addEventListener('resize',()=>{if(innerWidth===viewportWidth)return;viewportWidth=innerWidth;clearTimeout(resizeTimer);resizeTimer=setTimeout(render,120)});render();
