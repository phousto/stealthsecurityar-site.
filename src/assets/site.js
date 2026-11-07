// Mobile menu, dropdown toggles, and quote form.
(function () {
  var mt = document.querySelector('.menu-t'), nav = document.getElementById('mainnav');
  if (mt && nav) mt.addEventListener('click', function () {
    var open = nav.classList.toggle('open'); mt.setAttribute('aria-expanded', open);
  });
  document.querySelectorAll('.dd-t').forEach(function (b) {
    b.addEventListener('click', function () {
      var li = b.parentElement, open = li.classList.toggle('open'); b.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') document.querySelectorAll('.dd.open').forEach(function (d) { d.classList.remove('open'); });
  });

  var f = document.getElementById('quote');
  if (!f) return;
  var status = f.querySelector('.form-status');
  function say(msg, cls) { status.textContent = msg; status.className = 'form-status ' + (cls || ''); }
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = Object.fromEntries(new FormData(f).entries());
    if (d.company_website) return; // spam trap
    if (!d.name || !d.email || !d.message) return say('Please fill in your name, email and message.', 'err');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)) return say('Please check your email address.', 'err');
    var ep = f.dataset.endpoint;
    if (ep) {
      say('Sending…');
      fetch(ep, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
        .then(function (r) { if (!r.ok) throw 0; f.reset(); say('Thanks! We received your request and will be in touch soon.', 'ok'); })
        .catch(function () { say('That didn\'t send. Please call 1-479-746-8298 or email ' + f.dataset.email + '.', 'err'); });
    } else {
      var body = 'Name: ' + d.name + '\nEmail: ' + d.email + '\nPhone: ' + (d.phone || '') + '\nTown: ' + (d.town || '') + '\nService: ' + (d.service || '') + '\n\n' + d.message;
      location.href = 'mailto:' + f.dataset.email + '?subject=' + encodeURIComponent('Quote request from ' + d.name) + '&body=' + encodeURIComponent(body);
      say('Your email app should open with your request filled in. If it doesn\'t, call 1-479-746-8298.', 'ok');
    }
  });
})();
