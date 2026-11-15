(function () {
  'use strict';

  window.updateStatusIndicator = function(statusText) {
    var statusElement = document.getElementById("last_query_status");
    if (!statusElement) return;

    if (statusText.includes("Idle")) {
      statusElement.setAttribute('data-status', 'idle');
    } else if (statusText.includes("Error")) {
      statusElement.setAttribute('data-status', 'error');
    } else {
      statusElement.setAttribute('data-status', 'executing');
    }
  };

  if (!document.body.classList.contains('wasm')) return;

  var container = document.querySelector('.content-container');
  if (!container) return;
  var foldouts = container.querySelectorAll('.selection-foldout');

  function contentOf(foldout) {
    return foldout.querySelector(':scope > .selection-content');
  }

  function openFoldout(foldout) {
    var content = contentOf(foldout);
    if (content) window.Helpers.slideDown(content, 150);
    foldout.classList.add('open');
  }

  function closeFoldout(foldout) {
    var content = contentOf(foldout);
    if (content) {
      content.style.display = 'block';
      window.Helpers.slideUp(content, 150);
    }
    foldout.classList.remove('open');
  }

  container.addEventListener('click', function (e) {
    var head = e.target.closest('.selection-head');
    if (head && container.contains(head)) {
      e.stopPropagation();
      var fold = head.closest('.selection-foldout');
      if (!fold || fold.classList.contains('disabled')) return;
      if (fold.classList.contains('open')) closeFoldout(fold); else openFoldout(fold);
      return;
    }
    var content = e.target.closest('.selection-content');
    if (content && container.contains(content)) {
      e.stopPropagation();
      return;
    }
    var foldout = e.target.closest('.selection-foldout');
    if (foldout && container.contains(foldout) && !foldout.classList.contains('disabled') && !foldout.classList.contains('open')) {
      openFoldout(foldout);
    }
  });

  foldouts.forEach(function (fold) {
    var content = contentOf(fold);
    if (content) content.style.display = fold.classList.contains('open') ? '' : 'none';
  });

  function clearSelectedSpan(foldout) {
    if (foldout.dataset.foldout !== 'credentials') return;
    var selected = foldout.querySelector('.selection-head .selected');
    if (selected) selected.textContent = '';
  }

  ['input', 'change'].forEach(function (type) {
    container.addEventListener(type, function (e) {
      if (!e.target.matches('.selection-foldout[data-foldout="credentials"] input[type="text"]')) return;
      clearSelectedSpan(e.target.closest('.selection-foldout'));
    });
  });

  foldouts.forEach(clearSelectedSpan);
})();
