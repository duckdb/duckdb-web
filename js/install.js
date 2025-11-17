(function ($) {
  'use strict';

  $(function () {
    // Run only on installation page
    if (!$('body').hasClass('installation')) return;

    var $container = $('.installationselection');
    var $result = $('#result');
    var $templates = $('.instruction-collection');
    var $inst = $('.installation-instructions');
    var $wrap = $result.children('.instruction-wrap');
    var $more = $result.children('.more');
    var $docsLink = $more.find('.docs-link');
    var $altToggle = $more.find('.alternative-options');
    var $foldPlat = $container.find('.selection-foldout[data-foldout="platform"]');
    var $foldEnv = $container.find('.selection-foldout[data-foldout="environment"]');
    var $rgPlat = $container.find('.selection-options[data-role="platform"]');
    var $rgEnv = $container.find('.selection-options[data-role="environment"]');

    var state = {
      platform: null,
      environment: null
    };

    function detectPlatform() {
      if (window.UAParser) {
        try {
          var result = new UAParser().getResult();
          var osName = (result && result.os && result.os.name) ? String(result.os.name).toLowerCase() : '';
          if (osName) {
            if (/mac\s?os|macos|os\s?x/.test(osName)) return 'macos';
            if (/windows/.test(osName)) return 'windows';
            if (/linux|ubuntu|debian|fedora|arch|gentoo|suse|centos/.test(osName)) return 'linux';
          }
        } catch (e) {}
      }

      var fallback = (navigator.platform || '') + ' ' + (navigator.userAgent || '');
      if (/Mac/i.test(fallback)) return 'macos';
      if (/Win/i.test(fallback)) return 'windows';
      if (/Linux|X11/i.test(fallback)) return 'linux';
      return 'macos';
    }

    function readURL() {
      try {
        var params = new URLSearchParams(window.location.search);
        state.platform = sanitizeParam(params.get('platform'));
        state.environment = sanitizeParam(params.get('environment'));
      } catch (e) {}
    }

    function writeURL() {
      try {
        var params = new URLSearchParams(window.location.search);
        setOrDelete(params, 'platform', state.platform);
        setOrDelete(params, 'environment', state.environment);
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
        environment: 'cli'
      };
    }

    function normalizeState() {
      var def = defaultState();

      var $activePlatform = $container.find('.selection-options[data-role="platform"] .option.active').first();
      state.platform = state.platform || ($activePlatform.data('value') || null) || def.platform;

      var $activeEnv = $container.find('.selection-options[data-role="environment"] .option.active').first();
      state.environment = state.environment || ($activeEnv.data('value') || null) || def.environment;
    }

    function selectOption(role, value) {
      if (!role) return;
      var $group;
      if (role === 'platform') $group = $rgPlat;
      else if (role === 'environment') $group = $rgEnv;
      else $group = $();
      if (!$group || !$group.length) return;

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

    function applyUIFromState() {
      selectOption('platform', state.platform);
      selectOption('environment', state.environment);
    }

    function labelFor(role) {
      var $group = role === 'platform' ? $rgPlat : role === 'environment' ? $rgEnv : $();
      if (!$group || !$group.length) return '';
      var $opt = $group.find('.option.active').first();
      var displayLabel = $opt.attr('data-display-label');
      if (displayLabel) return $.trim(displayLabel);
      var txt = $.trim(($opt.find('.label').text() || $opt.text() || ''));
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
      var needsPlatform = environmentRequiresPlatform(state.environment);
      if (!needsPlatform) {
        platLabel = '';
      }
      var text = platLabel ? ' ' + platLabel : '';
      $foldPlat.find('.selection-head .selected').text(text);

      var $live = $container.find('.live-region');
      if (!$live.length) {
        $live = $('<div class="visually-hidden live-region" aria-live="polite"></div>').appendTo($container);
      }
      var liveText = [];
      if (envLabel) liveText.push(envLabel);
      if (platLabel) liveText.push(platLabel);
      $live.text(liveText.join(', '));
    }

    function updateVersionLabel() {
      if (!$inst || !$inst.length) return;
      var core = String($inst.attr('data-core-version') || '').trim();
      var jv = String($inst.attr('data-java-version') || '').trim();
      var ov = String($inst.attr('data-odbc-version') || '').trim();
      var gv = String($inst.attr('data-go-version') || '').trim();
      var rv = String($inst.attr('data-r-version') || '').trim();
      var rustv = String($inst.attr('data-rust-version') || '').trim();
      var env = state.environment || '';
      var ver = core;
      if (env === 'java' && jv) ver = jv;
      else if (env === 'odbc' && ov) ver = ov;
      else if (env === 'go' && gv) ver = gv;
      else if (env === 'r' && rv) ver = rv;
      else if (env === 'rust' && rustv) ver = rustv;
      var $cv = $inst.find('.currentversion');
      if ($cv.length) {
        if (ver) $cv.text('v' + ver);
        else $cv.text('');
      }
    }

    function updateFoldouts(animate) {
      var needsPlatform = environmentRequiresPlatform(state.environment);

      if (!needsPlatform) {
        setFoldoutOpen($foldPlat, false, !!animate);
        $foldPlat.addClass('disabled').attr('aria-disabled', 'true');
        $rgPlat.attr('aria-disabled', 'true');
        $rgPlat.find('.option')
          .attr('aria-disabled', 'true')
          .attr('tabindex', '-1');
        return;
      }

      $foldPlat.removeClass('disabled').removeAttr('aria-disabled');
      $rgPlat.removeAttr('aria-disabled');
      var $platOptions = $rgPlat.find('.option');
      $platOptions.attr('aria-disabled', 'false');
      var $activePlat = $platOptions.filter('.active').first();
      if ($activePlat.length) {
        $platOptions.not($activePlat).attr('tabindex', '-1');
        $activePlat.attr('tabindex', '0');
      } else {
        $platOptions.attr('tabindex', '-1');
        $platOptions.first().attr('tabindex', '0');
      }

      var shouldClosePlat = !!state.platform;
      setFoldoutOpen($foldPlat, !shouldClosePlat, !!animate);
    }

    function bestTemplate() {
      var p = state.platform;
      var e = state.environment;

      if (!p || !e) return $();

      // Try platform + environment match
      var sel = '[data-platform="' + cssEscape(p) + '"][data-environment="' + cssEscape(e) + '"]';
      var $match = $templates.find(sel).first();
      if ($match.length) return $match;

      // Fallback: environment-only (e.g., Python, Node.js)
      var selEnvOnly = '[data-environment="' + cssEscape(e) + '"]:not([data-platform])';
      return $templates.find(selEnvOnly).first();
    }

    function environmentRequiresPlatform(environment) {
      if (!environment) return false;
      var selEnvOnly = '[data-environment="' + cssEscape(environment) + '"]:not([data-platform])';
      if ($templates.find(selEnvOnly).length) return false;
      var selWithPlatform = '[data-environment="' + cssEscape(environment) + '"][data-platform]';
      return $templates.find(selWithPlatform).length > 0;
    }

    function render() {
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

    function onOptionActivate($opt) {
      if ($opt.attr('aria-disabled') === 'true' || $opt.hasClass('disabled')) return;

      var $group = $opt.closest('.selection-options');
      var role = String($group.data('role') || '');
      var value = String($opt.data('value') || '');

      if (!role || !value) return;

      selectOption(role, value);

      writeURL();
      render();
      updateHeadings();
      updateVersionLabel();
      updateFoldouts(true);
    }

    function wire() {
      $container.find('.selection-options[data-role]').attr('role', 'radiogroup');
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
        if ($fold.hasClass('disabled')) return;
        if (!$fold.hasClass('open')) {
          var $content = $fold.children('.selection-content');
          $content.stop(true, true).slideDown(150);
          $fold.addClass('open');
        }
      });

      $container.on('click', '.selection-head', function (e) {
        e.stopPropagation();
        var $fold = $(this).closest('.selection-foldout');
        if ($fold.hasClass('disabled')) return;
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

      $container.find('.selection-options[data-role]').each(function () {
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
    writeURL();
    $('.installation-instructions').hide();
    render();
    updateHeadings();
    updateVersionLabel();
    updateFoldouts(false);
    wire();
  });
})(jQuery);
