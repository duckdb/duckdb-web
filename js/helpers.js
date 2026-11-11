(function () {
	const running = new WeakMap();
	const savedDisplay = new WeakMap();
	const boxProps = ['height', 'paddingTop', 'paddingBottom', 'marginTop', 'marginBottom'];

	function prefersReducedMotion() {
		return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
	}

	function isVisible(el) {
		return Boolean(el) && el.getClientRects().length > 0;
	}

	function readBox(el) {
		const style = getComputedStyle(el);
		const box = {};
		boxProps.forEach(function (prop) {
			box[prop] = style[prop];
		});
		return box;
	}

	function collapsedBox() {
		const box = {};
		boxProps.forEach(function (prop) {
			box[prop] = '0px';
		});
		return box;
	}

	function stop(el) {
		const current = running.get(el);
		if (!current) {
			return null;
		}
		const from = current.type === 'fade' ? { opacity: getComputedStyle(el).opacity } : readBox(el);
		current.animation.cancel();
		running.delete(el);
		if (current.type === 'slide') {
			el.style.overflow = '';
		}
		return { direction: current.direction, from: from };
	}

	const defaultDisplays = {};

	function defaultDisplay(el) {
		const tag = el.nodeName;
		if (!defaultDisplays[tag]) {
			const probe = document.createElement(tag);
			document.body.appendChild(probe);
			const display = getComputedStyle(probe).display;
			probe.remove();
			defaultDisplays[tag] = display === 'none' ? 'block' : display;
		}
		return defaultDisplays[tag];
	}

	function reveal(el) {
		el.style.display = '';
		if (getComputedStyle(el).display === 'none') {
			el.style.display = savedDisplay.get(el) || defaultDisplay(el);
		}
	}

	function conceal(el) {
		const display = getComputedStyle(el).display;
		if (display !== 'none') {
			savedDisplay.set(el, display);
		}
		el.style.display = 'none';
	}

	function animate(el, keyframes, duration, type, direction, done) {
		if (prefersReducedMotion() || !duration) {
			done();
			return Promise.resolve();
		}
		const animation = el.animate(keyframes, { duration: duration, easing: 'ease-in-out', fill: 'forwards' });
		running.set(el, { animation: animation, type: type, direction: direction });
		return animation.finished.then(function () {
			running.delete(el);
			done();
			animation.cancel();
		}, function () {});
	}

	function slideDown(el, duration) {
		if (duration === undefined) duration = 400;
		const stopped = stop(el);
		const wasHidden = !isVisible(el);
		if (!wasHidden && !stopped) {
			return Promise.resolve();
		}
		reveal(el);
		const to = readBox(el);
		const from = stopped && stopped.from.height !== undefined ? stopped.from : collapsedBox();
		el.style.overflow = 'hidden';
		return animate(el, [from, to], duration, 'slide', 'down', function () {
			el.style.overflow = '';
		});
	}

	function slideUp(el, duration) {
		if (duration === undefined) duration = 400;
		const stopped = stop(el);
		if (!isVisible(el)) {
			return Promise.resolve();
		}
		const from = stopped && stopped.from.height !== undefined ? stopped.from : readBox(el);
		el.style.overflow = 'hidden';
		return animate(el, [from, collapsedBox()], duration, 'slide', 'up', function () {
			el.style.overflow = '';
			conceal(el);
		});
	}

	function slideToggle(el, duration) {
		const current = running.get(el);
		const opening = current ? current.direction === 'up' : !isVisible(el);
		return opening ? slideDown(el, duration) : slideUp(el, duration);
	}

	function fadeIn(el, duration) {
		if (duration === undefined) duration = 400;
		const stopped = stop(el);
		if (isVisible(el) && !stopped) {
			return Promise.resolve();
		}
		reveal(el);
		const from = stopped && stopped.from.opacity !== undefined ? stopped.from.opacity : 0;
		return animate(el, [{ opacity: from }, { opacity: getComputedStyle(el).opacity }], duration, 'fade', 'in', function () {});
	}

	function positionLeft(el) {
		const style = getComputedStyle(el);
		const marginLeft = parseFloat(style.marginLeft) || 0;
		if (style.position === 'fixed') {
			return el.getBoundingClientRect().left - marginLeft;
		}
		const pageLeft = function (node) {
			return node.getClientRects().length ? node.getBoundingClientRect().left + window.scrollX : 0;
		};
		let parent = el.offsetParent || document.documentElement;
		while (parent && (parent === document.body || parent === document.documentElement) && getComputedStyle(parent).position === 'static') {
			parent = parent.parentNode;
		}
		let parentLeft = 0;
		if (parent && parent !== el && parent.nodeType === 1) {
			parentLeft = pageLeft(parent) + (parseFloat(getComputedStyle(parent).borderLeftWidth) || 0);
		}
		return pageLeft(el) - parentLeft - marginLeft;
	}

	function hashTarget(hash) {
		const id = decodeURIComponent((hash || '').replace(/^#/, ''));
		if (!id) {
			return null;
		}
		return document.getElementById(id) || document.getElementsByName(id)[0] || null;
	}

	function scrollToTarget(el) {
		if (!el) {
			return;
		}
		const stickyVideo = document.querySelector('.video-container.sticky');
		const stickyOffset = stickyVideo ? stickyVideo.offsetHeight + 20 : 0;
		const bannerOffset = typeof window.docBannerHeight === 'function' ? window.docBannerHeight() : 0;
		const top = el.getBoundingClientRect().top + window.scrollY - 90 - stickyOffset - bannerOffset;
		window.scrollTo({ top: top, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
	}

	window.Helpers = {
		isVisible: isVisible,
		stop: function (el) { stop(el); },
		show: reveal,
		hide: conceal,
		slideDown: slideDown,
		slideUp: slideUp,
		slideToggle: slideToggle,
		fadeIn: fadeIn,
		positionLeft: positionLeft,
		hashTarget: hashTarget,
		scrollToTarget: scrollToTarget
	};
})();
