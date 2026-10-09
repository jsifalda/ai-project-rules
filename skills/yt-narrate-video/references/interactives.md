# Interactive figure patterns

Tested patterns from a finished page. Each has an HTML block (paste inside a chapter `<section>`) and a JS block (paste at `{{FIGURE_JS}}` in the template). The JS relies on helpers the template already defines: `$`, `$$`, `css(var)`, `el(tag, attrs, parent, text)`, `fmt(seconds)`, `esc(text)` (HTML-escapes text for `innerHTML`).

Rules for every figure:
- Read colors with `css('--go')` etc. at draw time so dark mode works.
- Draw SVGs in a 760-wide viewBox inside `.scroll-x`. The template scales text on mobile.
- If the figure has a draw function, end its block with `FIGS.push(drawX)` and do not call it directly. `redrawAll()` runs it on load, theme change and resize.
- Put a `.note` under any chart with invented numbers that says so.
- Keep `aria-live="polite"` on the readout so screen readers hear the result.

The sample copy comes from one Ideas-genre video. The mechanics work for any genre. Rewrite all copy, labels and numbers.

## Contents
1. Repeat loop vs learning loop (race chart) (L26)
2. Asymmetric ledger (L74)
3. Sentence rewriter (L111)
4. Multi-bar dial (L146)
5. Clickable traffic light (L175)
6. Area chart toggle (quantity x quality) (L206)
7. Resource allocator (campfires) (L248)
8. Two-loop diagram (L291)
9. Monte Carlo strategy simulator (L331)
10. Hindsight vs foresight dots (L379)

## Repeat loop vs learning loop (race chart)

**Use for:** Persistence vs reflection, iteration vs postmortem, any "slow now, fast later" trade. Shows a break-even point.

```html
<div class="fig" id="raceFig">
    <div class="fig-in">
      <h3>Who wins the race: the runner who never stops, or the one who stops once?</h3>
      <p class="sub">Each lap has the same pothole. The persistent runner falls in every lap and loses 3 seconds getting up. The reflective runner falls once, then stops for 6 seconds to study the hole, and never falls in it again.</p>
      <div class="ctl"><label for="laps">Laps <input type="range" id="laps" min="1" max="12" value="1"><output id="lapsOut">1</output></label><button class="btn ghost" id="lapsPlay" type="button">Play laps</button></div>
      <div class="scroll-x"><svg id="raceSvg" viewBox="0 0 760 270" width="100%" role="img" aria-label="Line chart of total time lost per lap for two runners"></svg></div>
      <p class="read" id="raceRead" aria-live="polite"></p>
      <p class="note">An illustrative model with made-up numbers. The point is the shape: the reflective runner is behind early and ahead for good after the break-even lap.</p>
    </div>
  </div>
```

```js
function drawRace(){
  const svg=$('#raceSvg');svg.innerHTML='';
  const L=+$('#laps').value;$('#lapsOut').textContent=L;
  const N=12, x0=60,x1=730,y0=230,y1=30, maxT=36;
  const X=l=>x0+(x1-x0)*l/N, Y=t=>y0-(y0-y1)*t/maxT;
  const ink=css('--ink'),ink2=css('--ink-2'),rule=css('--rule');
  for(let t=0;t<=maxT;t+=6){el('line',{x1:x0,x2:x1,y1:Y(t),y2:Y(t),stroke:rule,'stroke-width':1},svg);el('text',{x:x0-10,y:Y(t)+4,'text-anchor':'end','font-size':12,fill:ink2},svg,t+'s')}
  for(let l=0;l<=N;l+=2)el('text',{x:X(l),y:y0+20,'text-anchor':'middle','font-size':12,fill:ink2},svg,l===0?'0':'lap '+l);
  el('text',{x:x0,y:16,'font-size':12,fill:ink2},svg,'Total seconds lost');
  const per=l=>3*l, ref=l=>l===0?0:9;
  const path=(f,n)=>{let d='';for(let l=0;l<=n;l++)d+=(l?'L':'M')+X(l)+','+Y(f(l));return d};
  // future (faint)
  el('path',{d:path(per,N),fill:'none',stroke:css('--stop'),'stroke-width':2,'stroke-dasharray':'3 5',opacity:.35},svg);
  el('path',{d:path(ref,N),fill:'none',stroke:css('--go'),'stroke-width':2,'stroke-dasharray':'3 5',opacity:.35},svg);
  el('path',{d:path(per,L),fill:'none',stroke:css('--stop'),'stroke-width':3.5,'stroke-linejoin':'round'},svg);
  el('path',{d:path(ref,L),fill:'none',stroke:css('--go'),'stroke-width':3.5,'stroke-linejoin':'round'},svg);
  el('circle',{cx:X(L),cy:Y(per(L)),r:6,fill:css('--stop')},svg);el('circle',{cx:X(L),cy:Y(ref(L)),r:6,fill:css('--go')},svg);
  el('text',{x:X(N)-4,y:Y(per(N))-10,'text-anchor':'end','font-size':13,'font-weight':600,fill:css('--stop')},svg,'Persistent: falls every lap');
  el('text',{x:X(N)-4,y:Y(ref(N))-10,'text-anchor':'end','font-size':13,'font-weight':600,fill:css('--go')},svg,'Reflective: stops once');
  el('line',{x1:X(3),x2:X(3),y1:y0,y2:Y(9)-14,stroke:ink,'stroke-width':1,'stroke-dasharray':'2 3'},svg);
  el('text',{x:X(3)+6,y:Y(9)-18,'font-size':12,fill:ink},svg,'Break-even at lap 3');
  const p=per(L),r=ref(L);
  $('#raceRead').innerHTML=L<3?`After ${L} lap${L>1?'s':''}, the reflective runner is <b>behind by ${r-p} seconds</b>. Stopping looks like losing.`:L===3?`After 3 laps, they are <b>even at 9 seconds lost</b> each.`:`After ${L} laps, the reflective runner is <b>ahead by ${p-r} seconds</b>, and the gap grows by 3 every lap from here.`;
}
$('#laps').addEventListener('input',drawRace);
let playT=null;
$('#lapsPlay').addEventListener('click',()=>{clearInterval(playT);const r=$('#laps');r.value=1;drawRace();if(matchMedia('(prefers-reduced-motion: reduce)').matches){r.value=12;drawRace();return}playT=setInterval(()=>{if(+r.value>=12){clearInterval(playT);return}r.value=+r.value+1;drawRace();scaleText()},420)});
FIGS.push(drawRace);
```

## Asymmetric ledger

**Use for:** Trust, reputation, habits. Gains are small, losses are big. Click-driven, no draw function.

```html
<div class="fig" id="ledgerFig">
    <div class="fig-in">
      <h3>The self-trust ledger</h3>
      <p class="sub">Make and keep a few promises, then break one. Watch how far one broken promise moves the needle.</p>
      <div class="ctl"><button class="btn" id="keepBtn" type="button">Keep a promise</button><button class="btn ghost" id="breakBtn" type="button">Break a promise</button><button class="btn ghost" id="resetBtn" type="button">Start over</button></div>
      <div class="meter" aria-hidden="true"><i id="meterFill" style="width:50%"></i></div>
      <div class="beads" id="beads" aria-hidden="true"></div>
      <p class="read" id="ledgerRead" aria-live="polite">Self-trust: 50 of 100. No history yet.</p>
      <p class="note">Assumption, not data: a broken promise costs four times what a kept one earns. Research on trust repair broadly supports the asymmetry, but the exact ratio here is a choice for illustration.</p>
    </div>
  </div>
```

```js
let trust=50, hist=[];
function ledger(){
  $('#meterFill').style.width=trust+'%';
  $('#meterFill').style.background=trust>=60?'var(--go)':trust>=35?'var(--yield)':'var(--stop)';
  $('#beads').innerHTML=hist.slice(-24).map(k=>`<span style="background:var(${k?'--go':'--stop'})"></span>`).join('');
  const kept=hist.filter(Boolean).length, broke=hist.length-kept;
  let msg=`Self-trust: <b>${trust} of 100</b>. `;
  if(!hist.length)msg+='No history yet.';
  else if(broke===0)msg+=`${kept} kept, none broken. Slow, steady gains.`;
  else msg+=`${kept} kept, ${broke} broken. It takes ${Math.ceil(8/2)} kept promises to repair one broken one.`;
  $('#ledgerRead').innerHTML=msg;
}
$('#keepBtn').addEventListener('click',()=>{trust=Math.min(100,trust+2);hist.push(1);ledger()});
$('#breakBtn').addEventListener('click',()=>{trust=Math.max(0,trust-8);hist.push(0);ledger()});
$('#resetBtn').addEventListener('click',()=>{trust=50;hist=[];ledger()});
ledger();
```

## Sentence rewriter

**Use for:** Any reframing lesson ("can't" to "having trouble"). Edit the regex and output template.

```html
<div class="fig" id="reframeFig">
    <div class="fig-in reframe">
      <h3>Rewrite a "can't"</h3>
      <p class="sub">Type something you think you can't do. The sentence changes as you type.</p>
      <label for="cantIn" class="sub" style="display:block;margin-bottom:6px">Your sentence</label>
      <input id="cantIn" type="text" value="I can't get this release out on time" autocomplete="off">
      <p class="out" id="cantOut" aria-live="polite"></p>
      <p class="note" id="cantNext"></p>
    </div>
  </div>
```

```js
function reframe(){
  const raw=$('#cantIn').value.trim();
  const m=raw.match(/^(?:i|we)\s*(?:can't|cant|cannot|can not|won't be able to|am unable to|are unable to)\s+(.*)$/i);
  const who=/^we/i.test(raw)?'We\u2019re':'I\u2019m';
  let task;
  if(m&&m[1]){task=m[1].replace(/[.!]+$/,'');
    const words=task.split(' ');const v=words[0].toLowerCase();
    const ing=v.endsWith('e')&&!v.endsWith('ee')?v.slice(0,-1)+'ing':v+'ing';
    task=[ing].concat(words.slice(1)).join(' ');
    $('#cantOut').textContent=`${who} having trouble ${task}.`;
    $('#cantNext').textContent='Next: list what you already checked, and name the one thing you haven\u2019t tried yet.';
  }else if(!raw){$('#cantOut').textContent='';$('#cantNext').textContent='Start with "I can\u2019t\u2026"'}
  else{$('#cantOut').textContent='Start the sentence with "I can\u2019t" or "We can\u2019t".';$('#cantNext').textContent=''}
}
$('#cantIn').addEventListener('input',reframe);reframe();
```

## Multi-bar dial

**Use for:** One input that moves several outcomes at once (commitment, effort, price). State the curves are illustrative.

```html
<div class="fig" id="dialFig">
    <div class="fig-in">
      <h3>The price of plausible deniability</h3>
      <p class="sub">Drag the slider from one foot in the door to all in. Four things move together.</p>
      <div class="ctl"><label for="commit">Commitment <input type="range" id="commit" min="0" max="100" value="40"><output id="commitOut">40%</output></label></div>
      <div class="bars" id="dialBars"></div>
      <p class="read" id="dialRead" aria-live="polite"></p>
      <p class="note">Illustrative curves, not measured data. They encode the interview's claims: holding back lowers both the pain of failing and the chance of succeeding, and blurs what you learn.</p>
    </div>
  </div>
```

```js
const dialRows=[['Chance of success','--go'],['Pain if it fails','--stop'],['How clear the answer is','--sky'],['How much you earned it','--yield']];
$('#dialBars').innerHTML=dialRows.map((r,i)=>`<span>${r[0]}</span><div class="track"><div class="fill" id="df${i}" style="background:var(${r[1]})"></div></div><span class="v" id="dv${i}"></span>`).join('');
function dial(){
  const c=+$('#commit').value/100;$('#commitOut').textContent=Math.round(c*100)+'%';
  const vals=[0.08+0.72*Math.pow(c,1.6),0.15+0.8*c,Math.pow(c,2.2),c];
  vals.forEach((v,i)=>{$('#df'+i).style.width=(v*100)+'%';$('#dv'+i).textContent=Math.round(v*100)});
  $('#dialRead').innerHTML=c<0.35?'<b>One foot out.</b> Failure would barely hurt, and you would learn almost nothing from it either way.':c<0.75?'<b>Hedged.</b> You still have an excuse ready. If it works, part of you will know you held back.':c<0.96?'<b>Nearly all in.</b> The answer is getting readable, and so is the risk.':'<b>All in.</b> It may hurt more. But whatever happens, you find out, and you own the result.';
}
$('#commit').addEventListener('input',dial);dial();
```

## Clickable traffic light

**Use for:** Marker-state concept explainer. Swap the TL object text.

```html
<div class="fig" id="tlFig">
    <div class="fig-in">
      <h3>Read each light the way he does</h3>
      <p class="sub">Press a lamp.</p>
      <div class="tl">
        <div class="tl-box" role="group" aria-label="Traffic light">
          <button class="r" type="button" data-k="r" aria-pressed="false" aria-label="Red light"></button>
          <button class="y" type="button" data-k="y" aria-pressed="false" aria-label="Yellow light"></button>
          <button class="g" type="button" data-k="g" aria-pressed="true" aria-label="Green light"></button>
        </div>
        <div class="tl-txt" id="tlTxt" aria-live="polite"></div>
      </div>
    </div>
  </div>
```

```js
const TL={
 g:['Green: go','The green light is the obvious one. Commit, move, finish. He wants the go-moments taken all the way, not with one foot out.','At work: a decision is made. Stop relitigating it in every standup.'],
 y:['Yellow: pause','A yellow is a moment for introspection. Not stopping for good, but slowing down to look at why you keep landing in the same spot.','At work: the retro, the one-on-one, the quiet week after a launch. Don\u2019t skip them when things are busy.'],
 r:['Red: the hard stop','Reds are the hardships and crises. In his telling they are not the opposite of a good life. They are how a person evolves, and why growing older is worth anything.','At work: a failed launch you study is worth more than a modest success you don\u2019t.']
};
function tl(k){$$('.tl-box button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.k===k));const t=TL[k];$('#tlTxt').innerHTML=`<h4>${t[0]}</h4><p>${t[1]}</p><p style="color:var(--ink-2)">${t[2]}</p>`}
$$('.tl-box button').forEach(b=>b.addEventListener('click',()=>tl(b.dataset.k)));tl('g');
```

## Area chart toggle (quantity x quality)

**Use for:** Two strategies where the area under the curve is the score.

```html
<div class="fig" id="lifeFig">
    <div class="fig-in">
      <h3>Life as profit: years times quality</h3>
      <p class="sub">Two made-up lives. The shaded area is his "profit." Switch between them.</p>
      <div class="ctl"><button class="btn ghost" type="button" data-life="long" aria-pressed="true">Chase more years</button><button class="btn ghost" type="button" data-life="good" aria-pressed="false">Chase better years</button></div>
      <div class="scroll-x"><svg id="lifeSvg" viewBox="0 0 760 300" width="100%" role="img" aria-label="Area chart of quality of life by age"></svg></div>
      <p class="read" id="lifeRead" aria-live="polite"></p>
      <p class="note">Invented curves to show the idea, not health data. Quality is on a 0 to 10 scale.</p>
    </div>
  </div>
```

```js
let lifeMode='long';
function qLong(a){if(a<20)return 6+a*0.025;if(a<55)return 6.5-0.01*(a-20);if(a<70)return 6.15-0.12*(a-55);return Math.max(0.8,4.35-0.17*(a-70))}
function qGood(a){if(a<20)return 6+a*0.05;if(a<60)return 7+0.04*(a-20);if(a<78)return 8.6-0.05*(a-60);return Math.max(0,7.7-0.9*(a-78))}
function drawLife(){
  const svg=$('#lifeSvg');svg.innerHTML='';
  const end=lifeMode==='long'?96:86, f=lifeMode==='long'?qLong:qGood;
  const x0=50,x1=740,y0=255,y1=25,X=a=>x0+(x1-x0)*a/100,Y=q=>y0-(y0-y1)*q/10;
  const ink2=css('--ink-2'),rule=css('--rule');
  for(let q=0;q<=10;q+=2){el('line',{x1:x0,x2:x1,y1:Y(q),y2:Y(q),stroke:rule},svg);el('text',{x:x0-8,y:Y(q)+4,'text-anchor':'end','font-size':12,fill:ink2},svg,q)}
  for(let a=0;a<=100;a+=20)el('text',{x:X(a),y:y0+20,'text-anchor':'middle','font-size':12,fill:ink2},svg,a===0?'age 0':a);
  el('text',{x:x0,y:14,'font-size':12,fill:ink2},svg,'Quality of life');
  let d='M'+X(0)+','+Y(0),area=0;for(let a=0;a<=end;a+=0.5){const q=f(a);d+='L'+X(a)+','+Y(q);area+=q*0.5}d+='L'+X(end)+','+Y(0)+'Z';
  const col=lifeMode==='long'?css('--sky'):css('--go');
  el('path',{d,fill:col,opacity:.28},svg);
  let l='';for(let a=0;a<=end;a+=0.5)l+=(a?'L':'M')+X(a)+','+Y(f(a));el('path',{d:l,fill:'none',stroke:col,'stroke-width':3},svg);
  el('line',{x1:X(end),x2:X(end),y1:Y(0),y2:Y(9.6),stroke:css('--ink'),'stroke-dasharray':'2 3'},svg);
  el('text',{x:X(end)-6,y:Y(9.2),'text-anchor':'end','font-size':13,'font-weight':600,fill:css('--ink')},svg,'lives to '+end);
  const other=lifeMode==='long'?qGood:qLong,oe=lifeMode==='long'?86:96;let oa=0;for(let a=0;a<=oe;a+=0.5)oa+=other(a)*0.5;
  $('#lifeRead').innerHTML=`This life runs <b>${end} years</b> and scores <b>${Math.round(area)}</b> quality-years. The other one runs ${oe} years and scores ${Math.round(oa)}. ${area>oa?'Fewer years, more life.':'More years, less life.'}`;
}
$$('[data-life]').forEach(b=>b.addEventListener('click',()=>{lifeMode=b.dataset.life;$$('[data-life]').forEach(x=>x.setAttribute('aria-pressed',x===b));drawLife()}));
FIGS.push(drawLife);
```

## Resource allocator (campfires)

**Use for:** Focus, WIP limits, spreading too thin. Fixed upkeep per item, convex payoff above it.

```html
<div class="fig" id="fireFig">
    <div class="fig-in">
      <h3>Spread 12 logs</h3>
      <p class="sub">You have 12 logs. Each fire burns 2 just to stay lit, and every log above that adds real heat. Choose how many fires to keep.</p>
      <div class="ctl"><label for="fires">Fires <input type="range" id="fires" min="1" max="6" value="4"><output id="firesOut">4</output></label></div>
      <div class="scroll-x"><svg id="fireSvg" viewBox="0 0 760 220" width="100%" role="img" aria-label="Campfires sized by the logs each one gets"></svg></div>
      <p class="read" id="fireRead" aria-live="polite"></p>
      <p class="note">A toy model. The 2-log upkeep stands for the fixed cost of any project: context switching, meetings, maintenance. The heat curve is assumed, not measured.</p>
    </div>
  </div>
```

```js
function drawFires(){
  const svg=$('#fireSvg');svg.innerHTML='';
  const n=+$('#fires').value;$('#firesOut').textContent=n;
  const logs=12,base=Math.floor(logs/n),extra=logs%n;
  const alloc=Array.from({length:n},(_,i)=>base+(i<extra?1:0));
  const heat=l=>l<=2?0:Math.pow(l-2,1.25);
  let total=0;const w=760/n;
  el('line',{x1:0,x2:760,y1:190,y2:190,stroke:css('--rule')},svg);
  alloc.forEach((l,i)=>{
    const cx=w*i+w/2,h=heat(l);total+=h;const s=Math.pow(Math.min(1,h/heat(12)),0.6);
    for(let k=0;k<l;k++){const a=(k/l)*Math.PI;el('line',{x1:cx-Math.cos(a)*30,y1:190-Math.sin(a)*5,x2:cx+Math.cos(a)*30,y2:190+Math.sin(a)*5,stroke:'#6b4426','stroke-width':6,'stroke-linecap':'round'},svg)}
    if(h>0){const fh=30+130*s,fw=14+34*s;
      el('ellipse',{cx,cy:180-fh*0.35,rx:fw*2.2,ry:fh*0.8,fill:'#F2A531',opacity:.15},svg);
      el('path',{d:`M${cx-fw},185 Q${cx-fw*1.1},${185-fh*0.5} ${cx},${185-fh} Q${cx+fw*1.1},${185-fh*0.5} ${cx+fw},185Z`,fill:'#E2552A'},svg);
      el('path',{d:`M${cx-fw*0.55},186 Q${cx-fw*0.6},${186-fh*0.35} ${cx},${186-fh*0.65} Q${cx+fw*0.6},${186-fh*0.35} ${cx+fw*0.55},186Z`,fill:'#F7C948'},svg);
    }else{el('path',{d:`M${cx-6},184 q-4,-16 6,-26 q8,12 0,26z`,fill:css('--ink-2'),opacity:.45},svg)}
    el('text',{x:cx,y:212,'text-anchor':'middle','font-size':12,fill:css('--ink-2')},svg,l+' logs');
  });
  const best=heat(12);
  $('#fireRead').innerHTML=`<b>${n} fire${n>1?'s':''}</b>, ${Math.round(total)} units of heat. ${n===1?'Everything goes into one fire. Maximum heat.':n<=2?`About ${Math.round(100*total/best)}% of what one big fire gives.`:alloc.some(l=>l<=2)?`Some fires get only upkeep and give no heat at all. You keep ${Math.round(100*total/best)}% of the heat of one fire.`:`You keep ${Math.round(100*total/best)}% of the heat of one fire. The upkeep eats the rest.`}`;
}
$('#fires').addEventListener('input',drawFires);
FIGS.push(drawFires);
```

## Two-loop diagram

**Use for:** Before/after process comparisons with a loop that does or does not exit.

```html
<div class="fig" id="loopFig">
    <div class="fig-in">
      <h3>Two loops after a mistake</h3>
      <p class="sub">Switch between the fast loop and the one he argues for.</p>
      <div class="ctl"><button class="btn ghost" type="button" data-loop="fast" aria-pressed="true">Fast forgiveness</button><button class="btn ghost" type="button" data-loop="slow" aria-pressed="false">Pause, then change</button></div>
      <div class="scroll-x"><svg id="loopSvg" viewBox="0 0 760 250" width="100%" role="img" aria-label="Diagram of what happens after a mistake"></svg></div>
      <p class="read" id="loopRead" aria-live="polite"></p>
    </div>
  </div>
```

```js
let loopMode='fast';
function drawLoop(){
  const svg=$('#loopSvg');svg.innerHTML='';
  const ink=css('--ink'),ink2=css('--ink-2'),card=css('--paper-2');
  const defs=el('defs',{},svg);const mk=el('marker',{id:'ar',viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:7,markerHeight:7,orient:'auto-start-reverse'},defs);el('path',{d:'M0,0L10,5L0,10z',fill:ink2},mk);
  const box=(x,y,t,c)=>{el('rect',{x:x-74,y:y-24,width:148,height:48,rx:24,fill:c||card,stroke:css('--rule')},svg);el('text',{x,y:y+5,'text-anchor':'middle','font-size':14,'font-weight':600,fill:c?'#fff':ink},svg,t)};
  const arrow=(d)=>el('path',{d,fill:'none',stroke:ink2,'stroke-width':2,'marker-end':'url(#ar)'},svg);
  if(loopMode==='fast'){
    box(110,125,'Mistake',css('--stop'));box(310,60,'Sorry');box(510,60,'Forgiven');box(650,180,'Back to it');
    arrow('M150,104 Q200,60 236,60');arrow('M380,60 L436,60');arrow('M560,80 Q630,110 645,152');arrow('M580,190 Q330,240 160,150');
    el('text',{x:380,y:232,'text-anchor':'middle','font-size':13,fill:ink2},svg,'nothing changed, so the loop repeats');
    $('#loopRead').innerHTML='Apology traded for forgiveness, then <b>straight back to the same behavior</b>. He calls this becoming a repeat offender.';
  }else{
    box(90,125,'Mistake',css('--stop'));box(250,60,'Sorry');box(410,60,'Pause, feel it');box(570,60,'Change it');box(670,180,'Forgiven',css('--go'));
    arrow('M126,103 Q170,60 176,60');arrow('M320,60 L336,60');arrow('M480,60 L496,60');arrow('M620,82 Q660,120 668,152');
    el('text',{x:400,y:200,'text-anchor':'middle','font-size':13,fill:ink2},svg,'the loop exits, no second sorry needed');
    $('#loopRead').innerHTML='The pause comes first, then the change. <b>Forgiveness comes last</b>, once the behavior has moved. That includes forgiving yourself.';
  }
}
$$('[data-loop]').forEach(b=>b.addEventListener('click',()=>{loopMode=b.dataset.loop;$$('[data-loop]').forEach(x=>x.setAttribute('aria-pressed',x===b));drawLoop()}));
FIGS.push(drawLoop);
```

## Monte Carlo strategy simulator

**Use for:** Few safe bets vs many bold bets, hit rate vs total wins. Histogram of 2,000 runs.

```html
<div class="fig" id="riskFig">
    <div class="fig-in">
      <h3>Simulate 2,000 lives</h3>
      <p class="sub">The careful life takes 8 risks with a 7 in 8 hit rate. The bold life takes more risks with a lower hit rate. Change the bold life and see who comes out ahead.</p>
      <div class="ctl"><label for="riskN">Bold risks <input type="range" id="riskN" min="10" max="200" step="5" value="100"><output id="riskNOut">100</output></label></div>
      <div class="ctl"><label for="riskP">Bold hit rate <input type="range" id="riskP" min="1" max="25" value="8"><output id="riskPOut">8%</output></label><button class="btn ghost" id="riskRun" type="button">Run again</button></div>
      <div class="scroll-x"><svg id="riskSvg" viewBox="0 0 760 300" width="100%" role="img" aria-label="Histogram of wins per life for two strategies"></svg></div>
      <p class="read" id="riskRead" aria-live="polite"></p>
      <p class="note">Each risk is an independent coin flip with the hit rate shown. His numbers (7 of 8 versus 8 of 100) are the default. Real risks are not independent and not equal in size, so treat this as a sketch of the logic.</p>
    </div>
  </div>
```

```js
function binom(n,p){let k=0;for(let i=0;i<n;i++)if(Math.random()<p)k++;return k}
function drawRisk(){
  const n=+$('#riskN').value,p=+$('#riskP').value/100;$('#riskNOut').textContent=n;$('#riskPOut').textContent=Math.round(p*100)+'%';
  const T=2000,A=[],B=[];let bWins=0,ties=0;
  for(let i=0;i<T;i++){const a=binom(8,0.875),b=binom(n,p);A.push(a);B.push(b);if(b>a)bWins++;else if(b===a)ties++}
  const maxV=Math.max(14,...B,...A);const svg=$('#riskSvg');svg.innerHTML='';
  const x0=50,x1=740,y0=250,y1=30,bw=(x1-x0)/(maxV+1);
  const cnt=arr=>{const c=new Array(maxV+1).fill(0);arr.forEach(v=>c[v]++);return c};
  const cA=cnt(A),cB=cnt(B),top=Math.max(...cA,...cB);
  const X=v=>x0+bw*v,Y=c=>y0-(y0-y1)*c/top;
  const ink2=css('--ink-2'),rule=css('--rule');
  el('line',{x1:x0,x2:x1,y1:y0,y2:y0,stroke:rule},svg);
  const step=maxV>40?10:maxV>20?5:2;
  for(let v=0;v<=maxV;v+=step)el('text',{x:X(v)+bw/2,y:y0+18,'text-anchor':'middle','font-size':12,fill:ink2},svg,v);
  el('text',{x:x1,y:y0+36,'text-anchor':'end','font-size':12,fill:ink2},svg,'wins per life');
  for(let v=0;v<=maxV;v++){
    if(cA[v])el('rect',{x:X(v)+1,y:Y(cA[v]),width:Math.max(1,bw-2),height:y0-Y(cA[v]),fill:css('--sky'),opacity:.75},svg);
    if(cB[v])el('rect',{x:X(v)+1,y:Y(cB[v]),width:Math.max(1,bw-2),height:y0-Y(cB[v]),fill:css('--go'),opacity:.6},svg);
  }
  const mA=A.reduce((s,v)=>s+v,0)/T,mB=B.reduce((s,v)=>s+v,0)/T;
  el('rect',{x:x0+4,y:y1-14,width:12,height:12,fill:css('--sky'),opacity:.75},svg);el('text',{x:x0+22,y:y1-4,'font-size':13,fill:css('--ink')},svg,'Careful: 8 risks at 87.5%');
  el('rect',{x:x0+300,y:y1-14,width:12,height:12,fill:css('--go'),opacity:.6},svg);el('text',{x:x0+318,y:y1-4,'font-size':13,fill:css('--ink')},svg,`Bold: ${n} risks at ${Math.round(p*100)}%`);
  const misses=Math.round(n*(1-p));
  $('#riskRead').innerHTML=`Average wins: careful <b>${mA.toFixed(1)}</b>, bold <b>${mB.toFixed(1)}</b>. The bold life beats the careful one in <b>${Math.round(100*bWins/T)}%</b> of lives and ties in ${Math.round(100*ties/T)}%. It also misses about ${misses} times, each one a lesson. Break-even needs a bold hit rate of ${(700/n).toFixed(1)}%.`;
}
['riskN','riskP'].forEach(id=>$('#'+id).addEventListener('input',drawRisk));$('#riskRun').addEventListener('click',drawRisk);
FIGS.push(drawRisk);
```

## Hindsight vs foresight dots

**Use for:** "Connect the dots looking back" ideas. Toggle forward fog vs backward path.

```html
<div class="fig" id="dotsFig">
    <div class="fig-in">
      <h3>Look forward, then look back</h3>
      <p class="sub">The same set of moments, seen from two places in time.</p>
      <div class="ctl"><button class="btn ghost" type="button" data-view="fwd" aria-pressed="true">Look forward</button><button class="btn ghost" type="button" data-view="back" aria-pressed="false">Look back</button></div>
      <div class="scroll-x"><svg id="dotsSvg" viewBox="0 0 760 280" width="100%" role="img" aria-label="Dots that are scattered when looking forward and connected when looking back"></svg></div>
      <p class="read" id="dotsRead" aria-live="polite"></p>
    </div>
  </div>
```

```js
let dotView='fwd';
const P=[[60,220],[140,150],[205,205],[280,120],[345,190],[420,95],[490,170],[560,80],[620,150],[700,60]];
function drawDots(){
  const svg=$('#dotsSvg');svg.innerHTML='';const ink2=css('--ink-2');
  if(dotView==='fwd'){
    // fog of possibilities from the first dot
    const seed=[[0.3,.8],[.6,.3],[.9,.6],[.2,.2],[.75,.9],[.5,.55],[.1,.5],[.85,.15]];
    seed.forEach(([a,b])=>{el('path',{d:`M60,220 Q${200+a*300},${40+b*200} ${360+a*380},${30+b*230}`,fill:'none',stroke:ink2,'stroke-width':1.4,'stroke-dasharray':'2 6',opacity:.5},svg)});
    P.forEach(([x,y],i)=>el('circle',{cx:x,cy:y,r:i===0?9:7,fill:i===0?css('--ink'):css('--ink-2'),opacity:i===0?1:.25},svg));
    el('text',{x:60,y:250,'text-anchor':'middle','font-size':13,'font-weight':600,fill:css('--ink')},svg,'you, now');
    el('text',{x:560,y:260,'text-anchor':'middle','font-size':13,fill:ink2},svg,'plans for this afternoon, no idea what happens');
    $('#dotsRead').innerHTML='From here, the future is a fan of faint possibilities. <b>A mystery going forward.</b>';
  }else{
    let d='';P.forEach(([x,y],i)=>d+=(i?'L':'M')+x+','+y);
    el('path',{d,fill:'none',stroke:css('--ink'),'stroke-width':2.5,'stroke-linejoin':'round'},svg);
    P.forEach(([x,y],i)=>el('circle',{cx:x,cy:y,r:i===4?10:7,fill:i===4?css('--stop'):i===P.length-1?css('--go'):css('--sky')},svg));
    el('text',{x:345,y:222,'text-anchor':'middle','font-size':13,'font-weight':600,fill:css('--stop')},svg,'the red light');
    el('text',{x:345,y:238,'text-anchor':'middle','font-size':12,fill:ink2},svg,'60 seconds late');
    el('text',{x:620,y:200,'text-anchor':'middle','font-size':12,fill:ink2},svg,'"I thought that was the end"');
    el('text',{x:700,y:40,'text-anchor':'middle','font-size':13,'font-weight':600,fill:css('--go')},svg,'this table');
    $('#dotsRead').innerHTML='From the end, every dot connects, even the red light that made you late. <b>A science looking back.</b>';
  }
}
$$('[data-view]').forEach(b=>b.addEventListener('click',()=>{dotView=b.dataset.view;$$('[data-view]').forEach(x=>x.setAttribute('aria-pressed',x===b));drawDots()}));
FIGS.push(drawDots);
```
