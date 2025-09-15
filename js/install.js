(function ($) {
  'use strict';

  $(function () {
    // Run only on installation page
    if (!$('body').hasClass('installation')) return;

    var $container = $('.installationselection');
    var $result = $('#result');
    var $templates = $('.instruction-collection');
    var $inst = $('.installation-instructions');
    var $hint = $('.installation-hint');
    var $wrap = $result.children('.instruction-wrap');
    var $more = $result.children('.more');
    var $docsLink = $more.find('.docs-link');
    var $altToggle = $more.find('.alternative-options');
    var $foldPlat = $container.find('.selection-foldout[data-foldout="platform"]');
    var $foldEnv = $container.find('.selection-foldout[data-foldout="environment"]');
    var $rgPlat = $container.find('.selection-options[data-role="platform"]');
    var $rgEnv = $container.find('.selection-options[data-role="environment"]');
    var $rgArch = $container.find('.selection-options[data-role="architecture"]');
    var $archWrap = $container.find('.architecture-wrap');

    var state = {
      platform: null,
      environment: null,
      architecture: null
    };

    var urlFlags = {
      archFromURL: false,
      envFromURL: false
    };

    function detectPlatform() {
      var p = (navigator.platform || '') + ' ' + (navigator.userAgent || '');
      if (/Mac/i.test(p)) return 'macos';
      if (/Win/i.test(p)) return 'windows';
      if (/Linux|X11/i.test(p)) return 'linux';
      return 'macos';
    }

    function readURL() {
      try {
        var params = new URLSearchParams(window.location.search);
        state.platform = sanitizeParam(params.get('platform'));
        state.environment = sanitizeParam(params.get('environment'));
        state.architecture = sanitizeParam(params.get('architecture'));
        urlFlags.archFromURL = params.has('architecture');
        urlFlags.envFromURL = params.has('environment');
      } catch (e) {}
    }

    function writeURL() {
      try {
        var params = new URLSearchParams(window.location.search);
        setOrDelete(params, 'platform', state.platform);
        setOrDelete(params, 'environment', state.environment);
        setOrDelete(params, 'architecture', state.architecture);
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
      var pf = detectPlatform();
      return {
        platform: pf,
        environment: 'cli',
        architecture: null
      };
    }

    function normalizeState() {
      var def = defaultState();

      var $activePlatform = $container.find('.selection-options[data-role="platform"] .option.active').first();
      state.platform = state.platform || ($activePlatform.data('value') || null) || def.platform;

      var $activeEnv = $container.find('.selection-options[data-role="environment"] .option.active').first();
      state.environment = state.environment || ($activeEnv.data('value') || null) || def.environment;

      var $activeArch = $container.find('.selection-options[data-role="architecture"] .option.active').first();
      state.architecture = state.architecture || ($activeArch.data('value') || null) || def.architecture;
    }

    function selectOption(role, value) {
      if (!role) return;
      var $group = role === 'platform' ? $rgPlat : role === 'environment' ? $rgEnv : role === 'architecture' ? $rgArch : $();
      if (!$group.length) return;

      var $opt = $group.find('.option').filter(function () {
        return String($(this).data('value')) === String(value);
      }).first();

      if (!$opt.length) return;

      $group.find('.option')
        .removeClass('active')
        .attr('aria-checked', 'false')
        .attr('tabindex', '-1');
      $opt
        .addClass('active')
        .attr('aria-checked', 'true')
        .attr('tabindex', '0')
        .focus();

      state[role] = value;
    }

    // Reset architecture selection (used on platform change)
    function clearArchitectureSelection() {
      var $opts = $rgArch.find('.option');
      if (!$opts.length) {
        state.architecture = null;
        return;
      }
      $opts
        .removeClass('active')
        .attr('aria-checked', 'false')
        .attr('tabindex', '-1');
      $opts.first().attr('tabindex', '0');
      state.architecture = null;
    }

    function applyUIFromState() {
      selectOption('platform', state.platform);
      selectOption('environment', state.environment);
      if (state.architecture) {
        selectOption('architecture', state.architecture);
      }
    }

    // Default architecture detection via UAParser (never overrides user/URL)
    async function detectArchitecture() {
      try {
        if (window.UAParser) {
          var result = new UAParser().getResult();
          var arch = (result && result.cpu && result.cpu.architecture) ? String(result.cpu.architecture).toLowerCase() : '';
          if (/^(arm64|aarch64)$/.test(arch)) return 'arm64';
          if (/^(amd64|x86_64|x86-64|x64)$/.test(arch)) return 'x86_64';
          var osName = (result && result.os && result.os.name) ? String(result.os.name).toLowerCase() : '';
          if (/windows/.test(osName)) return 'x86_64';
          if (/mac\s?os|macos/.test(osName)) return 'arm64';
          if (/linux/.test(osName)) return 'x86_64';
          return null;
        }
      } catch (e) {}
      return null;
    }

    function labelFor(role) {
      var $group = role === 'platform' ? $rgPlat : role === 'environment' ? $rgEnv : role === 'architecture' ? $rgArch : $();
      var $opt = $group.find('.option.active').first();
      var txt = $.trim($opt.find('.label').text() || $opt.text() || '');
      return txt;
    }

    function setFoldoutOpen($foldout, open, animate) {
      var $content = $foldout.children('.selection-content');
      if (open) {
        $foldout.addClass('open');
        if (animate) $content.stop(true, true).slideDown(150); else $content.show();
      } else {
        $foldout.removeClass('open');
        if (animate) $content.stop(true, true).slideUp(150); else $content.hide();
      }
    }

    function updateHeadings() {
      var envLabel = labelFor('environment');
      $foldEnv.find('.selection-head .selected').text(envLabel ? ' ' + envLabel : '');

      var platLabel = labelFor('platform');
      var arch = (state.platform === 'macos') ? '' : (state.architecture ? String(state.architecture) : '');
      var parts = [];
      if (platLabel) parts.push(platLabel);
      if (arch) parts.push(arch);
      var text = parts.length ? ' ' + parts.join(', ') : '';
      $foldPlat.find('.selection-head .selected').text(text);

      var $live = $container.find('.live-region');
      if (!$live.length) {
        $live = $('<div class="visually-hidden live-region" aria-live="polite"></div>').appendTo($container);
      }
      var liveText = [];
      if (envLabel) liveText.push(envLabel);
      if (platLabel) liveText.push(platLabel);
      if (arch) liveText.push(arch);
      $live.text(liveText.join(', '));
    }

    function updateFoldouts(animate) {
      var shouldClosePlat = !!state.platform && (state.platform === 'macos' || !!state.architecture);
      setFoldoutOpen($foldPlat, !shouldClosePlat, !!animate);
    }

    function bestTemplate() {
      var p = state.platform;
      var e = state.environment;
      var a = state.architecture;

      if (!p || !e) return $();

      var selExact = '[data-platform="' + cssEscape(p) + '"][data-environment="' + cssEscape(e) + '"]';
      if (a) selExact += '[data-architecture="' + cssEscape(a) + '"]';
      var $exact = $templates.find(selExact).first();
      if ($exact.length) return $exact;

      if (a) {
        var selEnvArchNoPlat = '[data-environment="' + cssEscape(e) + '"][data-architecture="' + cssEscape(a) + '"]:not([data-platform])';
        var $envArchNoPlat = $templates.find(selEnvArchNoPlat).first();
        if ($envArchNoPlat.length) return $envArchNoPlat;
      }

      var selWildcard = '[data-platform="' + cssEscape(p) + '"][data-environment="' + cssEscape(e) + '"]:not([data-architecture]), ' +
                        '[data-platform="' + cssEscape(p) + '"][data-environment="' + cssEscape(e) + '"][data-architecture=""]';
      var $wild = $templates.find(selWildcard).first();
      if ($wild.length) return $wild;

      var selEnvOnly = '[data-environment="' + cssEscape(e) + '"]:not([data-platform]):not([data-architecture])';
      var $envOnly = $templates.find(selEnvOnly).first();
      if ($envOnly.length) return $envOnly;

      return $();
    }

    // Return true if architecture choice is required for current platform+environment
    function requiresArchitecture(p, e) {
      if (!e) return false;
      // env-only snippet available -> no architecture required
      var selEnvOnly = '[data-environment="' + cssEscape(e) + '"]:not([data-platform]):not([data-architecture])';
      if ($templates.find(selEnvOnly).length) return false;
      if (!p) return false;
      // platform+env without architecture exists -> no architecture required
      var selPlatEnvNoArch = '[data-platform="' + cssEscape(p) + '"][data-environment="' + cssEscape(e) + '"]:not([data-architecture])';
      if ($templates.find(selPlatEnvNoArch).length) return false;
      // otherwise architecture is required
      return true;
    }

    function render() {
      // If environment is selected but architecture is missing and required, show hint instead of instructions
      if (state.environment && !state.architecture && requiresArchitecture(state.platform, state.environment)) {
        if ($wrap.length) $wrap.empty();
        // neutralize .more area
        $altToggle
          .hide()
          .attr('aria-expanded', 'false')
          .off('click.install')
          .removeAttr('aria-controls')
          .attr('tabindex', '-1')
          .removeAttr('role');
        $docsLink
          .removeAttr('href')
          .hide()
          .attr('aria-disabled', 'true')
          .attr('tabindex', '-1');
        $inst.hide();
        if ($hint && $hint.length) $hint.show();
        return;
      } else {
        if ($hint && $hint.length) $hint.hide();
      }

      var $tpl = bestTemplate();

      if (!$tpl.length) {
        if ($wrap.length) $wrap.empty();

        $altToggle
          .hide()
          .attr('aria-expanded', 'false')
          .off('click.install')
          .removeAttr('aria-controls')
          .attr('tabindex', '-1')
          .removeAttr('role');

        $more.find('.docs-link')
          .removeAttr('href')
          .hide()
          .attr('aria-disabled', 'true')
          .attr('tabindex', '-1');

        $inst.hide();
        return;
      }

      if ($wrap.length) {
        $wrap.html($tpl.html());
        $wrap.find('.more').remove();
      } else {
        $result.html($tpl.html());
      }

      updateMore($tpl);
      $inst.show();
    }

    function updateMore($tpl) {
      var docs = String(($tpl && $tpl.attr('data-docs')) || '').trim();

      if (docs) {
        $docsLink.attr('href', docs).show().removeAttr('aria-disabled').attr('tabindex', '0');
      } else {
        $docsLink.removeAttr('href').hide().attr('aria-disabled', 'true').attr('tabindex', '-1');
      }

      var $alt = $result.find('.alternative');

      if ($alt.length) {
        $alt.hide().attr('id', 'alt-panel');
        $altToggle
          .show()
          .attr('aria-expanded', 'false')
          .attr('aria-controls', 'alt-panel')
          .attr('role', 'button')
          .attr('tabindex', '0')
          .off('click.install')
          .on('click.install', function (e) {
            e.preventDefault();
            var expanded = $(this).attr('aria-expanded') === 'true';
            $(this).attr('aria-expanded', String(!expanded));
            $alt.stop(true, true).slideToggle(150);
          });
      } else {
        $altToggle
          .hide()
          .off('click.install')
          .removeAttr('aria-controls')
          .attr('aria-expanded', 'false')
          .removeAttr('role')
          .attr('tabindex', '-1');
      }
    }

    function updateAvailability() {
      var $group = $rgArch;
      if (!$group.length) return;
      $group.find('.option')
        .removeClass('disabled')
        .attr('aria-disabled', 'false')
        .attr('tabindex', '0');
    }

    function updateArchitectureVisibility() {
      if ($archWrap && $archWrap.length) {
        if (state.platform === 'macos') {
          $archWrap.hide();
        } else {
          $archWrap.show();
        }
      }
    }

    function onOptionActivate($opt) {
      if ($opt.attr('aria-disabled') === 'true' || $opt.hasClass('disabled')) return;

      var $group = $opt.closest('.selection-options');
      var role = String($group.data('role') || '');
      var value = String($opt.data('value') || '');

      if (!role || !value) return;

      selectOption(role, value);

      // Reset architecture on platform change
      if (role === 'platform') {
        clearArchitectureSelection();
        updateArchitectureVisibility();
      }

      if (role !== 'architecture') {
        updateAvailability();
      }

      writeURL();
      render();
      updateHeadings();
      updateFoldouts(true);
    }

    function wire() {
      $rgPlat.add($rgEnv).add($rgArch).attr('role', 'radiogroup');
      $container.find('.selection-options .option').attr('role', 'radio');

      $container.on('click', '.selection-options .option', function (e) {
        e.stopPropagation();
        onOptionActivate($(this));
      });

      $container.on('click', '.selection-content', function (e) {
        e.stopPropagation();
      });

      $container.on('click', '.selection-foldout', function () {
        var $fold = $(this);
        if (!$fold.hasClass('open')) {
          var $content = $fold.children('.selection-content');
          $content.stop(true, true).slideDown(150);
          $fold.addClass('open');
        }
      });

      $container.on('click', '.selection-head', function (e) {
        e.stopPropagation();
        var $fold = $(this).closest('.selection-foldout');
        var $content = $fold.children('.selection-content');
        if ($fold.hasClass('open')) {
          $content.stop(true, true).slideUp(150);
          $fold.removeClass('open');
        } else {
          $content.stop(true, true).slideDown(150);
          $fold.addClass('open');
        }
      });

      $container.find('.selection-foldout').each(function () {
        var $fold = $(this);
        var isOpen = $fold.hasClass('open');
        var $content = $fold.children('.selection-content');
        if (isOpen) $content.show(); else $content.hide();
      });

      $rgPlat.add($rgEnv).add($rgArch).each(function () {
        var $group = $(this);
        var $opts = $group.find('.option');
        var $active = $opts.filter('.active').first();
        if ($active.length) {
          $opts.not($active).attr('tabindex', '-1');
          $active.attr('tabindex', '0');
        } else {
          $opts.attr('tabindex', '-1');
          $opts.first().attr('tabindex', '0');
        }
      });

      $container.on('keydown', '.selection-options .option', function (e) {
        var key = e.key || e.keyCode;

        if (key === 'Enter' || key === ' ' || key === 13 || key === 32) {
          e.preventDefault();
          onOptionActivate($(this));
          return;
        }

        if (key === 'ArrowRight' || key === 'ArrowDown' || key === 'ArrowLeft' || key === 'ArrowUp') {
          e.preventDefault();
          var $group = $(this).closest('.selection-options');
          var $opts = $group.find('.option').filter(function () {
            return $(this).attr('aria-disabled') !== 'true' && !$(this).hasClass('disabled');
          });
          var idx = $opts.index(this);
          if (idx < 0) return;
          var dir = (key === 'ArrowRight' || key === 'ArrowDown') ? 1 : -1;
          var next = (idx + dir + $opts.length) % $opts.length;
          var $next = $opts.eq(next);
          onOptionActivate($next);
          $next.focus();
        }
      });
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
    updateAvailability();
    updateArchitectureVisibility();
    writeURL();
    $('.installation-instructions').hide();
    render();
    updateHeadings();
    updateFoldouts(false);
    wire();

    // Auto-detect architecture if not set via URL or user choice
    if (!state.architecture && !urlFlags.archFromURL && state.platform !== 'macos') {
      detectArchitecture().then(function (arch) {
        if (arch && !state.architecture) {
          state.architecture = arch;
          applyUIFromState();
          updateAvailability();
          writeURL();
          render();
          updateHeadings();
          updateFoldouts(true);
        } else if (!arch) {
          updateFoldouts(true);
        }
      });
    }
  });
})(jQuery);
