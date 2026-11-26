(function () {

	var OPEN_DELAY = 80;
	var CLOSE_DELAY = 200;
	var desktop = window.matchMedia('(min-width: 901px)');

	document.querySelectorAll('nav.megamenu').forEach(function (nav) {
		var items = Array.prototype.slice.call(nav.querySelectorAll('.mm-item.has-panel'));
		if (!items.length) return;

		var viewport = document.createElement('div');
		viewport.className = 'mm-viewport';
		var box = document.createElement('div');
		box.className = 'mm-viewport-box';
		viewport.appendChild(box);

		var entries = items.map(function (item) {
			return {
				item: item,
				trigger: item.querySelector('.mm-trigger'),
				panel: item.querySelector('.mm-panel')
			};
		});

		var current = null;
		var openTimer = null;
		var closeTimer = null;
		var hideTimer = null;
		var hoverOpenedAt = 0;

		function clearTimers() {
			clearTimeout(openTimer);
			clearTimeout(closeTimer);
		}

		function links(entry) {
			return Array.prototype.slice.call(entry.panel.querySelectorAll('a'));
		}

		function open(entry) {
			if (current === entry) return;
			var first = !current;
			clearTimeout(hideTimer);
			entries.forEach(function (other) {
				if (other === entry) return;
				other.panel.classList.remove('is-active');
				other.trigger.setAttribute('aria-expanded', 'false');
			});
			current = entry;
			entry.panel.classList.add('is-active');
			entry.trigger.setAttribute('aria-expanded', 'true');

			var height = entry.panel.offsetHeight + 'px';
			if (first) {
				box.classList.add('no-transition');
				box.style.height = height;
				box.offsetHeight;
				box.classList.remove('no-transition');
				viewport.classList.add('is-open');
			} else {
				box.style.height = height;
			}
		}

		function close() {
			clearTimers();
			if (!current) return;
			var panel = current.panel;
			current.trigger.setAttribute('aria-expanded', 'false');
			current = null;
			viewport.classList.remove('is-open');
			hideTimer = setTimeout(function () {
				panel.classList.remove('is-active');
			}, 150);
		}

		function scheduleClose() {
			clearTimeout(openTimer);
			clearTimeout(closeTimer);
			closeTimer = setTimeout(close, CLOSE_DELAY);
		}

		function mount() {
			entries.forEach(function (entry) {
				box.appendChild(entry.panel);
			});
			nav.appendChild(viewport);
			nav.classList.add('mm-js');
		}

		function unmount() {
			close();
			clearTimeout(hideTimer);
			entries.forEach(function (entry) {
				entry.panel.classList.remove('is-active');
				entry.item.appendChild(entry.panel);
			});
			if (viewport.parentNode) viewport.parentNode.removeChild(viewport);
			nav.classList.remove('mm-js');
		}

		entries.forEach(function (entry) {
			entry.item.addEventListener('pointerenter', function (e) {
				if (!desktop.matches || e.pointerType !== 'mouse') return;
				clearTimers();
				if (current) {
					open(entry);
				} else {
					openTimer = setTimeout(function () {
						hoverOpenedAt = Date.now();
						open(entry);
					}, OPEN_DELAY);
				}
			});

			entry.item.addEventListener('pointerleave', function (e) {
				if (!desktop.matches || e.pointerType !== 'mouse') return;
				scheduleClose();
			});

			entry.trigger.addEventListener('click', function () {
				if (!desktop.matches) return;
				clearTimers();
				if (current === entry) {
					if (Date.now() - hoverOpenedAt > 400) close();
				} else {
					open(entry);
				}
			});

			entry.trigger.addEventListener('keydown', function (e) {
				if (!desktop.matches || e.key !== 'ArrowDown') return;
				e.preventDefault();
				clearTimers();
				open(entry);
				var first = links(entry)[0];
				if (first) first.focus();
			});

			entry.panel.addEventListener('keydown', function (e) {
				if (e.key !== 'Tab') return;
				var list = links(entry);
				if (e.shiftKey && document.activeElement === list[0]) {
					e.preventDefault();
					entry.trigger.focus();
				} else if (!e.shiftKey && document.activeElement === list[list.length - 1]) {
					e.preventDefault();
					close();
					var next = entry.item.nextElementSibling;
					var target = next && next.querySelector('.mm-trigger');
					if (target) target.focus();
				}
			});
		});

		nav.querySelectorAll('.mm-item:not(.has-panel)').forEach(function (item) {
			item.addEventListener('pointerenter', function (e) {
				if (current && e.pointerType === 'mouse') scheduleClose();
			});
		});

		viewport.addEventListener('pointerenter', function (e) {
			if (e.pointerType === 'mouse') clearTimers();
		});

		viewport.addEventListener('pointerleave', function (e) {
			if (e.pointerType === 'mouse') scheduleClose();
		});

		nav.addEventListener('keydown', function (e) {
			if (e.key !== 'Escape' || !current) return;
			var trigger = current.trigger;
			close();
			trigger.focus();
		});

		nav.addEventListener('focusout', function (e) {
			if (current && e.relatedTarget && !nav.contains(e.relatedTarget)) close();
		});

		document.addEventListener('pointerdown', function (e) {
			if (current && !nav.contains(e.target)) close();
		});

		function sync() {
			if (desktop.matches) mount(); else unmount();
		}

		desktop.addEventListener('change', sync);
		sync();
	});

})();
