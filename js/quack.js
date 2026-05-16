// Page-specific behavior for the Quack landing page.
// Loaded conditionally via _layouts/default.html when body_class contains "quack".

// Install-Try Quack today: pill-tabs with sliding highlight + tab content swap.
(function() {
	var topbar = document.querySelector('.quack-install .install-topbar');
	if (!topbar) return;
	var lis = topbar.querySelectorAll('li');
	var highlight = topbar.querySelector('.select-highlight');
	var panes = document.querySelectorAll('.quack-install .install-steps');

	function moveHighlight(li) {
		highlight.style.left = li.offsetLeft + 'px';
		highlight.style.width = li.offsetWidth + 'px';
	}

	function activate(li) {
		var target = li.getAttribute('data-target');
		lis.forEach(function(x) { x.classList.toggle('active', x === li); });
		panes.forEach(function(p) {
			p.classList.toggle('hidden', p.getAttribute('data-tab') !== target);
		});
		moveHighlight(li);
	}

	lis.forEach(function(li) {
		li.addEventListener('click', function() { activate(li); });
	});

	var initial = topbar.querySelector('li.active') || lis[0];
	if (initial) {
		requestAnimationFrame(function() { moveHighlight(initial); });
		window.addEventListener('resize', function() {
			var current = topbar.querySelector('li.active') || lis[0];
			if (current) moveHighlight(current);
		});
	}
})();

// Introducing Quack: click thumbnail → swap in YouTube iframe with autoplay.
(function() {
	document.querySelectorAll('.quack-introducing .video-thumbnail').forEach(function(thumb) {
		thumb.addEventListener('click', function() {
			var container = thumb.parentElement.querySelector('.video-container');
			if (!container) return;
			var iframe = container.querySelector('iframe');
			if (iframe) {
				var baseSrc = iframe.getAttribute('data-src') || '';
				if (baseSrc) iframe.setAttribute('src', baseSrc + '?autoplay=1');
			}
			container.style.display = '';
			thumb.style.display = 'none';
		});
	});
})();

// Architecture storage tabs: swap DuckDB / DuckLake panel and sync server catalog name.
(function() {
	var tabs = document.querySelectorAll('.quack-architecture .storage-tabs .tab');
	var panels = document.querySelectorAll('.quack-architecture .storage-panel');
	var catalogSpan = document.querySelector('.server-catalog-name');

	function syncCatalog(target) {
		if (!catalogSpan) return;
		panels.forEach(function(p) {
			if (p.getAttribute('data-storage') === target) {
				catalogSpan.textContent = p.getAttribute('data-catalog') || '';
			}
		});
	}

	tabs.forEach(function(btn) {
		btn.addEventListener('click', function() {
			var target = btn.getAttribute('data-target');
			tabs.forEach(function(t) { t.classList.toggle('active', t === btn); });
			panels.forEach(function(p) {
				p.classList.toggle('hidden', p.getAttribute('data-storage') !== target);
			});
			syncCatalog(target);
		});
	});
})();
