# Generic install (any site with an HTML head)

## Contents

- Placement (line 12)
- Consent defaults (line 19)
- Tag loaders (line 40)
- Clarity consentv2 call (line 59)
- Consent banner (line 75)
- Rules (line 167)

## Placement

- Put the consent defaults and the tag loaders in the root HTML `<head>`, in that order: static `index.html`, Vite `index.html`, Astro base layout.
- Put the consent banner at the end of `<body>`.
- Replace `G-XXXXXXXXXX` and `CLARITY_PROJECT_ID` before commit.
- Set `DEFAULT` from the gate's consent model in both scripts. Opt-out → `'granted'`. Opt-in → `'denied'`.

## Consent defaults

- Run this before the gtag loader. A stored choice wins over `DEFAULT`.

```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  (function () {
    var DEFAULT = 'granted';
    var stored = null;
    try { stored = localStorage.getItem('analytics-consent'); } catch (e) {}
    if (!stored) { var m = document.cookie.match(/(?:^|; )analytics-consent=(granted|denied)/); stored = m && m[1]; }
    gtag('consent', 'default', {
      ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
      analytics_storage: stored === 'granted' || stored === 'denied' ? stored : DEFAULT
    });
  })();
</script>
```

## Tag loaders

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
<script>
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "CLARITY_PROJECT_ID");
</script>
```

- Keep the Clarity loader stub.

## Clarity consentv2 call

- Source: https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-consent-api-v2
- Keep the key casing exactly. `v` is `'granted'` or `'denied'`.

```js
window.clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: v });
```

- Send it on every page load.
- Define the queue stub before a `consentv2` call that can run before the Clarity loader.

```js
window.clarity = window.clarity || function () { (window.clarity.q = window.clarity.q || []).push(arguments); };
```

## Consent banner

- Give Accept and Reject the same visual weight.

```html
<div id="consent" class="consent" role="region" aria-label="Cookie consent" hidden>
  <p>We use cookies to measure traffic and improve this site.</p>
  <div class="consent-actions">
    <button type="button" data-consent="denied">Reject</button>
    <button type="button" data-consent="granted">Accept</button>
  </div>
</div>
<style>
  .consent{position:fixed;left:0;right:0;bottom:0;z-index:1000;display:flex;flex-wrap:wrap;
    gap:.75rem;align-items:center;justify-content:space-between;
    padding:1rem 1rem calc(1rem + env(safe-area-inset-bottom));
    background:var(--consent-bg,#fff);color:var(--consent-fg,#1a1a1a);
    border-top:1px solid var(--consent-border,#d0d0d0);font:inherit}
  .consent[hidden]{display:none}
  .consent p{margin:0;flex:1 1 16rem}
  .consent-actions{display:flex;gap:.5rem}
  .consent button{font:inherit;min-height:44px;padding:.5rem 1rem;border-radius:.375rem;cursor:pointer;
    border:1px solid currentColor;background:transparent;color:inherit}
  .consent button:focus-visible{outline:2px solid var(--consent-focus,#2563eb);outline-offset:2px}
  @media (prefers-color-scheme:dark){
    .consent{background:var(--consent-bg,#1a1a1a);color:var(--consent-fg,#f2f2f2);
      border-top-color:var(--consent-border,#3a3a3a)}
  }
</style>
<script>
  (function () {
    var DEFAULT = 'granted';
    var KEY = 'analytics-consent';
    var ONE_YEAR_S = 31536000;
    var el = document.getElementById('consent');
    function read() {
      var v = null;
      try { v = localStorage.getItem(KEY); } catch (e) {}
      if (!v) { var m = document.cookie.match(/(?:^|; )analytics-consent=(granted|denied)/); v = m && m[1]; }
      return v;
    }
    function write(v) {
      try { localStorage.setItem(KEY, v); } catch (e) {}
      document.cookie = KEY + '=' + v + '; Max-Age=' + ONE_YEAR_S + '; path=/; SameSite=Lax';
    }
    function clearGaCookies() {
      var parts = location.hostname.split('.');
      var domains = [''];
      for (var i = 0; i < parts.length - 1; i++) {
        var d = parts.slice(i).join('.');
        domains.push('; domain=' + d, '; domain=.' + d);
      }
      document.cookie.split(';').forEach(function (c) {
        var name = c.split('=')[0].trim();
        if (name.indexOf('_ga') !== 0) return;
        domains.forEach(function (d) {
          document.cookie = name + '=; Max-Age=0; path=/' + d;
        });
      });
    }
    function apply(v) {
      if (typeof window.gtag === 'function') window.gtag('consent', 'update', { analytics_storage: v });
      if (typeof window.clarity === 'function') window.clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: v });
      if (v === 'denied') clearGaCookies();
    }
    var stored = read();
    var choice = stored === 'granted' || stored === 'denied' ? stored : null;
    apply(choice || DEFAULT);
    if (choice || !el) return;
    el.hidden = false;
    var body = document.body;
    var basePad = body.style.paddingBottom;
    function pad() {
      body.style.paddingBottom = basePad;
      body.style.paddingBottom = (parseFloat(getComputedStyle(body).paddingBottom) || 0) + el.offsetHeight + 'px';
    }
    pad();
    window.addEventListener('resize', pad);
    el.addEventListener('click', function (e) {
      var btn = e.target.closest && e.target.closest('[data-consent]');
      if (!btn) return;
      var v = btn.getAttribute('data-consent');
      write(v);
      apply(v);
      el.hidden = true;
      window.removeEventListener('resize', pad);
      body.style.paddingBottom = basePad;
    });
  })();
</script>
```

## Rules

- Map the `--consent-*` custom properties to the host's own tokens. Set them on `.consent`, never on `:root`.
- Match the host's UI copy style, a11y rules and theme switch from its `CLAUDE.md` or `AGENTS.md`.
- Add no animation to the banner.
- Keep `ad_storage` denied.
- Guard every `window.gtag` and `window.clarity` call. A blocked script must cause no uncaught error.
- Keep the banner text to one short sentence.
- Keep the body padding code.
