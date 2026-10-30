/* Local Figma development plugin. Creates new pages; never edits existing nodes. */
figma.showUI(__html__,{width:440,height:410,themeColors:true});
let active=false;
figma.ui.onmessage=async message=>{
 if(message.type!=='build'||active)return;active=true;
 try{await build(message.payload);active=false}catch(error){active=false;figma.ui.postMessage({type:'error',message:'Build stopped: '+error.message+'\nExisting pages were preserved. Inspect newly created RM pages before retrying.'})}
};
const rgb=hex=>({r:parseInt(hex.slice(1,3),16)/255,g:parseInt(hex.slice(3,5),16)/255,b:parseInt(hex.slice(5,7),16)/255});
const solid=hex=>({type:'SOLID',color:rgb(hex)});
async function build(payload){
 const token=payload.tokens,fonts={},images={},styles={},variables={},components={},frameMap={},pending=[];
 const stamp='RM v0.4';
 // All screens and interactions use one page because Figma prototypes are per-page.
 const pages={};for(const [key,name]of Object.entries({Overview:'00 / Cover',Foundations:'01 / Foundations',Components:'02 / Components',Wireframes:'03 / Wireframes','High fidelity':'04 / Screens & prototype',Mobile:'04 / Screens & prototype'})){
  if(!Object.values(pages).some(p=>p.name===stamp+' / '+name)){const p=figma.createPage();p.name=stamp+' / '+name;pages[key]=p}else pages[key]=Object.values(pages).find(p=>p.name===stamp+' / '+name);
 }
 const library=figma.createPage();library.name=stamp+' / 05 / Reusable library';
 const collection=figma.variables.createVariableCollection(stamp+' / Colour tokens');
 for(const [name,hex]of Object.entries(token.color)){const v=figma.variables.createVariable(stamp+'/'+name,collection,'COLOR');v.setValueForMode(collection.defaultModeId,rgb(hex));variables[hex]=v;const st=figma.createPaintStyle();st.name=stamp+'/'+name;st.paints=[solid(hex)];}
 const paint=hex=>variables[hex]?figma.variables.setBoundVariableForPaint(solid(hex),'color',variables[hex]):solid(hex);
 const available=await figma.listAvailableFontsAsync();
 async function font(family,weight){const key=family+weight;if(fonts[key])return fonts[key];const preferred=weight>=700?'Bold':weight>=600?'SemiBold':weight>=500?'Medium':'Regular';let found=available.find(f=>f.fontName.family===family&&f.fontName.style.toLowerCase()===preferred.toLowerCase());if(!found)found=available.find(f=>f.fontName.family===family&&f.fontName.style==='Regular');if(!found)found=available.find(f=>f.fontName.family==='Inter'&&f.fontName.style==='Regular');if(!found)throw Error('Inter is unavailable in this Figma session.');await figma.loadFontAsync(found.fontName);fonts[key]=found.fontName;return found.fontName;}
 for(const n of payload.scenes.flatMap(s=>s.nodes).filter(n=>n.type==='text'))await font(n.font,n.weight);
 for(const [name,b64]of Object.entries(payload.images))images[name]=figma.createImage(figma.base64Decode(b64)).hash;
 async function primitive(n,parent,dx=0,dy=0){let node;
  if(n.type==='text'){
   node=figma.createText();node.fontName=await font(n.font,n.weight);node.fontSize=n.size;node.characters=n.text;node.textAutoResize='WIDTH_AND_HEIGHT';node.fills=[paint(n.color)];node.lineHeight={unit:'PERCENT',value:120};
   const key=n.font+'/'+n.size+'/'+n.weight;if(!styles[key]){const st=figma.createTextStyle();st.name=stamp+'/'+key;st.fontName=node.fontName;st.fontSize=n.size;st.lineHeight=node.lineHeight;styles[key]=st;}
   await node.setTextStyleIdAsync(styles[key].id);
  }else if(n.type==='vector'){
   node=figma.createNodeFromSvg('<svg width="28" height="28" xmlns="http://www.w3.org/2000/svg"><path fill="'+n.fill+'" fill-rule="evenodd" d="'+n.path+'"/></svg>');node.resize(n.w,n.h);
  }else{
   node=figma.createRectangle();node.resize(n.w,n.h);node.cornerRadius=n.r||0;
   if(n.type==='image'){if(!images[n.file])throw Error('Missing image: '+n.file);node.fills=[{type:'IMAGE',imageHash:images[n.file],scaleMode:'FILL'}];}
   else node.fills=[paint(n.fill)];
   if(n.stroke){node.strokes=[paint(n.stroke)];node.strokeWeight=1;node.strokeAlign='INSIDE';}
  }
  node.name=n.name||n.type;parent.appendChild(node);node.x=n.x-dx;node.y=n.y-dy;return node;
 }
 let componentY=0;
 async function buttonMaster(kind){if(components[kind])return components[kind];const c=figma.createComponent();library.appendChild(c);c.name='Button / '+kind;c.layoutMode='HORIZONTAL';c.primaryAxisAlignItems='CENTER';c.counterAxisAlignItems='CENTER';c.primaryAxisSizingMode='FIXED';c.counterAxisSizingMode='FIXED';c.resize(220,48);c.paddingLeft=18;c.paddingRight=18;c.itemSpacing=8;c.cornerRadius=8;c.fills=[paint(kind==='primary'?token.color.action:token.color.surface)];if(kind!=='primary')c.strokes=[paint(token.color.border)];c.x=0;c.y=componentY;componentY+=88;
  const label=await primitive({type:'text',x:0,y:0,text:'Button label',font:'Inter',size:14,weight:600,color:token.color.text,name:'Label'},c);const prop=c.addComponentProperty('Label','TEXT','Button label');label.componentPropertyReferences={characters:prop};components[kind]=c;return c;}
 await buttonMaster('primary');await buttonMaster('secondary');
 const cardMasters={};
 async function cardMaster(nodes){const base=nodes[0],key=base.name+'/'+base.w;if(cardMasters[key])return cardMasters[key];const c=figma.createComponent();library.appendChild(c);c.name=key;c.resize(base.w,base.h);c.fills=[];c.clipsContent=false;c.x=480+(Object.keys(cardMasters).length%3)*500;c.y=Math.floor(Object.keys(cardMasters).length/3)*500;
  for(const n of nodes)await primitive(n,c,base.x,base.y);cardMasters[key]=c;return c;}
 const placements=new Map();
 const pageHeights=new Map();
 for(const s of payload.scenes){const key=pages[s.page].id;pageHeights.set(key,Math.max(pageHeights.get(key)||0,s.height));}
 for(let index=0;index<payload.scenes.length;index++){
  const s=payload.scenes[index],page=pages[s.page];await figma.setCurrentPageAsync(page);
  const placed=placements.get(page.id)||0;placements.set(page.id,placed+1);
  const f=figma.createFrame();page.appendChild(f);f.name=s.title;f.resize(s.width,s.height);f.fills=[paint(s.background)];f.x=(placed%4)*1580;f.y=Math.floor(placed/4)*(pageHeights.get(page.id)+240);f.clipsContent=true;f.setPluginData('rendermarket-id',s.id);f.setPluginData('status','New AI-assisted portfolio design; fictional data; no transactions');
  if(s.width===1440)f.layoutGrids=[{pattern:'COLUMNS',alignment:'STRETCH',gutterSize:24,count:12,offset:56,color:{r:.4,g:.4,b:1,a:.05},visible:false}];
  frameMap[s.id]=f;
  for(let i=0;i<s.nodes.length;i++){
   const n=s.nodes[i];
   if(n.component&&s.page!=='Wireframes'){
    const master=await buttonMaster(n.component.split('/')[1]),instance=master.createInstance();f.appendChild(instance);instance.x=n.x;instance.y=n.y;instance.resize(n.w,n.h);const property=Object.keys(master.componentPropertyDefinitions).find(k=>k.startsWith('Label#'));instance.setProperties({[property]:s.nodes[i+1].text});i++;continue;
   }
   if(n.name&&n.name.startsWith('Asset card /')&&s.page!=='Wireframes'){
    const c=await cardMaster(s.nodes.slice(i,i+8));const instance=c.createInstance();f.appendChild(instance);instance.x=n.x;instance.y=n.y;i+=7;continue;
   }
   await primitive(n,f);
  }
  if(s.page==='High fidelity'||s.page==='Mobile')for(const h of s.hotspots){const hit=figma.createRectangle();hit.name='Interaction / '+h.label;hit.resize(h.w,h.h);hit.fills=[{...solid('#FFFFFF'),opacity:0.001}];f.appendChild(hit);hit.x=h.x;hit.y=h.y;pending.push({hit,h,source:s});}
  if(index%4===0)figma.ui.postMessage({type:'progress',message:'Built '+(index+1)+' / '+payload.scenes.length+' artboards…'});
 }
 // Additional written states make simulated actions meaningful in Figma.
 const prototype=pages['High fidelity'];await figma.setCurrentPageAsync(prototype);
 const overlays={};
 async function overlay(id,title,body){const f=figma.createFrame();prototype.appendChild(f);f.name='Feedback / '+title;f.resize(540,230);f.x=6500;f.y=Object.keys(overlays).length*300;f.cornerRadius=16;f.fills=[paint(token.color.surface)];await primitive({type:'text',x:28,y:30,text:title,font:'Space Grotesk',size:24,weight:500,color:token.color.text},f);await primitive({type:'text',x:28,y:88,text:body,font:'Inter',size:14,weight:400,color:token.color.muted},f);await primitive({type:'text',x:28,y:160,text:'Close / return to your flow',font:'Inter',size:14,weight:600,color:token.color.accent},f);const close=figma.createRectangle();f.appendChild(close);close.resize(480,48);close.x=20;close.y=143;close.fills=[{...solid('#FFFFFF'),opacity:.001}];await close.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'CLOSE'}]}]);overlays[id]=f;return f;}
 await overlay('save','Saved in this design demo','Fictional collection. No account or remote data.');
 await overlay('draft','Draft saved / simulation','The sample flow can continue without a real account.');
 await overlay('attach','Sample files attached','No upload occurred. Continue to price and licence.');
 await overlay('search','Search / fixed Figma example','Use the browser preview for typed search and filters.');
 await overlay('menu','Prototype navigation','Use Explore, Saved or Creator studio to continue.');
 await overlay('sort','Sort / illustrative control','The browser preview demonstrates price sorting.');
 let links=0;
 for(const {hit,h,source}of pending){
  let target=h.to;let action=h.action;
  if(source.page==='Mobile'&&target&&frameMap['mobile-'+target])target='mobile-'+target;
  if(h.url){await hit.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'URL',url:h.url}]}]);links++;}
  else if(h.to&&frameMap[target]){await hit.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'NODE',destinationId:frameMap[target].id,navigation:'NAVIGATE',transition:null}]}]);links++;}
  else if(action){const kind=action.split(':')[0];const dest=overlays[kind]||overlays.search;await hit.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'NODE',destinationId:dest.id,navigation:'OVERLAY',transition:null}]}]);links++;}
 }
 prototype.flowStartingPoints=[{nodeId:frameMap.home.id,name:'Buyer / discover → review → demo request'},{nodeId:frameMap.register.id,name:'Creator / start → upload → preview → demo publish'},{nodeId:frameMap['mobile-home'].id,name:'Mobile / buyer adaptation'}];
 prototype.selection=[frameMap.home];figma.viewport.scrollAndZoomIntoView([frameMap.home]);await figma.setFileThumbnailNodeAsync(frameMap.cover);
 figma.commitUndo();figma.ui.postMessage({type:'done',message:'Created '+payload.scenes.length+' editable artboards, '+links+' prototype links, colour variables, text styles and reusable components.\n\nReview fonts, text bounds and links in Figma before sharing. Choose the Buyer or Creator starting flow in Present mode. Public sharing is not changed by this plugin.'});
 figma.notify('RenderMarket imported. Review the file and prototype before publication.');
}
