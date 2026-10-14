/* Caverna Hair e Makeup · comportamento do site */
window.CONFIG = {
  instagram: 'andreiacaverna_hairemakeup',
  whatsapp: '5511972260964' // CONFIRMAR o DDD: o post mostra só 97226-0964
};

(function () {
  var doc = document.documentElement;
  var reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* abertura */
  requestAnimationFrame(function () { setTimeout(function () { doc.classList.add('pronto'); }, 60); });
  document.querySelectorAll('[data-ano]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* gaveta do menu (celular) */
  var nav = document.querySelector('.nav');
  var abrir = document.querySelector('.nav-abrir');
  var gaveta = document.querySelector('.nav-menu');
  if (abrir && gaveta) {
    function alternar(a) {
      abrir.setAttribute('aria-expanded', a);
      abrir.querySelector('span').textContent = a ? 'Fechar' : 'Menu';
      gaveta.classList.toggle('aberta', a);
      nav.classList.toggle('menu-aberto', a);
      document.body.style.overflow = a ? 'hidden' : '';
    }
    abrir.addEventListener('click', function () { alternar(abrir.getAttribute('aria-expanded') !== 'true'); });
    gaveta.addEventListener('click', function (e) { if (e.target.closest('a') && abrir.getAttribute('aria-expanded') === 'true') alternar(false); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape' && abrir.getAttribute('aria-expanded') === 'true') { alternar(false); abrir.focus(); } });
    matchMedia('(min-width: 1100px)').addEventListener('change', function (m) { if (m.matches) alternar(false); });
  }

  /* barra de progresso */
  var prog = document.querySelectorAll('[data-prog]');
  function aoRolar() {
    var t = Math.max(1, doc.scrollHeight - innerHeight);
    var p = Math.min(1, scrollY / t).toFixed(4);
    prog.forEach(function (el) { el.style.setProperty('--p', p); });
  }
  addEventListener('scroll', aoRolar, { passive: true });
  aoRolar();

  /* revelar ao rolar */
  var io = 'IntersectionObserver' in window && !reduz ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' }) : null;
  function revelar(els) {
    els.forEach(function (el, i) {
      el.classList.add('rv');
      if (!io) { el.classList.add('vis'); return; }
      el.style.transitionDelay = (i % 4) * 70 + 'ms';
      io.observe(el);
    });
  }
  revelar(document.querySelectorAll('[data-rv]'));

  /* fotos */
  var OBRAS = window.OBRAS || [];
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }
  function src(o, w) { return 'assets/obras/' + o.id + '-' + w + '.webp'; }
  function fig(o, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'obra';
    b.dataset.i = i;
    b.innerHTML = '<img src="' + src(o, 640) + '" alt="' + esc(o.d) + '" loading="lazy" decoding="async" width="640" height="' + Math.round(640 / o.r) + '">' +
      '<span class="leg">' + esc(o.d) + '</span>';
    return b;
  }
  var lista = OBRAS;
  var grade = document.querySelector('[data-grade]');
  if (grade) {
    var limite = +grade.dataset.limite || 0;
    var filtros = document.querySelectorAll('.filtros button');
    var ordem = grade.dataset.ordem ? grade.dataset.ordem.split(',').map(function (n) {
      return OBRAS.filter(function (o) { return o.id === 'ac-' + n; })[0];
    }).filter(Boolean) : null;
    function aplicar(e, empurrar) {
      lista = ordem || (e && e !== 'todos' ? OBRAS.filter(function (o) { return o.e === e; }) : OBRAS);
      grade.innerHTML = '';
      (limite ? lista.slice(0, limite) : lista).forEach(function (o) { grade.appendChild(fig(o, OBRAS.indexOf(o))); });
      revelar(grade.querySelectorAll('.obra'));
      filtros.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.f === (e || 'todos')); });
      if (empurrar && history.replaceState) history.replaceState(null, '', e && e !== 'todos' ? '?cat=' + e : location.pathname);
    }
    filtros.forEach(function (b) {
      var n = b.dataset.f === 'todos' ? OBRAS.length : OBRAS.filter(function (o) { return o.e === b.dataset.f; }).length;
      var s = b.querySelector('sup'); if (s) s.textContent = n;
      b.addEventListener('click', function () { aplicar(b.dataset.f, true); });
    });
    var q = new URLSearchParams(location.search).get('cat');
    aplicar(['cabelo', 'make', 'penteado'].indexOf(q) > -1 ? q : 'todos');
  }

  /* lightbox */
  var lb = document.querySelector('.lb');
  if (lb) {
    var img = lb.querySelector('img');
    var leg = lb.querySelector('[data-leg]');
    var cont = lb.querySelector('[data-cont]');
    var atual = 0, origem = null;
    function mostrar(k) {
      var n = lista.length;
      atual = (k + n) % n;
      var o = lista[atual];
      img.style.opacity = 0;
      var novo = new Image();
      novo.onload = function () { img.src = novo.src; img.alt = o.d; img.style.opacity = 1; };
      novo.src = src(o, 1200);
      leg.textContent = o.d;
      cont.textContent = String(atual + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0');
    }
    function abrirLb(o) {
      origem = document.activeElement;
      mostrar(lista.indexOf(o));
      lb.classList.add('aberto');
      lb.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      lb.querySelector('[data-fechar]').focus();
    }
    function fechar() {
      lb.classList.remove('aberto');
      lb.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (origem) origem.focus();
    }
    document.addEventListener('click', function (e) {
      var b = e.target.closest('.obra');
      if (b) abrirLb(OBRAS[+b.dataset.i]);
    });
    lb.querySelector('[data-fechar]').addEventListener('click', fechar);
    lb.querySelector('[data-ant]').addEventListener('click', function () { mostrar(atual - 1); });
    lb.querySelector('[data-prox]').addEventListener('click', function () { mostrar(atual + 1); });
    lb.querySelector('.lb-palco').addEventListener('click', function (e) { if (e.target === e.currentTarget) fechar(); });
    addEventListener('keydown', function (e) {
      if (!lb.classList.contains('aberto')) return;
      if (e.key === 'Escape') fechar();
      if (e.key === 'ArrowLeft') mostrar(atual - 1);
      if (e.key === 'ArrowRight') mostrar(atual + 1);
    });
    var x0 = null;
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) mostrar(atual + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  /* agendamento: monta a mensagem e abre o WhatsApp */
  var form = document.querySelector('[data-agendar]');
  if (form) {
    var previa = form.querySelector('.previa');
    var soCabelo = form.querySelectorAll('[data-so-cabelo]');
    var pre = new URLSearchParams(location.search).get('servico');
    if (pre) {
      var r = form.querySelector('[data-s="' + pre + '"]');
      if (r) r.checked = true;
    }
    function cabelo() {
      var s = form.querySelector('input[name=servico]:checked');
      return !s || s.hasAttribute('data-cabelo');
    }
    function texto() {
      var f = new FormData(form);
      var l = ['Oi, Andréia! Vim pelo site e queria agendar um horário.', ''];
      if (f.get('nome')) l.push('Nome: ' + f.get('nome'));
      if (f.get('servico')) l.push('Serviço: ' + f.get('servico'));
      if (cabelo() && f.get('quimica')) l.push('Cabelo hoje: ' + f.get('quimica'));
      if (f.get('local')) l.push('Onde: ' + f.get('local'));
      var per = f.getAll('periodo');
      if (per.length) l.push('Período: ' + per.join(', '));
      if (f.get('dia')) l.push('Data: ' + f.get('dia'));
      if (f.get('obs')) { l.push(''); l.push('Observações: ' + f.get('obs')); }
      return l.join('\n');
    }
    function atualizar() {
      var c = cabelo();
      soCabelo.forEach(function (el) { el.hidden = !c; });
      previa.textContent = texto();
    }
    form.addEventListener('input', atualizar);
    form.addEventListener('change', atualizar);
    atualizar();
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var erro = form.querySelector('.erro');
      if (erro) erro.remove();
      var faltando = !form.nome.value.trim() ? form.nome : !form.querySelector('input[name=servico]:checked') ? form.querySelector('input[name=servico]') : null;
      if (faltando) {
        var p = document.createElement('p');
        p.className = 'erro';
        p.setAttribute('role', 'alert');
        p.textContent = faltando.name === 'nome' ? 'Escreva seu nome para a Andréia saber com quem está falando.' : 'Escolha o serviço.';
        faltando.closest('.campo').after(p);
        faltando.focus();
        return;
      }
      window.open('https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(texto()), '_blank', 'noopener');
    });
  }
})();
