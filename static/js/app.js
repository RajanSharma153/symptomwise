document.addEventListener('DOMContentLoaded', () => {

  const themeToggle = document.getElementById('themeToggle');
  const applyTheme = theme => {
    document.documentElement.dataset.theme = theme;
    if (themeToggle) {
      const dark = theme === 'dark';
      themeToggle.setAttribute('aria-label', dark ? 'लाइट मोड चालू करें' : 'डार्क मोड चालू करें');
      themeToggle.title = dark ? 'लाइट मोड' : 'डार्क मोड';
      const icon = themeToggle.querySelector('.theme-icon');
      const label = themeToggle.querySelector('.theme-label');
      if (icon) icon.textContent = dark ? '☀' : '☾';
      if (label) label.textContent = dark ? 'लाइट मोड' : 'डार्क मोड';
    }
  };
  let savedTheme = null;
  try { savedTheme = localStorage.getItem('symptomwise-theme'); } catch (e) {}
  const systemDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(savedTheme || (systemDark ? 'dark' : 'light'));
  if (themeToggle) themeToggle.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem('symptomwise-theme', next); } catch (e) {}
  });


  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const open = navLinks.classList.toggle('nav-open');
      navToggle.classList.toggle('is-open', open);
      navToggle.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('menu-open', open);
    });
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      navLinks.classList.remove('nav-open'); navToggle.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false'); document.body.classList.remove('menu-open');
    }));
  }

  const search = document.getElementById('symptomSearch');
  const chips = [...document.querySelectorAll('.symptom-chip')];
  const count = document.getElementById('selectedCount');
  const updateCount = () => {
    const n = document.querySelectorAll('.symptom-chip input:checked').length;
    if (count) count.textContent = n;
    document.querySelectorAll('.symptom-chip').forEach(chip => chip.classList.toggle('is-selected', chip.querySelector('input').checked));
  };
  chips.forEach(chip => chip.querySelector('input').addEventListener('change', updateCount));
  updateCount();
  if (search) search.addEventListener('input', () => {
    const q = search.value.trim().toLowerCase();
    chips.forEach(chip => chip.classList.toggle('is-hidden', !chip.dataset.symptom.includes(q)));
  });

  const form = document.getElementById('symptomForm');
  if (form) form.addEventListener('submit', event => {
    if (!form.querySelector('input:checked')) {
      event.preventDefault();
      const panel = document.querySelector('.symptom-panel');
      panel.classList.remove('nudge'); void panel.offsetWidth; panel.classList.add('nudge');
      panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
      if (search) search.focus();
    }
  });

  const revealItems = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }), { threshold: 0.12, rootMargin: '0px 0px -35px 0px' });
    revealItems.forEach(item => observer.observe(item));
  } else revealItems.forEach(item => item.classList.add('is-visible'));
});
