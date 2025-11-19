(function ($) {
  'use strict';

  $(function () {
    // Run only on wasm page
    if (!$('body').hasClass('wasm')) return;

    var $container = $('.content-container');
    var $foldouts = $container.find('.selection-foldout');

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

    function wire() {
      // Click handler for foldout content (prevent propagation)
      $container.on('click', '.selection-content', function (e) {
        e.stopPropagation();
      });

      // Click handler for entire foldout (opens it)
      $container.on('click', '.selection-foldout', function () {
        var $fold = $(this);
        if ($fold.hasClass('disabled')) return;
        if (!$fold.hasClass('open')) {
          var $content = $fold.children('.selection-content');
          $content.stop(true, true).slideDown(150);
          $fold.addClass('open');
        }
      });

      // Click handler for selection-head (toggles open/close)
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

      // Initialize foldouts based on their initial state
      $foldouts.each(function () {
        var $fold = $(this);
        var isOpen = $fold.hasClass('open');
        var $content = $fold.children('.selection-content');
        if (isOpen) $content.show(); else $content.hide();
      });
    }

    // Update selected span based on form inputs (only for credentials foldout)
    function updateSelectedSpan($foldout) {
      // Only update if this is the credentials foldout
      if ($foldout.data('foldout') !== 'credentials') return;
      
      var $selected = $foldout.find('.selection-head .selected');
      var $form = $foldout.find('form');
      var values = [];
      
      $form.find('input[type="text"]').each(function() {
        var $input = $(this);
        var value = $input.val().trim();
        if (value) {
          var label = $input.prev('label').text().replace(':', '').trim();
          values.push(label + ': ' + value);
        }
      });
      
      if (values.length > 0) {
        $selected.text(values.join(', '));
      } else {
        $selected.text('None');
      }
    }

    // Watch for input changes (only for credentials foldout)
    $container.on('input change', '.selection-foldout[data-foldout="credentials"] input[type="text"]', function() {
      var $foldout = $(this).closest('.selection-foldout');
      updateSelectedSpan($foldout);
    });

    // Initialize selected spans (only for credentials foldout)
    $foldouts.filter('[data-foldout="credentials"]').each(function() {
      updateSelectedSpan($(this));
    });

    // Initialize
    wire();
  });
})(jQuery);
