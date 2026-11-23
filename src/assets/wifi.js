// Managed Wi-Fi plan builder: home or business, who owns the equipment, a package, add-ons -> live totals.
(function () {
  var f = document.getElementById('wifi'), raw = document.getElementById('wifi-data');
  if (!f || !raw) return;
  var D = JSON.parse(raw.textContent);
  var $ = function (s) { return f.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(f.querySelectorAll(s)); };
  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  f.classList.add('js');

  function val(name) { var el = $('input[name="' + name + '"]:checked'); return el ? el.value : ''; }

  function pickDefault(seg) {
    var cur = $('input[name="plan"]:checked');
    if (cur && D.plans[cur.value].seg === seg) return;
    var feat = $$('.wplan[data-seg="' + seg + '"]').filter(function (l) { return l.classList.contains('feat'); })[0]
      || $('.wplan[data-seg="' + seg + '"]');
    if (feat) feat.querySelector('input').checked = true;
  }

  function addonLine(a, mode, n) {
    var p = a[mode], once = p.once * n, mo = p.monthly * n;
    return { label: (n > 1 ? n + ' × ' : '') + a.name, once: once, mo: mo };
  }

  function render() {
    var seg = val('seg') || 'home', mode = val('own') || 'own';
    f.dataset.seg = seg; f.dataset.own = mode;
    pickDefault(seg);
    var plan = D.plans[val('plan')];
    var quoteOnly = plan.quote && mode === 'lease';
    var lines = [], once = 0, mo = 0;
    if (plan.quote) {
      lines.push({ label: plan.name + (quoteOnly ? ' (custom quote)' : ' (from)'), once: quoteOnly ? 0 : plan.own.equip, mo: quoteOnly ? 0 : plan.own.monthly });
    } else if (mode === 'own') {
      lines.push({ label: 'Equipment', once: plan.own.equip, mo: 0 });
      lines.push({ label: 'Installation and setup', once: plan.own.setup, mo: 0 });
      lines.push({ label: 'Managed Wi-Fi', once: 0, mo: plan.own.monthly });
    } else {
      lines.push({ label: 'Setup (equipment included)', once: plan.lease.setup, mo: 0 });
      lines.push({ label: 'Equipment and managed Wi-Fi', once: 0, mo: plan.lease.monthly });
    }
    $$('.wadd').forEach(function (row) {
      var a = D.addons[row.dataset.id], hidden = row.dataset.only && row.dataset.only !== seg;
      row.hidden = !!hidden;
      if (hidden) return;
      var input = row.querySelector('input'), n = input.type === 'checkbox' ? (input.checked ? 1 : 0) : Math.max(0, Math.min(20, parseInt(input.value, 10) || 0));
      if (input.type !== 'checkbox' && String(n) !== input.value) input.value = n;
      if (n) lines.push(addonLine(a, mode, n));
    });
    lines.forEach(function (l) { once += l.once; mo += l.mo; });
    document.getElementById('ws-plan').textContent = plan.name + ' · ' + (seg === 'home' ? 'Home' : 'Small business') + ' · ' + (mode === 'own' ? 'You buy it' : 'We own it');
    document.getElementById('ws-lines').innerHTML = lines.map(function (l) {
      var p = [l.once ? money(l.once) : '', l.mo ? money(l.mo) + '/mo' : ''].filter(Boolean).join(' + ') || (quoteOnly ? 'Quote' : '–');
      return '<li><span></span><b></b></li>'.replace('<span></span>', '<span>' + esc(l.label) + '</span>').replace('<b></b>', '<b>' + p + '</b>');
    }).join('');
    document.getElementById('ws-once').textContent = quoteOnly ? 'Quote' : (plan.quote ? 'from ' : '') + money(once);
    document.getElementById('ws-mo').textContent = quoteOnly ? 'Quote' : (plan.quote ? 'from ' : '') + money(mo);
    var wb1 = document.getElementById('wb-once'), wb2 = document.getElementById('wb-mo');
    if (wb1) { wb1.textContent = document.getElementById('ws-once').textContent; wb2.textContent = document.getElementById('ws-mo').textContent; }
    document.getElementById('ws-note').textContent = mode === 'lease'
      ? D.term + '-month agreement. Failed equipment replaced free. Internet service not included.'
      : 'Plus sales tax on equipment. Internet service not included. Monthly plan is month to month.';
    var msg = 'Managed Wi-Fi quote request\n' + document.getElementById('ws-plan').textContent + '\n'
      + lines.map(function (l) { return '- ' + l.label + ': ' + ([l.once ? money(l.once) : '', l.mo ? money(l.mo) + '/mo' : ''].filter(Boolean).join(' + ') || 'quote'); }).join('\n')
      + '\nOne time: ' + (quoteOnly ? 'quote' : money(once)) + '  Monthly: ' + (quoteOnly ? 'quote' : money(mo)) + '\n\nAbout my building: ';
    document.getElementById('ws-quote').href = '/contact?service=' + encodeURIComponent('Managed Wi-Fi') + '&message=' + encodeURIComponent(msg) + '#quote';
  }

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  f.addEventListener('change', render);
  f.addEventListener('input', render);
  f.addEventListener('click', function (e) {
    var b = e.target.closest('.q-dn, .q-up');
    if (!b) return;
    var input = b.parentElement.querySelector('input');
    input.value = Math.max(0, Math.min(20, (parseInt(input.value, 10) || 0) + (b.classList.contains('q-dn') ? -1 : 1)));
    render();
  });
  render();
})();
