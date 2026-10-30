/* Pure catalogue logic check; no browser, DOM, network or UI automation. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),bundle={window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'prototype/catalogue.js'),'utf8'),bundle);
const data=bundle.window.RM_ASSETS;
assert.equal(data.length,27);assert.equal(new Set(data.map(a=>a.id)).size,27);
const state={fields:{},category:'All assets',region:'All places',price:0,sort:'featured'};
const context={state,RM_ASSETS:data};vm.createContext(context);
const source=fs.readFileSync(path.join(root,'prototype/app.js'),'utf8');
vm.runInContext(source.match(/^function matches\(\).*$/m)[0],context);
for(const [query,ids]of [['mama put',['canteen']],['barbershop',['barbershop']],['church',['church']],['football field',['football']],['akara woman',['akara-vendor']],['akara',['akara','akara-vendor']]]){
 state.fields.search=query;const result=context.matches().map(a=>a.id).sort().join(',');assert.equal(result,ids.sort().join(','),query);
}
state.fields.search='lagos everyday';assert.equal(context.matches().length,10);
state.fields.search='characters';assert.equal(context.matches().length,5);
state.fields.search='';state.sort='price-asc';const sorted=context.matches();assert.equal(sorted.at(-1).id,'sanctuary');assert(sorted.slice(0,-1).every((a,i,list)=>i===0||list[i-1].price<=a.price));
state.price=1;assert(context.matches().every(a=>a.price!==null&&a.price<10000));
console.log('PASS: 27 unique entries; six named searches; Lagos/character discovery; price sorting/filtering.');
