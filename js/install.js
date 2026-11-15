(function () {
  'use strict';

  // Run only on installation page
  if (!document.body.classList.contains('installation')) return;

  var H = window.Helpers;

  function one(root, selector) {
    return root ? root.querySelector(selector) : null;
  }

  function all(root, selector) {
    return root ? Array.from(root.querySelectorAll(selector)) : [];
  }

  function directChild(el, className) {
    return el ? Array.from(el.children).find(function (child) { return child.classList.contains(className); }) || null : null;
  }

  function setAttrs(el, attrs) {
    if (!el) return;
    Object.keys(attrs).forEach(function (name) {
      if (attrs[name] === null) el.removeAttribute(name);
      else el.setAttribute(name, attrs[name]);
    });
  }

  var container = document.querySelector('.installationselection');
  var result = document.getElementById('result');
  var templates = Array.from(document.querySelectorAll('.instruction-collection'));
  var inst = document.querySelector('.installation-instructions');
  var wrap = directChild(result, 'instruction-wrap');
  var more = directChild(result, 'more');
  var docsLink = one(more, '.docs-link');
  var altToggle = one(more, '.alternative-options');
  var foldPlat = one(container, '.selection-foldout[data-foldout="platform"]');
  var foldEnv = one(container, '.selection-foldout[data-foldout="environment"]');
  var rgPlat = one(container, '.selection-options[data-role="platform"]');
  var rgEnv = one(container, '.selection-options[data-role="environment"]');

  var versionSwitch = one(inst, '.version-switch');
  var versionBtns = all(versionSwitch, '.version-switch-option');
  var versionSlider = one(versionSwitch, '.version-switch-slider');
  var altPanels = [];

  // Releases (e.g., '2.0', '1.5', '1.4'), newest first, as rendered from _data/releases.yml
  var VERSIONS = versionBtns.map(function (btn) { return btn.getAttribute('data-version'); });
  var ALIASES = {};
  var defaultLabels = new Map();
  versionBtns.forEach(function (btn) {
    var v = btn.getAttribute('data-version');
    defaultLabels.set(btn, btn.textContent);
    String(btn.getAttribute('data-aliases') || '').split(' ').forEach(function (a) {
      if (a) ALIASES[a] = v;
    });
  });

  var defaultVersion = container ? container.getAttribute('data-default-version') : null;
  if (VERSIONS.indexOf(defaultVersion) < 0) defaultVersion = VERSIONS[0];

  var state = {
    platform: null,
    environment: null,
    version: defaultVersion // the release selected by the user, see shownVersion()
  };

  function readURL() {
    try {
      var params = new URLSearchParams(window.location.search);
      state.platform = sanitizeParam(params.get('platform'));
      state.environment = sanitizeParam(params.get('environment'));
      var v = sanitizeParam(params.get('version'));
      v = ALIASES[v] || v;
      if (VERSIONS.indexOf(v) >= 0) state.version = v;
    } catch (e) {}
  }

  function writeURL() {
    try {
      var params = new URLSearchParams(window.location.search);
      setOrDelete(params, 'platform', state.platform);
      setOrDelete(params, 'environment', state.environment);
      setOrDelete(params, 'version', state.version !== defaultVersion ? state.version : null);
      var newQuery = params.toString();
      var newUrl = window.location.pathname + (newQuery ? '?' + newQuery : '') + window.location.hash;
      var prevQuery = window.location.search.replace(/^\?/, '');
      if (prevQuery !== newQuery) {
        window.history.replaceState({}, '', newUrl);
      }
    } catch (e) {}
  }

  function setOrDelete(params, key, val) {
    if (val && String(val).length) params.set(key, String(val));
    else params.delete(key);
  }

  function sanitizeParam(val) {
    if (val == null) return null;
    val = String(val).trim().toLowerCase();
    if (!val) return null;
    return val;
  }

  function defaultState() {
    var pf = window.detectPlatform();
    return {
      platform: pf,
      environment: 'cli'
    };
  }

  function normalizeState() {
    var def = defaultState();

    var activePlatform = one(container, '.selection-options[data-role="platform"] .option.active');
    state.platform = state.platform || (activePlatform && activePlatform.dataset.value || null) || def.platform;

    var activeEnv = one(container, '.selection-options[data-role="environment"] .option.active');
    state.environment = state.environment || (activeEnv && activeEnv.dataset.value || null) || def.environment;
  }

  function groupFor(role) {
    if (role === 'platform') return rgPlat;
    if (role === 'environment') return rgEnv;
    return null;
  }

  function selectOption(role, value) {
    if (!role) return;
    var group = groupFor(role);
    if (!group) return;

    var options = all(group, '.option');
    var opt = options.find(function (o) {
      return String(o.dataset.value) === String(value);
    });

    if (!opt) return;

    options.forEach(function (o) {
      o.classList.remove('active');
      setAttrs(o, { 'aria-checked': 'false', 'tabindex': '-1' });
    });
    opt.classList.add('active');
    setAttrs(opt, { 'aria-checked': 'true', 'tabindex': '0' });

    state[role] = value;
  }

  function applyUIFromState() {
    selectOption('platform', state.platform);
    selectOption('environment', state.environment);
  }

  function labelFor(role) {
    var group = groupFor(role);
    if (!group) return '';
    var opt = one(group, '.option.active');
    if (!opt) return '';
    var displayLabel = opt.getAttribute('data-display-label');
    if (displayLabel) return displayLabel.trim();
    var label = one(opt, '.label');
    return ((label && label.textContent) || opt.textContent || '').trim();
  }

  function setFoldoutOpen(foldout, open, animate) {
    if (!foldout) return;
    var content = directChild(foldout, 'selection-content');
    var changed = foldout.classList.contains('open') !== open;
    all(foldout, '.selection-head button').forEach(function (btn) {
      btn.setAttribute('aria-expanded', String(open));
    });
    foldout.classList.toggle('open', open);
    if (!content) return;
    H.stop(content);
    if (open) {
      if (animate && changed) {
        content.style.display = 'none';
        H.slideDown(content, 150);
      } else {
        H.show(content);
      }
    } else {
      if (animate && changed) {
        content.style.display = 'block';
        H.slideUp(content, 150);
      } else {
        H.hide(content);
      }
    }
  }

  function updateHeadings() {
    var envLabel = labelFor('environment');
    var envSelected = one(foldEnv, '.selection-head .selected');
    if (envSelected) envSelected.textContent = envLabel ? ' ' + envLabel : '';

    var platLabel = labelFor('platform');
    var needsPlatform = environmentRequiresPlatform(state.environment);
    if (!needsPlatform) {
      platLabel = '';
    }
    var text = platLabel ? ' ' + platLabel : '';
    var platSelected = one(foldPlat, '.selection-head .selected');
    if (platSelected) platSelected.textContent = needsPlatform ? text : 'Not required';

    if (!container) return;
    var live = one(container, '.live-region');
    if (!live) {
      live = document.createElement('div');
      live.className = 'visually-hidden live-region';
      live.setAttribute('aria-live', 'polite');
      container.appendChild(live);
    }
    var liveText = [];
    if (envLabel) liveText.push(envLabel);
    if (platLabel) liveText.push(platLabel);
    live.textContent = liveText.join(', ');
  }

  function findInTemplates(selector) {
    return templates.reduce(function (found, tpl) {
      return found.concat(Array.from(tpl.querySelectorAll(selector)));
    }, []);
  }

  function templatesFor(v) {
    var envSel = '[data-environment="' + cssEscape(state.environment) + '"]';
    return findInTemplates(envSel + '[data-release="' + cssEscape(v) + '"]');
  }

  function hasVersion(v) {
    return templatesFor(v).length > 0;
  }

  // The selected release, or the newest one offering the selected client
  function shownVersion() {
    return hasVersion(state.version) ? state.version : (VERSIONS.filter(hasVersion)[0] || state.version);
  }

  // Label the buttons with the client's version, e.g., the JDBC driver's version for Java
  function updateVersionButtons() {
    versionBtns.forEach(function (btn) {
      var tpl = templatesFor(btn.getAttribute('data-version'))[0];
      var label = tpl ? tpl.getAttribute('data-label') : null;
      var suffix = btn.getAttribute('data-suffix');
      btn.textContent = label ? label + (suffix ? ' (' + suffix + ')' : '') : defaultLabels.get(btn);
    });
    positionSlider();
  }

  function updateVersionToggle() {
    var shown = shownVersion();
    versionBtns.forEach(function (btn) {
      var v = btn.getAttribute('data-version');
      var isActive = v === shown;
      var isAvailable = hasVersion(v);

      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-checked', String(isActive));
      btn.disabled = !isAvailable;
      btn.setAttribute('aria-disabled', String(!isAvailable));
    });

    positionSlider();
  }

  function positionSlider() {
    var active = versionBtns.find(function (btn) { return btn.classList.contains('active'); });
    var toggle = one(versionSwitch, '.version-switch-toggle');
    if (!active || !toggle || !versionSlider) return;

    var activeRect = active.getBoundingClientRect();
    var offset = activeRect.left - toggle.getBoundingClientRect().left;
    versionSlider.style.width = activeRect.width + 'px';
    versionSlider.style.transform = 'translateX(' + offset + 'px)';
  }

  function updateFoldouts(animate) {
    var needsPlatform = environmentRequiresPlatform(state.environment);
    all(foldPlat, '.selection-head button').forEach(function (btn) {
      btn.disabled = !needsPlatform;
    });
    var platOptions = all(rgPlat, '.option');

    if (!needsPlatform) {
      setFoldoutOpen(foldPlat, false, !!animate);
      if (foldPlat) {
        foldPlat.classList.add('disabled');
        foldPlat.setAttribute('aria-disabled', 'true');
      }
      setAttrs(rgPlat, { 'aria-disabled': 'true' });
      platOptions.forEach(function (o) {
        setAttrs(o, { 'aria-disabled': 'true', 'tabindex': '-1' });
      });
      return;
    }

    if (foldPlat) {
      foldPlat.classList.remove('disabled');
      foldPlat.removeAttribute('aria-disabled');
    }
    setAttrs(rgPlat, { 'aria-disabled': null });
    platOptions.forEach(function (o) {
      o.setAttribute('aria-disabled', 'false');
    });
    var activePlat = platOptions.find(function (o) { return o.classList.contains('active'); });
    platOptions.forEach(function (o, i) {
      var focusable = activePlat ? o === activePlat : i === 0;
      o.setAttribute('tabindex', focusable ? '0' : '-1');
    });

    var shouldClosePlat = !!state.platform;
    setFoldoutOpen(foldPlat, !shouldClosePlat, !!animate);
  }

  function findTemplate(environment, platform, version) {
    var envSel = '[data-environment="' + cssEscape(environment) + '"]';
    var candidates = findInTemplates(envSel + '[data-release="' + cssEscape(version) + '"]');

    if (platform) {
      var match = candidates.find(function (c) { return c.matches('[data-platform="' + cssEscape(platform) + '"]'); });
      if (match) return match;
    }

    // Fallback: environment-only (e.g., Python, Node.js)
    return candidates.find(function (c) { return !c.hasAttribute('data-platform'); }) || null;
  }

  function bestTemplate() {
    if (!state.environment) return null;
    return findTemplate(state.environment, state.platform, shownVersion());
  }

  function environmentRequiresPlatform(environment) {
    if (!environment) return false;
    var selEnvOnly = '[data-environment="' + cssEscape(environment) + '"]:not([data-platform])';
    if (findInTemplates(selEnvOnly).length) return false;
    var selWithPlatform = '[data-environment="' + cssEscape(environment) + '"][data-platform]';
    return findInTemplates(selWithPlatform).length > 0;
  }

  function disableAltToggle() {
    altPanels = [];
    if (!altToggle) return;
    H.hide(altToggle);
    setAttrs(altToggle, { 'aria-expanded': 'false', 'aria-controls': null, 'tabindex': '-1', 'role': null });
  }

  function render() {
    var tpl = bestTemplate();

    if (!tpl) {
      if (wrap) wrap.innerHTML = '';
      disableAltToggle();
      if (docsLink) {
        docsLink.removeAttribute('href');
        H.hide(docsLink);
        setAttrs(docsLink, { 'aria-disabled': 'true', 'tabindex': '-1' });
      }
      if (inst) H.hide(inst);
      return;
    }

    if (wrap) {
      wrap.innerHTML = tpl.innerHTML;
      all(wrap, '.more').forEach(function (el) { el.remove(); });
    }

    updateMore(tpl);
    if (inst) H.show(inst);
  }

  function updateMore(tpl) {
    var docs = String((tpl && tpl.getAttribute('data-docs')) || '').trim();

    if (docsLink) {
      if (docs) {
        docsLink.setAttribute('href', docs);
        H.show(docsLink);
        setAttrs(docsLink, { 'aria-disabled': null, 'tabindex': '0' });
      } else {
        docsLink.removeAttribute('href');
        H.hide(docsLink);
        setAttrs(docsLink, { 'aria-disabled': 'true', 'tabindex': '-1' });
      }
    }

    var panels = all(result, '.alternative');

    if (panels.length) {
      panels.forEach(function (panel) {
        H.hide(panel);
        panel.id = 'alt-panel';
      });
      altPanels = panels;
      if (altToggle) {
        H.show(altToggle);
        setAttrs(altToggle, { 'aria-expanded': 'false', 'aria-controls': 'alt-panel', 'role': 'button', 'tabindex': '0' });
      }
    } else {
      disableAltToggle();
    }
  }

  function onAltToggleClick(e) {
    if (!altPanels.length) return;
    e.preventDefault();
    var expanded = altToggle.getAttribute('aria-expanded') === 'true';
    altToggle.setAttribute('aria-expanded', String(!expanded));
    altPanels.forEach(function (panel) {
      H.slideToggle(panel, 150);
    });
  }

  function onOptionActivate(opt) {
    if (opt.getAttribute('aria-disabled') === 'true' || opt.classList.contains('disabled')) return;

    var group = opt.closest('.selection-options');
    var role = String((group && group.dataset.role) || '');
    var value = String(opt.dataset.value || '');

    if (!role || !value) return;

    selectOption(role, value);
    opt.focus();

    writeURL();
    render();
    updateHeadings();
    updateVersionToggle();
    updateVersionButtons();
    updateFoldouts(true);
  }

  function closestInContainer(target, selector) {
    var el = target.closest(selector);
    return el && container.contains(el) ? el : null;
  }

  function wire() {
    all(container, '.selection-options[data-role]').forEach(function (group) {
      group.setAttribute('role', 'radiogroup');
    });
    all(container, '.selection-options .option').forEach(function (opt) {
      opt.setAttribute('role', 'radio');
    });

    if (container) {
      container.addEventListener('click', function (e) {
        var opt = closestInContainer(e.target, '.selection-options .option');
        if (opt) {
          e.stopPropagation();
          onOptionActivate(opt);
          return;
        }
        var head = closestInContainer(e.target, '.selection-head');
        if (head) {
          e.stopPropagation();
          var headFold = head.closest('.selection-foldout');
          if (headFold && !headFold.classList.contains('disabled')) {
            setFoldoutOpen(headFold, !headFold.classList.contains('open'), true);
          }
          return;
        }
        if (closestInContainer(e.target, '.selection-content')) {
          e.stopPropagation();
          return;
        }
        var fold = closestInContainer(e.target, '.selection-foldout');
        if (fold && !fold.classList.contains('disabled') && !fold.classList.contains('open')) {
          setFoldoutOpen(fold, true, true);
        }
      });

      container.addEventListener('keydown', function (e) {
        var opt = closestInContainer(e.target, '.selection-options .option');
        if (!opt) return;
        var key = e.key;

        if (key === 'Enter' || key === ' ') {
          e.preventDefault();
          onOptionActivate(opt);
          return;
        }

        if (key === 'ArrowRight' || key === 'ArrowDown' || key === 'ArrowLeft' || key === 'ArrowUp') {
          e.preventDefault();
          var group = opt.closest('.selection-options');
          var opts = all(group, '.option').filter(function (o) {
            return o.getAttribute('aria-disabled') !== 'true' && !o.classList.contains('disabled');
          });
          var idx = opts.indexOf(opt);
          if (idx < 0) return;
          var dir = (key === 'ArrowRight' || key === 'ArrowDown') ? 1 : -1;
          var next = opts[(idx + dir + opts.length) % opts.length];
          onOptionActivate(next);
          next.focus();
        }
      });
    }

    all(container, '.selection-foldout').forEach(function (fold) {
      setFoldoutOpen(fold, fold.classList.contains('open'), false);
    });

    all(container, '.selection-options[data-role]').forEach(function (group) {
      var opts = all(group, '.option');
      var active = opts.find(function (o) { return o.classList.contains('active'); });
      opts.forEach(function (o, i) {
        var focusable = active ? o === active : i === 0;
        o.setAttribute('tabindex', focusable ? '0' : '-1');
      });
    });

    if (altToggle) altToggle.addEventListener('click', onAltToggleClick);

    if (versionSwitch) {
      // Version switch toggle
      versionSwitch.addEventListener('click', function (e) {
        var btn = e.target.closest('.version-switch-option');
        if (!btn || !versionSwitch.contains(btn)) return;
        e.preventDefault();
        var newVersion = btn.getAttribute('data-version');
        if (newVersion === state.version) return;
        state.version = newVersion;
        writeURL();
        render();
        updateVersionToggle();
        updateVersionButtons();
      });

      versionSwitch.addEventListener('keydown', function (e) {
        var btn = e.target.closest('.version-switch-option');
        if (!btn || !versionSwitch.contains(btn)) return;
        var key = e.key;
        if (key === 'ArrowRight' || key === 'ArrowLeft') {
          e.preventDefault();
          var enabled = versionBtns.filter(function (b) { return !b.disabled; });
          var idx = enabled.indexOf(btn);
          if (idx < 0) return;
          var dir = key === 'ArrowRight' ? 1 : -1;
          var next = enabled[(idx + dir + enabled.length) % enabled.length];
          next.click();
          next.focus();
        }
      });
    }
  }

  function cssEscape(str) {
    var s = String(str);
    if (window.CSS && CSS.escape) return CSS.escape(s);
    return s.replace(/[^a-zA-Z0-9_-]/g, '\\$&');
  }

  // Init
  readURL();
  normalizeState();
  applyUIFromState();
  writeURL();
  document.querySelectorAll('.installation-instructions').forEach(function (el) { H.hide(el); });
  render();
  updateHeadings();
  updateVersionToggle();
  updateVersionButtons();
  updateFoldouts(false);
  wire();
})();
