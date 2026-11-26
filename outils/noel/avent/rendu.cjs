const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1100,height:2000}});
await p.goto('file://'+process.cwd()+'/avent.html');await p.waitForTimeout(500);
const fs=require('fs');fs.mkdirSync('png',{recursive:true});
for(let i=1;i<=24;i++){await p.locator('#c'+i).screenshot({path:`png/avent-${String(i).padStart(2,'0')}.png`});}
await p.locator('.cover').screenshot({path:'png/avent-couverture-bulle.png'});await b.close();})();
