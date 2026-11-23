/* Progressive enhancement only — the page is complete without this file. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* current year in the footer */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  /* shadow line under the top bar once the page is scrolled */
  var bar = document.querySelector('.topbar');
  if (bar) {
    var onScroll = function () {
      bar.classList.toggle('stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  if (!('IntersectionObserver' in window)) return;

  /* fade sections in as they enter the viewport */
  if (!reduced) {
    var revealer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in');
        revealer.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

    document.querySelectorAll('.reveal').forEach(function (el) {
      revealer.observe(el);
    });
  }

  /* highlight the nav entry for the section in view */
  var links = {};
  document.querySelectorAll('.bar nav a[href^="#"]').forEach(function (a) {
    links[a.getAttribute('href').slice(1)] = a;
  });
  var targets = Object.keys(links)
    .map(function (id) { return document.getElementById(id); })
    .filter(Boolean);

  if (targets.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        for (var id in links) links[id].classList.remove('active');
        var active = links[e.target.id];
        if (active) active.classList.add('active');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    targets.forEach(function (t) { spy.observe(t); });
  }
})();
