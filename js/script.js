function docBannerHeight() {
	var banner = document.querySelector('.banner.docversion');
	return banner ? banner.offsetHeight : 0;
}

// Detect OS (using UAParser), also used by install.js
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

$(document).ready(function(){
	var initialHashTarget = Helpers.hashTarget(window.location.hash);
	if (initialHashTarget) {
		Helpers.scrollToTarget(initialHashTarget);
		var hashParent = initialHashTarget.parentElement;
		if (document.body.classList.contains('faq') && hashParent && hashParent.classList.contains('qa-wrap')) {
			hashParent.classList.add('open');
			hashParent.querySelectorAll('.answer').forEach(function (answer) {
				Helpers.slideDown(answer, 150);
			});
		}
	}
	
	
	
	/** DARK MODE SWITCH */
	var isDark = document.documentElement.classList.contains('darkmode');
	var modeButtons = document.querySelectorAll('.mode');
	modeButtons.forEach(function (button) {
		button.setAttribute('data-mode', isDark ? 'light' : 'dark');
	});

	setTimeout(() => {
		document.documentElement.classList.remove('disable-transitions');
	}, 300);
	
	modeButtons.forEach(function (button) {
		button.addEventListener('click', onModeClick);
	});

	function onModeClick() {
		var isDark = this.getAttribute('data-mode') === 'dark';
		document.documentElement.classList.toggle('darkmode', isDark);
		this.setAttribute('data-mode', isDark ? 'light' : 'dark');
		localStorage.setItem('mode', isDark ? 'dark' : 'light');
		if (isDark) {
			document.documentElement.style.backgroundColor = '#0d0d0d';
			document.documentElement.style.colorScheme = 'dark';
		} else {
			document.documentElement.style.backgroundColor = '';
			document.documentElement.style.colorScheme = '';
		}
		document.documentElement.classList.add('disable-transitions');
		setTimeout(() => {
			document.documentElement.classList.remove('disable-transitions');
		}, 300);
	}

	

	var OSdatid = detectPlatform();
	var OSName = OSdatid === 'macos' ? 'macOS' : OSdatid === 'windows' ? 'Windows' : OSdatid === 'linux' ? 'Linux' : 'Unknown OS';
	document.querySelectorAll('.systemdetected').forEach(function (el) {
		el.textContent = 'System detected: ' + OSName;
	});
	
	
	
	
	/** FILTER LINE  */
	var filterbars = document.querySelectorAll('.filterbar');
	if (filterbars.length && typeof Isotope !== 'undefined') {

		/* CUSTOM FITROWS FUNCTION FOR ISOTOPE TO GET EQUAL HEIGHT TILES */
		!function(t){"use strict";function i(t){var i=t.create("fitRows");return i.prototype._resetLayout=function(){if(this.x=0,this.y=0,this.maxY=0,this.row=0,this.rows=[],this._getMeasurement("gutter","outerWidth"),this.options.equalheight)for(var t=0;t<this.isotope.items.length;t++)this.isotope.items[t].css({height:"auto"})},i.prototype._getItemLayoutPosition=function(t){t.getSize();var i=this.gutter||0,s=t.size.outerWidth,o=Math.ceil(this.isotope.size.innerWidth+i);0!==this.x&&s+this.x+i>o&&(this.x=0,this.y=this.maxY+i),0===this.x&&0!==this.y&&this.row++;var e={x:this.x,y:this.y};return this.maxY=Math.max(this.maxY,this.y+t.size.outerHeight),this.x+=s+i,void 0===this.rows[this.row]?(this.rows[this.row]=[],this.rows[this.row].start=this.y,this.rows[this.row].end=this.maxY):this.rows[this.row].end=Math.max(this.rows[this.row].end,this.maxY),t.row=this.row,e},i.prototype._equalHeight=function(){for(var t=0;t<this.isotope.items.length;t++){var i=this.isotope.items[t].row,s=this.rows[i];if(s){var o=s.end-s.start;o-=this.isotope.items[t].size.borderTopWidth+this.isotope.items[t].size.borderBottomWidth,o-=this.isotope.items[t].size.marginTop+this.isotope.items[t].size.marginBottom,o-=this.gutter.height||0,!1==this.isotope.items[t].size.isBorderBox&&(o-=this.isotope.items[t].size.paddingTop+this.isotope.items[t].size.paddingBottom),this.isotope.items[t].size.height=o,this.isotope.items[t].css({height:o.toString()+"px"})}}},i.prototype._getContainerSize=function(){return this.options.equalheight&&this._equalHeight(),{height:this.maxY}},i}"function"==typeof define&&define.amd?define(["../layout-mode"],i):"object"==typeof exports?module.exports=i(require("../layout-mode")):i(t.Isotope.LayoutMode)}(window);

		var grids = Array.prototype.map.call(document.querySelectorAll('.newstiles'), function (el) {
			return new Isotope(el, {
				itemSelector: '.postpreview',
				layoutMode: 'fitRows',
				isJQueryFiltering: false,
				fitRows: {
					gutter: document.querySelector('.guides-list') ? 16 : 32,
					equalheight: true
				}
			});
		});

		var heading = document.querySelector('.pagetitle h1');
		var defaultHeading = heading ? heading.textContent.trim() : '';
		var search = document.getElementById('search-input');
		var topicFilter = document.getElementById('topic-filter');
		var coreToggle = document.getElementById('core-toggle');
		var emptyMessages = document.querySelectorAll('.filter-empty');
		var activeFilter = '*';

		function filterButtons(scope) {
			return Array.prototype.slice.call(scope.querySelectorAll('[data-filter]'));
		}

		function updateFilterHighlight(button) {
			if (!button) return;
			var tags = button.closest('.filtertags');
			var highlight = tags && tags.querySelector('.filter-highlight');
			if (!highlight || !Helpers.isVisible(button)) return;
			highlight.style.left = Helpers.positionLeft(button) + 'px';
			highlight.style.width = button.getBoundingClientRect().width + 'px';
		}

		function setActiveFilter(value) {
			activeFilter = value;
			if (topicFilter) {
				var topics = filterButtons(topicFilter);
				var matches = topics.filter(function (topic) { return topic.getAttribute('data-filter') === value; });
				topics.forEach(function (topic) {
					topic.removeAttribute('aria-current');
					if (topic.parentElement) topic.parentElement.classList.remove('current');
				});
				matches.forEach(function (topic) {
					topic.setAttribute('aria-current', 'true');
					if (topic.parentElement) topic.parentElement.classList.add('current');
				});
				var label = matches.map(function (topic) { return topic.textContent; }).join('');
				topicFilter.querySelectorAll('.selectedversion').forEach(function (el) { el.textContent = label; });
				topicFilter.querySelectorAll('.versiontrigger').forEach(function (el) { el.setAttribute('aria-label', 'Filter guides by topic: ' + label); });
			}
			document.querySelectorAll('.filterbar .filtertags').forEach(function (tags) {
				var match = null;
				tags.querySelectorAll('.filter-btn').forEach(function (button) {
					button.classList.remove('active');
					if (button.getAttribute('data-filter') === value) {
						button.classList.add('active');
						match = match || button;
					}
				});
				updateFilterHighlight(match);
			});
			if (heading) {
				var active = document.querySelector('.filterbar .filter-btn.active');
				heading.textContent = (active && active.getAttribute('data-heading')) || defaultHeading;
			}
		}

		function readFiltersFromURL() {
			var params = new URLSearchParams(window.location.search);
			var type = params.get('type');
			if (type && Array.prototype.some.call(document.querySelectorAll('.filterbar [data-filter]'), function (el) {
				return el.getAttribute('data-filter') === '.' + type;
			})) {
				setActiveFilter('.' + type);
			}
			if (params.get('q') && search) {
				search.value = params.get('q');
			}
			if (params.get('core') === '1' && coreToggle) {
				coreToggle.checked = true;
			}
		}

		function searchValue() {
			return search ? search.value : '';
		}

		function writeFiltersToURL() {
			var params = new URLSearchParams();
			if (activeFilter !== '*') {
				params.set('type', activeFilter.replace(/^\./, ''));
			}
			if (coreToggle && coreToggle.checked) {
				params.set('core', '1');
			}
			if (searchValue()) {
				params.set('q', searchValue());
			}
			history.replaceState(null, '', window.location.pathname + (params.toString() ? '?' + params.toString() : ''));
		}

		function applyFilters() {
			var query = searchValue().toLowerCase().trim();
			var coreOnly = Boolean(coreToggle && coreToggle.checked);

			grids.forEach(function (iso) {
				var section = iso.element.closest('.events-section');
				if (section) section.classList.remove('is-empty');
			});

			grids.forEach(function (iso) {
				iso.arrange({
					filter: function (item) {
						if (activeFilter !== '*' && !item.matches(activeFilter)) return false;
						if (coreOnly && item.getAttribute('data-core') !== 'true') return false;
						if (query && (item.getAttribute('data-search') || '').indexOf(query) === -1) return false;
						return true;
					}
				});
			});

			var visible = 0;
			grids.forEach(function (iso) {
				var count = iso.filteredItems.length;
				visible += count;
				var section = iso.element.closest('.events-section');
				if (section) section.classList.toggle('is-empty', count === 0);
			});
			emptyMessages.forEach(function (el) { el.hidden = visible > 0; });
		}

		filterbars.forEach(function (bar) {
			bar.addEventListener('click', function (e) {
				var option = e.target.closest('[data-filter]');
				if (!option || !bar.contains(option)) return;
				e.preventDefault();
				setActiveFilter(option.getAttribute('data-filter'));
				applyFilters();
				writeFiltersToURL();
				if (topicFilter && topicFilter.contains(option)) {
					topicFilter.classList.remove('active');
					topicFilter.querySelectorAll('.versiontrigger').forEach(function (trigger) {
						trigger.setAttribute('aria-expanded', 'false');
					});
					var trigger = topicFilter.querySelector('.versiontrigger');
					if (trigger) trigger.focus();
				}
			});
		});

		if (search) {
			search.addEventListener('input', function () {
				applyFilters();
				writeFiltersToURL();
			});
		}

		if (coreToggle) {
			coreToggle.addEventListener('change', function () {
				applyFilters();
				writeFiltersToURL();
			});
		}

		// --- Mobile filter modal ---
		var filterToggles = document.querySelectorAll('.filter-toggle');
		var filterModals = document.querySelectorAll('.filter-modal');
		var filterOverlays = document.querySelectorAll('.filter-overlay');

		function setFilterModal(open) {
			[filterToggles, filterModals, filterOverlays].forEach(function (list) {
				list.forEach(function (el) { el.classList.toggle('is-open', open); });
			});
			if (open) {
				filterModals.forEach(function (modal) {
					updateFilterHighlight(modal.querySelector('.filter-btn.active'));
				});
			}
		}

		filterToggles.forEach(function (toggle) {
			toggle.addEventListener('click', function () {
				var anyOpen = Array.prototype.some.call(filterModals, function (modal) { return modal.classList.contains('is-open'); });
				setFilterModal(!anyOpen);
			});
		});
		filterOverlays.forEach(function (overlay) {
			overlay.addEventListener('click', function () {
				setFilterModal(false);
			});
		});

		setActiveFilter(activeFilter);
		readFiltersFromURL();
		applyFilters();
	}
	

	
	// Same Page Anchor Scroll Navigation
	document.querySelectorAll('a[href*="#"]:not([href="#"]):not([href="#0"])').forEach(function (link) {
		link.addEventListener('click', function (event) {
			if (event.target.closest('svg.anchor-icon')) {
				return;
			}
			if (
				location.pathname.replace(/^\//, '') !== this.pathname.replace(/^\//, '') ||
				location.hostname !== this.hostname ||
				location.search !== this.search
			) {
				return;
			}
			var target = Helpers.hashTarget(this.hash);
			if (!target) {
				return;
			}
			event.preventDefault();
			if (location.hash !== this.hash) {
				history.pushState(null, '', this.hash);
			}
			Helpers.scrollToTarget(target);
		});
	});

    
    // FAQs
	document.querySelectorAll('.qa-wrap h3').forEach(function (heading) {
		heading.insertAdjacentHTML('beforeend', '<span class="faq-icon"><svg class="icon"><use href="#chevron-down"></use></svg></span>');
	});
	document.querySelectorAll('.qa-wrap').forEach(function (qaWrap) {
		qaWrap.addEventListener('click', function (event) {
			var answers = qaWrap.querySelectorAll('.answer');
			if (event.target.closest('h3')) {
				qaWrap.classList.toggle('open');
				answers.forEach(function (answer) {
					Helpers.slideToggle(answer, 150);
				});
			} else if (!qaWrap.classList.contains('open')) {
				qaWrap.classList.add('open');
				answers.forEach(function (answer) {
					Helpers.slideDown(answer, 150);
				});
			}
		});
	});
	document.querySelectorAll('.qa-wrap .answer a').forEach(function (link) {
		link.addEventListener('click', function (event) {
			event.stopPropagation();
		});
	});


	/* SIDENAVIGATION Documentation */
	const drillNav = document.querySelector('.sidenav-drill');
	const navRoot = drillNav ? Array.from(drillNav.children).find(function (el) { return el.classList.contains('sidenav'); }) : null;
	const navMotionKey = 'docs-sidebar-enter';

	function setDrill(item, open) {
		if (navRoot) navRoot.classList.add('nav-motion');
		item.classList.toggle('is-open', open);
		Array.from(item.children).forEach(function (child) {
			if (child.classList.contains('nav-drill')) child.setAttribute('aria-expanded', String(open));
		});
		if (item.parentElement && item.parentElement.classList.contains('nav-list')) {
			item.parentElement.classList.toggle('is-drilled', open);
		}
	}

	function enterDrill(item) {
		setDrill(item, true);
		drillNav.scrollTop = 0;
		Array.from(drillNav.children).forEach(function (child) {
			if (child.classList.contains('sidenav')) child.scrollTop = 0;
		});
		const backButton = item.querySelector(':scope > .nav-list > .nav-back > button');
		if (backButton) backButton.focus();
	}

	if (drillNav) {
		drillNav.addEventListener('click', function (e) {
			const sectionLink = e.target.closest('a.nav-row');
			if (sectionLink && drillNav.contains(sectionLink) && sectionLink.matches('.sidenav > .hasSub > a.nav-row')) {
				if ((navRoot && navRoot.classList.contains('is-drilled')) || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button !== 0) return;
				if (window.matchMedia('(max-width: 900px)').matches) {
					e.preventDefault();
					enterDrill(sectionLink.parentElement);
					return;
				}
				try { sessionStorage.setItem(navMotionKey, new URL(sectionLink.href).pathname); } catch (err) {}
				return;
			}

			const drillButton = e.target.closest('.nav-drill');
			if (drillButton && drillNav.contains(drillButton)) {
				enterDrill(drillButton.parentElement);
				return;
			}

			const backButton = e.target.closest('.nav-back button');
			if (backButton && drillNav.contains(backButton)) {
				const list = backButton.closest('.nav-list');
				const item = list && list.parentElement && list.parentElement.classList.contains('nav-item') ? list.parentElement : null;
				if (!item) return;
				setDrill(item, false);
				Array.from(item.children).forEach(function (child) {
					if (child.classList.contains('nav-row')) child.focus();
				});
				return;
			}

			const expandButton = e.target.closest('.nav-expand');
			if (expandButton && drillNav.contains(expandButton)) {
				const open = expandButton.getAttribute('aria-expanded') !== 'true';
				expandButton.setAttribute('aria-expanded', String(open));
				expandButton.parentElement.classList.toggle('is-open', open);
			}
		});
	}

	if (navRoot) {
		navRoot.addEventListener('animationend', function (e) {
			if (e.animationName !== 'docs-sidebar-enter') return;
			navRoot.classList.remove('nav-motion');
			document.documentElement.classList.remove('docs-sidebar-enter');
		});
	}

	const currentNavRow = document.querySelector('.sidenav-drill [aria-current="page"]');
	if (currentNavRow) {
		const navScroller = currentNavRow.closest('.sidenav-drill');
		const rowOffset = currentNavRow.getBoundingClientRect().top - navScroller.getBoundingClientRect().top;
		if (rowOffset > navScroller.clientHeight - 40) {
			navScroller.scrollTop = rowOffset - navScroller.clientHeight / 2;
		}
	}
	
	/* MOBILE MENU / SUBMENU */
	const hamburgers = document.querySelectorAll('.hamburger');
	const landingMenus = Array.from(document.querySelectorAll('.landingmenu nav'));
	const sideNavigations = document.querySelectorAll('.sidenavigation');
	const banners = Array.from(document.querySelectorAll('.banner')).filter(function (banner) {
		return !banner.classList.contains('docversion');
	});
	let bannersHiddenByMenu = [];

	if (hamburgers.length > 0) {
		hamburgers.forEach(function (hamburger) {
			hamburger.addEventListener('click', function () {
				this.classList.toggle('is-active');

				if (landingMenus.length > 0) { // Menu 1: Landingmenu
					landingMenus.forEach(function (nav) { nav.classList.toggle('slidein'); });
					document.querySelectorAll('body main').forEach(function (main) { main.classList.toggle('inactive'); });
				}

				if (sideNavigations.length > 0) { // Menu 2: Sidenavigation
					sideNavigations.forEach(function (nav) { nav.classList.toggle('slidein'); });
					document.querySelectorAll('body.documentation main .wrap').forEach(function (wrap) { wrap.classList.toggle('inactive'); });
				}

				// Banner hide/show mobile menu, restoring only banners the menu hid
				if (this.classList.contains('is-active')) {
					bannersHiddenByMenu = banners.filter(Helpers.isVisible);
					bannersHiddenByMenu.forEach(function (banner) {
						Helpers.slideUp(banner, 250);
					});
				} else {
					bannersHiddenByMenu.forEach(function (banner) {
						Helpers.slideDown(banner, 250);
					});
					bannersHiddenByMenu = [];
				}
			});
		});

		// Menu 1 Open Submenu
		landingMenus.forEach(function (nav) {
			nav.addEventListener('click', function (e) {
				if (window.innerWidth > 900) return;
				const item = e.target.closest('.hasSub');
				if (!item || !nav.contains(item)) return;
				e.preventDefault();
				const submenu = item.nextElementSibling && item.nextElementSibling.classList.contains('submenuwrap') ? item.nextElementSibling : null;
				if (item.classList.contains('open')) {
					item.classList.remove('open');
					if (submenu) Helpers.slideUp(submenu);
				} else {
					landingMenus.forEach(function (menu) {
						menu.querySelectorAll('.hasSub').forEach(function (el) { el.classList.remove('open'); });
						menu.querySelectorAll('.submenuwrap').forEach(function (el) { Helpers.slideUp(el); });
					});
					item.classList.add('open');
					if (submenu) Helpers.slideDown(submenu);
				}
			});
		});
	}

    
	// Appending Content-List of Overview-Pages
	function cleanNavClone(list) {
		list.querySelectorAll('.nav-back, svg').forEach(function (el) { el.remove(); });
		list.querySelectorAll('.nav-drill, .nav-expand').forEach(function (el) {
			const span = document.createElement('span');
			span.textContent = el.textContent;
			el.replaceWith(span);
		});
		list.classList.remove('is-drilled');
		list.querySelectorAll('.is-open, .is-drilled').forEach(function (el) { el.classList.remove('is-open', 'is-drilled'); });
		return list;
	}

	const currentNavLink = document.querySelector('.sidenav-drill [aria-current="page"]');
	const overviewIndex = document.querySelector('#main_content_wrap .index');
	if (window.location.href.includes("/overview") && currentNavLink && overviewIndex) {
		const overviewList = currentNavLink.closest('.nav-list').cloneNode(true);
		overviewList.classList.remove('sidenav');
		const currentInClone = overviewList.querySelector('[aria-current="page"]');
		if (currentInClone && currentInClone.parentElement) currentInClone.parentElement.remove();
		overviewIndex.appendChild(cleanNavClone(overviewList));
	}

	// Appending Content-List of Documentation
	const docuSitemap = document.getElementById('docusitemaphere');
	const sitemapSource = document.querySelector('.sidenav-drill ul.sidenav');
	if (docuSitemap && sitemapSource) {
		docuSitemap.appendChild(cleanNavClone(sitemapSource.cloneNode(true)));
	}
	
// Add class-name to external Links
function linksWithIcon(classes) {
	return Array.from(document.querySelectorAll(['#main_content_wrap', '.singleentry .content'].map(function (scope) {
		return classes.map(function (cls) { return scope + ' a.' + cls; }).join(', ');
	}).join(', ')));
}

function markLinks(test, addClass, removeClasses, exclude, githubTables, supporterBoard, onMatch) {
	document.querySelectorAll('a').forEach(function (a) {
		if (test(a)) {
			a.classList.add(addClass);
			removeClasses.forEach(function (cls) { a.classList.remove(cls); });
			if (onMatch) onMatch(a);
		}
	});
	document.querySelectorAll(exclude).forEach(function (a) { a.classList.remove(addClass); });
	if (githubTables) {
		document.querySelectorAll('table a.' + addClass).forEach(function (a) {
			if (a.textContent.includes('GitHub')) {
				a.classList.remove(addClass);
				a.classList.add('nobg');
			}
		});
	}
	if (supporterBoard) {
		document.querySelectorAll('.supporterboard a.' + addClass).forEach(function (a) {
			a.classList.remove(addClass);
			a.classList.add('nobg');
		});
	}
}

function hrefMatches(a, pattern) {
	var href = a.getAttribute('href');
	return Boolean(href) && pattern.test(href) && !a.querySelector('img') && !a.classList.contains('button');
}

markLinks(function (a) {
	return a.hostname && a.hostname !== location.hostname && !a.querySelector('img, svg') && !a.classList.contains('button');
}, 'externallink', [], '.headercontent a, .box-link a, .footercontent a, .highlight a, .button, .download-btn, .ecosystem-diagram a, a.tag, a:has(> .tag)', true, true, function (a) {
	a.setAttribute('target', '_blank');
});

// Add download icon to links pointing to downloadable files
markLinks(function (a) {
	return hrefMatches(a, /\.(pdf|zip|gz|tar|jar|csv|parquet|mp3)(\?.*)?$/i);
}, 'downloadlink', ['externallink'], '.headercontent a, .box-link a, .footercontent a, .highlight a, .button, .download-btn, .ecosystem-diagram a', true, true);

// Add play icon to links pointing to YouTube or Vimeo
markLinks(function (a) {
	return hrefMatches(a, /^(https?:)?\/\/(www\.|m\.)?(youtube\.com|youtu\.be|vimeo\.com)\//i);
}, 'videolink', ['externallink', 'downloadlink'], '.headercontent a, .box-link a, .footercontent a, .highlight a, .button, .ecosystem-diagram a', true, true);

// Add podcast icon to links pointing to Spotify or Apple Podcasts
markLinks(function (a) {
	return hrefMatches(a, /^(https?:)?\/\/(open\.spotify\.com|podcasts\.apple\.com)\//i);
}, 'podcastlink', ['externallink', 'downloadlink', 'videolink'], '.headercontent a, .box-link a, .footercontent a, .highlight a, .button, .ecosystem-diagram a', false, true);

// Glue the anchor icon to the last word of a heading so it never wraps alone
document.querySelectorAll(':is(h1, h2, h3, h4, h5, h6) svg.anchor-icon').forEach(function (svg) {
	var a = svg.parentElement;
	if (!a || a.tagName !== 'A' || a.querySelector('.anchor-wrap')) return;
	var contents = Array.from(a.childNodes);
	var last = null;
	for (var i = contents.length - 1; i >= 0; i--) {
		if (contents[i] === svg) continue;
		last = contents[i];
		break;
	}
	if (!last || last.nodeType !== 3) return;
	var match = last.nodeValue.match(/(\S+)(\s*)$/);
	if (!match) return;
	last.nodeValue = last.nodeValue.slice(0, match.index);
	var wrap = document.createElement('span');
	wrap.className = 'anchor-wrap';
	wrap.textContent = match[1];
	wrap.appendChild(svg);
	a.appendChild(wrap);
});

// Append sprite icons to external, download, video and podcast links, gluing the icon to the last word
linksWithIcon(['externallink', 'downloadlink', 'videolink', 'podcastlink']).forEach(function (a) {
	if (a.querySelector('svg.linkicon')) return;
	var icon = a.classList.contains('videolink') ? 'youtube' : (a.classList.contains('podcastlink') ? 'headphones-01' : (a.classList.contains('downloadlink') ? 'download-01' : 'link-external-02'));
	var svgMarkup = '<svg class="icon linkicon"><use href="#' + icon + '"></use></svg>';
	var last = a.lastChild;
	var match = (last && last.nodeType === 3) ? last.nodeValue.match(/(\S+)(\s*)$/) : null;
	if (match) {
		last.nodeValue = last.nodeValue.slice(0, match.index);
		var wrap = document.createElement('span');
		wrap.className = 'linkicon-wrap';
		wrap.textContent = match[1];
		wrap.insertAdjacentHTML('beforeend', svgMarkup);
		a.appendChild(wrap);
	} else {
		a.insertAdjacentHTML('beforeend', svgMarkup);
	}
});

// Copy the heading URL to the clipboard when the anchor-link icon is clicked
var anchorIconState = new WeakMap();
document.addEventListener('click', function (e) {
	var svg = e.target.closest('svg.anchor-icon');
	if (!svg) return;
	e.preventDefault();
	e.stopImmediatePropagation();
	var anchor = svg.closest('a');
	var url = anchor ? anchor.href : (location.origin + location.pathname + location.hash);
	if (navigator.clipboard && navigator.clipboard.writeText) {
		navigator.clipboard.writeText(url);
	}
	var use = svg.querySelector('use');
	var iconState = anchorIconState.get(svg) || { original: use ? use.getAttribute('href') : null, timer: null };
	anchorIconState.set(svg, iconState);
	if (use) use.setAttribute('href', '#check');
	svg.classList.add('copied');
	clearTimeout(iconState.timer);
	iconState.timer = setTimeout(function () {
		if (use) use.setAttribute('href', iconState.original);
		svg.classList.remove('copied');
	}, 1500);
});

// Glue trailing punctuation to the link icon with a word joiner so it never wraps alone
linksWithIcon(['externallink', 'downloadlink', 'videolink', 'podcastlink']).forEach(function (a) {
	var next = a.nextSibling;
	if (!next || next.nodeType !== 3) return;
	var match = next.nodeValue.match(/^\s*[.,;:)]/);
	if (!match) return;
	next.nodeValue = '\u2060' + next.nodeValue.slice(match[0].length - 1);
});

	// Documentation version and topic dropdowns share the same interaction.
	var docDropdowns = Array.from(document.querySelectorAll('.options .version, #topic-filter'));
	function setDropdownOpen(dropdown, open) {
		dropdown.classList.toggle('active', open);
		dropdown.querySelectorAll('.versiontrigger').forEach(function (trigger) {
			trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
		});
	}
	function closeVersionSelect() {
		var open = docDropdowns.filter(function (dropdown) { return dropdown.classList.contains('active'); });
		if (!open.length) return false;
		open.forEach(function (dropdown) { setDropdownOpen(dropdown, false); });
		return true;
	}

	docDropdowns.forEach(function (dropdown) {
		dropdown.querySelectorAll('.versiontrigger').forEach(function (trigger) {
			trigger.addEventListener('click', function () {
				var version = trigger.closest('.version');
				if (!version) return;
				var open = !version.classList.contains('active');
				closeVersionSelect();
				version.classList.toggle('active', open);
				trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
			});
		});

		dropdown.addEventListener('keydown', function (e) {
			if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
			e.preventDefault();
			var links = Array.from(dropdown.querySelectorAll('.versionsidebar a'));
			if (!links.length) return;
			var index = links.indexOf(document.activeElement);
			closeVersionSelect();
			setDropdownOpen(dropdown, true);
			index = e.key === 'ArrowDown' ? (index + 1) % links.length : (index <= 0 ? links.length - 1 : index - 1);
			links[index].focus();
		});

		dropdown.addEventListener('focusout', function (e) {
			if (!dropdown.contains(e.relatedTarget)) {
				setDropdownOpen(dropdown, false);
			}
		});
	});

	document.addEventListener('click', function (e) {
		if (e.target.closest('.options .version, #topic-filter')) return;
		closeVersionSelect();
	});

	document.addEventListener('keydown', function (e) {
		if (e.key !== 'Escape') return;
		var triggers = [];
		docDropdowns.forEach(function (dropdown) {
			if (dropdown.classList.contains('active')) triggers = triggers.concat(Array.from(dropdown.querySelectorAll('.versiontrigger')));
		});
		if (closeVersionSelect() && triggers[0]) {
			triggers[0].focus();
		}
	});

	// COPY PAGE AS MARKDOWN
	document.querySelectorAll('.headlinebar .copy-markdown').forEach(function (btn) {
		btn.addEventListener('click', function () {
			if (btn.classList.contains('copied')) return;

			var markdownPromise = fetch(btn.getAttribute('data-source')).then(function (response) {
				if (!response.ok) throw new Error('HTTP ' + response.status);
				return response.text();
			});

			function setLabel(icon, label) {
				btn.querySelectorAll('use').forEach(function (use) { use.setAttribute('href', icon); });
				btn.querySelectorAll('span').forEach(function (span) { span.textContent = label; });
			}

			function markCopied() {
				btn.classList.add('copied');
				setLabel('#check', 'Copied');
				setTimeout(function () {
					btn.classList.remove('copied');
					setLabel('#copy-01', 'Copy Markdown');
				}, 2000);
			}

			if (navigator.clipboard && window.ClipboardItem) {
				var item = new ClipboardItem({
					'text/plain': markdownPromise.then(function (text) {
						return new Blob([text], { type: 'text/plain' });
					})
				});
				navigator.clipboard.write([item]).then(markCopied);
			} else if (navigator.clipboard) {
				markdownPromise.then(function (text) {
					return navigator.clipboard.writeText(text);
				}).then(markCopied);
			}
		});
	});
	
	
	
	// LOCAL STORAGE
	function setWithExpiry(key, value, ttl) {
		const now = new Date()
		const item = {
			value: value,
			expiry: now.getTime() + ttl,
		}
		localStorage.setItem(key, JSON.stringify(item))
	}
	function getWithExpiry(key) {
		const itemStr = localStorage.getItem(key)
		if (!itemStr) {
			return null
		}
		const item = JSON.parse(itemStr)
		const now = new Date()
		if (now.getTime() > item.expiry) {
			localStorage.removeItem(key)
			return null
		}
		return item.value
	}


	
	// SEARCH 
	var resultSelected = null;
	var searchOverlay = document.querySelector('.searchoverlay');
	var searchInputs = function () { return document.querySelectorAll('.searchoverlay form input'); };
	if( OSdatid == "macos" && document.querySelector('.sidenavigation') && !drillNav ){
		document.querySelectorAll('.opensearch .shortcut.win').forEach(function (el) { Helpers.hide(el); });
		document.querySelectorAll('.opensearch .shortcut.mac').forEach(function (el) { Helpers.show(el); });
	}
	function setSearchOpen(open) {
		document.querySelectorAll('.searchoverlay').forEach(function (el) { el.classList.toggle('active', open); });
		document.body.classList.toggle('search', open);
	}
	var toggleSearch = function(){
		if (document.body.classList.contains('search')) {
			setSearchOpen(false);
		} else {
			setSearchOpen(true);
			var input = searchInputs()[0];
			if (input) input.focus();
		}
	};
	window.addEventListener('keydown', function (e){
		var searchOpen = document.body.classList.contains('search');
		// close Search on ESC
		if (e.key === 'Escape' && searchOpen) {
			setSearchOpen(false);
		}

		if ((e.metaKey || e.ctrlKey) && (e.code === 'KeyK' || (e.key && e.key.toLowerCase() === 'k'))) {
			// open search on cmd/ctrl + k
			e.preventDefault(); // Prevent default browser behavior for all browsers
			if (searchOverlay) {
				toggleSearch();
			}
		}
		// de-focus input when on enter or follow the result-link
		if (e.key === 'Enter' && document.body.classList.contains('search')) {
			var selected = document.querySelector('.search_result.selected');
			if (selected) {
				var selectedLink = selected.querySelector('a');
				if (selectedLink) document.location.href = selectedLink.getAttribute('href');
			} else {
				searchInputs().forEach(function (input) { input.blur(); });
			}
		}

		// scroll through results with up and down keys
		var focused = document.activeElement;
		var otherInputFocused = focused && focused.tagName === 'INPUT' && !focused.closest('.searchoverlay');
		if (!otherInputFocused && (e.key === 'ArrowDown' || e.key === 'ArrowUp') && document.body.classList.contains('search')) {
			e.preventDefault();
			var results = document.querySelectorAll('.search_result');
			var next;
			if (resultSelected) {
				resultSelected.classList.remove('selected');
				next = e.key === 'ArrowDown' ? resultSelected.nextElementSibling : resultSelected.previousElementSibling;
			}
			if (!next) {
				next = e.key === 'ArrowDown' ? results[0] : results[results.length - 1];
			}
			resultSelected = next || null;
			if (resultSelected) {
				resultSelected.classList.add('selected');
				resultSelected.scrollIntoView({ block: 'nearest' });
			}
		}
	});

	document.querySelectorAll('nav .search_icon, .opensearch').forEach(function (el) {
		el.addEventListener('click', toggleSearch);
	});
	document.querySelectorAll('.searchoverlay').forEach(function (overlay) {
		overlay.addEventListener('click', function (e) {
			if (e.target !== this) return;
			toggleSearch();
		});
	});
	document.querySelectorAll('.searchoverlay .empty_input').forEach(function (button) {
		button.addEventListener('click', function () {
			searchInputs().forEach(function (input) { input.value = ''; });
			var input = searchInputs()[0];
			if (input) input.focus();
			var results = document.getElementById('search_results');
			if (results) results.innerHTML = '';
			button.classList.remove('visible');
		});
	});

	// Show/hide empty_input button based on input content
	searchInputs().forEach(function (input) {
		input.addEventListener('input', function () {
			var filled = this.value.length > 0;
			document.querySelectorAll('.searchoverlay .empty_input').forEach(function (button) {
				button.classList.toggle('visible', filled);
			});
		});
	});
	document.querySelectorAll('.search_icon').forEach(function (icon) {
		icon.addEventListener('click', function () {
			const allHamburgers = Array.from(document.querySelectorAll('.hamburger'));
			if (!allHamburgers.some(Helpers.isVisible)) return;
			if (!allHamburgers.some(function (h) { return h.classList.contains('is-active'); })) return;
			if (document.body.classList.contains('search')) {
				allHamburgers.forEach(function (h) { h.classList.remove('is-active'); });
				document.querySelectorAll('body.documentation main .wrap.inactive').forEach(function (el) { el.classList.remove('inactive'); });
				document.querySelectorAll('.sidenavigation.slidein, nav.slidein').forEach(function (el) { el.classList.remove('slidein'); });
			} else {
				document.querySelectorAll('.sidenavigation').forEach(function (el) { el.classList.add('slidein'); });
				document.querySelectorAll('body.documentation main .wrap').forEach(function (el) { el.classList.add('inactive'); });
			}
		});
	});
	document.querySelectorAll('.hamburger').forEach(function (hamburger) {
		hamburger.addEventListener('click', function () {
			if (!this.classList.contains('is-active') && document.body.classList.contains('search')) {
				toggleSearch();
				document.querySelectorAll('.sidenavigation').forEach(function (el) { Helpers.fadeIn(el); });
				document.querySelectorAll('body.documentation main .wrap.inactive').forEach(function (el) { el.classList.remove('inactive'); });
			}
		});
	});
	
	// UPDATE HIGHLIGHT ELEMENT
	function updateHighlight(container, item) {
		if (!container || !item) return;
		var highlights = container.querySelectorAll('.select-highlight');
		if (!highlights.length) return;
		var left = Helpers.positionLeft(item) || 0;
		var width = item.getBoundingClientRect().width || 0;
		highlights.forEach(function (highlight) {
			highlight.style.left = left + 'px';
			highlight.style.width = width + 'px';
		});
	}

	function tabItems(containers) {
		var items = [];
		containers.forEach(function (container) {
			container.querySelectorAll(':scope > ul > li').forEach(function (li) { items.push(li); });
		});
		return items;
	}

	// QUICK INSTALLATION ON LANDING/HOME PAGE
	var envTopbars = document.querySelectorAll('.install .environment');
	if (envTopbars.length) {
		var envTopbar = envTopbars[0];
		var envItems = tabItems(envTopbars);

		var updateInstallation = function (item) {
			updateHighlight(envTopbar, item);
			var activeClient = item ? item.getAttribute('data-client') : undefined;
			var installDiv = document.querySelector('#quick-installation div[data-install=\'' + activeClient + ' ' + OSdatid + '\']') ||
				document.querySelector('#quick-installation div[data-install=\'' + activeClient + '\']');
			if (installDiv) {
				document.querySelectorAll('.result').forEach(function (el) { el.innerHTML = installDiv.innerHTML; });
			}
			var version = installDiv ? installDiv.getAttribute('data-version') : null;
			document.querySelectorAll('.bottombar .version').forEach(function (el) {
				if (version) {
					el.textContent = 'Latest version: ' + version;
					Helpers.show(el);
				} else {
					Helpers.hide(el);
				}
			});
		};

		updateInstallation(envItems.filter(function (li) { return li.classList.contains('active'); })[0]);

		envItems.forEach(function (li) {
			li.addEventListener('click', function () {
				envItems.forEach(function (other) { other.classList.remove('active'); });
				li.classList.add('active');
				updateInstallation(li);
			});
		});
	}

	// DUCKSTACK TABS ON LANDING/HOME PAGE
	var stackTopbars = document.querySelectorAll('section.duckstack .topbar');
	if (stackTopbars.length) {
		var stackTopbar = stackTopbars[0];
		var stackItems = tabItems(stackTopbars);
		var stackPanels = document.querySelectorAll('section.duckstack .stack-panel');

		updateHighlight(stackTopbar, stackItems.filter(function (li) { return li.classList.contains('active'); })[0]);

		stackItems.forEach(function (li) {
			li.addEventListener('click', function () {
				stackItems.forEach(function (other) { other.classList.remove('active'); });
				li.classList.add('active');
				updateHighlight(stackTopbar, li);
				var stack = li.getAttribute('data-stack');
				stackPanels.forEach(function (panel) {
					panel.classList.toggle('active', panel.getAttribute('data-stack') === stack);
				});
			});
		});
	}

	/** HIGHLIGHT TOC MENU **/
	var tocItems = [];
	document.querySelectorAll('.toc-entry > a[href^="#"]').forEach(function (link) {
		var heading = document.getElementById(decodeURIComponent(link.getAttribute('href').slice(1)));
		if (heading) tocItems.push({ heading: heading, entry: link.parentNode });
	});

	if (tocItems.length) {
		var tocEntries = document.querySelectorAll('.toc-entry');
		var tocTicking = false;

		var updateToc = function() {
			tocTicking = false;
			var scrollPos = window.scrollY + 150;
			var current = null;

			if (scrollPos + window.innerHeight >= document.documentElement.scrollHeight - 20) {
				current = tocItems[tocItems.length - 1].entry;
			} else {
				tocItems.forEach(function(item) {
					if (item.heading.getBoundingClientRect().top + window.scrollY <= scrollPos) {
						current = item.entry;
					}
				});
			}

			tocEntries.forEach(function (entry) { entry.classList.remove('current'); });
			if (current) {
				current.classList.add('current');
			}
		};

		window.addEventListener('scroll', function() {
			if (!tocTicking) {
				tocTicking = true;
				window.requestAnimationFrame(updateToc);
			}
		}, { passive: true });
	}


	/** HIDE BANNER **/
	var homeBanners = Array.prototype.filter.call(document.querySelectorAll('.banner'), function (el) {
		return !el.classList.contains('docversion');
	});
	var bannerVersion = function () {
		var value = homeBanners.length ? homeBanners[0].getAttribute('data-banner-version') : null;
		if (value !== null && value !== '' && String(+value) === value) return +value;
		return value || 'default';
	};
	var currentBannerVersion = bannerVersion();
	var storedBannerData = getWithExpiry("homeBanner");
	var shouldShowBanner = !storedBannerData || storedBannerData.version !== currentBannerVersion;

	homeBanners.forEach(function (banner) {
		if (!shouldShowBanner) {
			Helpers.hide(banner);
		} else {
			banner.style.display = 'flex';
		}
		banner.querySelectorAll('.close').forEach(function (close) {
			close.addEventListener('click', function(){
				setWithExpiry('homeBanner', {version: bannerVersion(), closed: true}, 172800000); // 900000 = 15 min, 172800000 = 2 days
				homeBanners.forEach(function (el) { Helpers.slideUp(el, 300); });
			});
		});
	});

	/** DOCS VERSION BANNER HEIGHT **/
	var docBanner = document.querySelector('.banner.docversion');
	if (docBanner) {
		var syncDocBannerHeight = function() {
			document.body.style.setProperty('--docbanner-height', docBanner.offsetHeight + 'px');
		};
		syncDocBannerHeight();
		window.addEventListener('resize', syncDocBannerHeight);
	}
	// setWithExpiry('homeBanner', '', -1); // deletes content

	/** BANNER ROTATOR **/
	(function() {
		var rotator = document.querySelector('.banner-rotator');
		var items = document.querySelectorAll('.banner-rotator .banner-item');
		if (items.length > 1) {
			var interval = (Number(rotator.getAttribute('data-interval')) || 7) * 1000;
			var current = 0;
			setInterval(function() {
				items[current].classList.remove('active');
				current = (current + 1) % items.length;
				items[current].classList.add('active');
			}, interval);
		}
	})();


	/** ADD WORD-BOXES TO CODE TABLES */
	document.querySelectorAll('.monospace_table + table tbody td').forEach(function (cell) {
		var children = Array.prototype.filter.call(cell.childNodes, function (node) {
			return node.nodeType !== Node.TEXT_NODE || node.nodeValue.trim().length > 0;
		});
		if (children.length === 1 && children[0].nodeType === Node.ELEMENT_NODE && children[0].tagName === 'CODE') {
			return;
		}
		var code = document.createElement('code');
		code.className = 'language-plaintext';
		while (cell.firstChild) {
			code.appendChild(cell.firstChild);
		}
		cell.appendChild(code);
	});
	
	/** RE-CALCULATE SELECT-ACTIVE-BUBBLES */
	var updateAllHighlights = function () {
		document.querySelectorAll('.topbar, .environment').forEach(function (container) {
			updateHighlight(container, container.querySelector('li.active'));
		});
	};
	window.addEventListener('load', updateAllHighlights);
	window.addEventListener('resize', updateAllHighlights);

	// DUCKCON EVENT PAGES
	const MAPBOX_ACCESS_TOKEN = 'pk.eyJ1Ijoiam9uYXRoYW4tYXVjaCIsImEiOiJjbDllMHhxNHowbG50M29vZ3Y0NnZhdHY1In0.XQxUUmkkSGKUkNThK1p9Yg';
	const MAPBOX_STYLES_URL = 'mapbox://styles/jonathan-auch/cmhz38wfd001801sbe3c06ece'
	const $duckconMap = $('.js-duckcon-map');
	const duckconSliderClass = '.js-duckcon-slider';
	const $duckconSlider = $(duckconSliderClass);

	const duckconSliderOptions = {
		slidesPerView: "auto",
		spaceBetween: 30,
		centeredSlides: true,
		loop: true,
		navigation: {
			nextEl: ".swiper-button-next",
			prevEl: ".swiper-button-prev",
		},
	}

	// Initialize the map if present on page
	if ($duckconMap.length) {
		const mapEl = $duckconMap[0];
		const lng = parseFloat(mapEl.dataset.lng);
		const lat = parseFloat(mapEl.dataset.lat);
		const label = mapEl.dataset.label;

		mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;

		const map = new mapboxgl.Map({
			container: 'duckcon-map',
			style: MAPBOX_STYLES_URL,
			center: [lng, lat],
			zoom: 15,
		});

		const marker = document.createElement('div');
		marker.className = 'js-marker map-marker';
		marker.dataset.label = label;
		new mapboxgl.Marker(marker).setLngLat([lng, lat]).addTo(map);
	}

	// Initialize the slider if present on page
	if ($duckconSlider.length) {
		new Swiper(duckconSliderClass, duckconSliderOptions);
	}

	// QUOTE SLIDER
	$('.quote-slider').each(function() {
		var $wrap = $(this);
		var $quotes = $wrap.children('blockquote.quote');
		if ($quotes.length < 2 || typeof Swiper === 'undefined') return;

		var $swiper = $('<div class="swiper"><div class="swiper-wrapper"></div></div>');
		var $track = $swiper.find('.swiper-wrapper');
		$quotes.each(function() {
			$('<div class="swiper-slide"></div>').append(this).appendTo($track);
		});

		var $controls = $(
			'<div class="quote-slider-controls">' +
				'<button type="button" class="quote-slider-prev" aria-label="Previous quote">' +
					'<svg class="icon"><use href="#chevron-left"></use></svg>' +
				'</button>' +
				'<button type="button" class="quote-slider-next" aria-label="Next quote">' +
					'<svg class="icon"><use href="#chevron-right"></use></svg>' +
				'</button>' +
			'</div>'
		);

		$wrap.empty().append($swiper).append($controls);

		function trailingSpace() {
			var slide = $swiper[0].querySelector('.swiper-slide');
			return slide ? Math.max(0, $swiper[0].clientWidth - slide.offsetWidth) : 0;
		}

		var delay = parseInt($wrap.data('autoplay'), 10);

		new Swiper($swiper[0], {
			slidesPerView: 'auto',
			spaceBetween: 20,
			slidesOffsetAfter: trailingSpace(),
			grabCursor: true,
			slideToClickedSlide: true,
			autoplay: delay > 0 ? {
				delay: delay,
				disableOnInteraction: true,
				pauseOnMouseEnter: true,
				stopOnLastSlide: true
			} : false,
			navigation: {
				nextEl: $controls.find('.quote-slider-next')[0],
				prevEl: $controls.find('.quote-slider-prev')[0]
			},
			on: {
				init: function() {
					$wrap.toggleClass('is-end', this.isEnd);
				},
				resize: function() {
					this.params.slidesOffsetAfter = trailingSpace();
					this.update();
				},
				reachEnd: function() {
					$wrap.addClass('is-end');
				},
				fromEdge: function() {
					$wrap.removeClass('is-end');
				}
			}
		});
	});

	// Author marquee: keep the scroll speed constant regardless of name length
	$(document).on('mouseenter', '.postpreview', function() {
		var author = this.querySelector('.byline .author, .meta .author');
		if (!author) return;
		var span = author.querySelector('span');
		if (!span) return;

		var distance = span.scrollWidth - author.clientWidth;
		if (distance < 24) {
			author.style.removeProperty('--marquee-duration');
			return;
		}

		var SPEED = 65;
		var MOVING = 0.92;
		var duration = distance / SPEED / MOVING;
		author.style.setProperty('--marquee-duration', duration.toFixed(2) + 's');
	});
});
