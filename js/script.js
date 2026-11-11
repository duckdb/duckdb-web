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
	if ($('.filterbar').length !== 0) {

		/* CUSTOM FITROWS FUNCTION FOR ISOTOPE TO GET EQUAL HEIGHT TILES */
		!function(t){"use strict";function i(t){var i=t.create("fitRows");return i.prototype._resetLayout=function(){if(this.x=0,this.y=0,this.maxY=0,this.row=0,this.rows=[],this._getMeasurement("gutter","outerWidth"),this.options.equalheight)for(var t=0;t<this.isotope.items.length;t++)this.isotope.items[t].css({height:"auto"})},i.prototype._getItemLayoutPosition=function(t){t.getSize();var i=this.gutter||0,s=t.size.outerWidth,o=Math.ceil(this.isotope.size.innerWidth+i);0!==this.x&&s+this.x+i>o&&(this.x=0,this.y=this.maxY+i),0===this.x&&0!==this.y&&this.row++;var e={x:this.x,y:this.y};return this.maxY=Math.max(this.maxY,this.y+t.size.outerHeight),this.x+=s+i,void 0===this.rows[this.row]?(this.rows[this.row]=[],this.rows[this.row].start=this.y,this.rows[this.row].end=this.maxY):this.rows[this.row].end=Math.max(this.rows[this.row].end,this.maxY),t.row=this.row,e},i.prototype._equalHeight=function(){for(var t=0;t<this.isotope.items.length;t++){var i=this.isotope.items[t].row,s=this.rows[i];if(s){var o=s.end-s.start;o-=this.isotope.items[t].size.borderTopWidth+this.isotope.items[t].size.borderBottomWidth,o-=this.isotope.items[t].size.marginTop+this.isotope.items[t].size.marginBottom,o-=this.gutter.height||0,!1==this.isotope.items[t].size.isBorderBox&&(o-=this.isotope.items[t].size.paddingTop+this.isotope.items[t].size.paddingBottom),this.isotope.items[t].size.height=o,this.isotope.items[t].css({height:o.toString()+"px"})}}},i.prototype._getContainerSize=function(){return this.options.equalheight&&this._equalHeight(),{height:this.maxY}},i}"function"==typeof define&&define.amd?define(["../layout-mode"],i):"object"==typeof exports?module.exports=i(require("../layout-mode")):i(t.Isotope.LayoutMode)}(window);

		var $grid = $('.newstiles').isotope({
			itemSelector: '.postpreview',
			layoutMode: 'fitRows',
			fitRows: {
				gutter: $('.guides-list').length ? 16 : 32,
				equalheight: true
			}
		});

		var $heading = $('.pagetitle h1').first();
		var defaultHeading = $.trim($heading.text());
		var $search = $('#search-input');
		var $topicFilter = $('#topic-filter');
		var $coreToggle = $('#core-toggle');
		var $empty = $('.filter-empty');
		var activeFilter = '*';

		function updateFilterHighlight($button) {
			var $highlight = $button.closest('.filtertags').find('.filter-highlight');
			if ($highlight.length && $button.is(':visible')) {
				$highlight.css({
					left: $button.position().left,
					width: $button.outerWidth()
				});
			}
		}

		function setActiveFilter(value) {
			activeFilter = value;
			var $topics = $topicFilter.find('[data-filter]');
			var $topic = $topics.filter(function() { return $(this).attr('data-filter') === value; });
			$topics.removeAttr('aria-current').parent().removeClass('current');
			$topic.attr('aria-current', 'true').parent().addClass('current');
			$topicFilter.find('.selectedversion').text($topic.text());
			$topicFilter.find('.versiontrigger').attr('aria-label', 'Filter guides by topic: ' + $topic.text());
			$('.filterbar .filtertags').each(function() {
				var $buttons = $(this).find('.filter-btn').removeClass('active');
				var $match = $buttons.filter('[data-filter="' + value + '"]').addClass('active');
				updateFilterHighlight($match);
			});
			var heading = $('.filterbar .filter-btn.active').first().attr('data-heading');
			$heading.text(heading || defaultHeading);
		}

		function readFiltersFromURL() {
			var params = new URLSearchParams(window.location.search);
			var type = params.get('type');
			if (type && $('.filterbar [data-filter]').filter(function() {
				return $(this).attr('data-filter') === '.' + type;
			}).length) {
				setActiveFilter('.' + type);
			}
			if (params.get('q')) {
				$search.val(params.get('q'));
			}
			if (params.get('core') === '1') {
				$coreToggle.prop('checked', true);
			}
		}

		function writeFiltersToURL() {
			var params = new URLSearchParams();
			if (activeFilter !== '*') {
				params.set('type', activeFilter.replace(/^\./, ''));
			}
			if ($coreToggle.is(':checked')) {
				params.set('core', '1');
			}
			if ($search.val()) {
				params.set('q', $search.val());
			}
			history.replaceState(null, '', window.location.pathname + (params.toString() ? '?' + params.toString() : ''));
		}

		function applyFilters() {
			var searchValue = $search.val().toLowerCase().trim();
			var coreOnly = $coreToggle.is(':checked');

			$grid.closest('.events-section').removeClass('is-empty');

			$grid.isotope({
				filter: function() {
					var $item = $(this);
					if (activeFilter !== '*' && !$item.is(activeFilter)) return false;
					if (coreOnly && $item.attr('data-core') !== 'true') return false;
					if (searchValue && ($item.attr('data-search') || '').indexOf(searchValue) === -1) return false;
					return true;
				}
			});

			var visible = 0;
			$grid.each(function() {
				var iso = $(this).data('isotope');
				var count = iso ? iso.filteredItems.length : 0;
				visible += count;
				$(this).closest('.events-section').toggleClass('is-empty', count === 0);
			});
			$empty.prop('hidden', visible > 0);
		}

		$('.filterbar').on('click', '[data-filter]', function(e) {
			e.preventDefault();
			setActiveFilter($(this).attr('data-filter'));
			applyFilters();
			writeFiltersToURL();
			if ($(this).closest($topicFilter).length) {
				$topicFilter.removeClass('active').find('.versiontrigger').attr('aria-expanded', 'false').trigger('focus');
			}
		});

		$search.on('input', function() {
			applyFilters();
			writeFiltersToURL();
		});

		$coreToggle.on('change', function() {
			applyFilters();
			writeFiltersToURL();
		});

		// --- Mobile filter modal ---
		var $filterToggle = $('.filter-toggle');
		var $filterModal = $('.filter-modal');
		var $filterOverlay = $('.filter-overlay');

		function setFilterModal(open) {
			$filterToggle.toggleClass('is-open', open);
			$filterModal.toggleClass('is-open', open);
			$filterOverlay.toggleClass('is-open', open);
			if (open) {
				updateFilterHighlight($filterModal.find('.filter-btn.active'));
			}
		}

		$filterToggle.on('click', function() {
			setFilterModal(!$filterModal.hasClass('is-open'));
		});
		$filterOverlay.on('click', function() {
			setFilterModal(false);
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
	const $drillNav = $('.sidenav-drill');
	const $navRoot = $drillNav.children('.sidenav');
	const navMotionKey = 'docs-sidebar-enter';

	$drillNav.on('click', '.sidenav > .hasSub > a.nav-row', function(e) {
		if ($navRoot.hasClass('is-drilled') || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button !== 0) return;
		if (window.matchMedia('(max-width: 900px)').matches) {
			e.preventDefault();
			enterDrill($(this).parent());
			return;
		}
		try { sessionStorage.setItem(navMotionKey, new URL(this.href).pathname); } catch (e) {}
	});

	$navRoot.on('animationend', function(e) {
		if (e.originalEvent.animationName !== 'docs-sidebar-enter') return;
		$(this).removeClass('nav-motion');
		document.documentElement.classList.remove('docs-sidebar-enter');
	});

	function setDrill($item, open) {
		$navRoot.addClass('nav-motion');
		$item.toggleClass('is-open', open);
		$item.children('.nav-drill').attr('aria-expanded', open);
		$item.parent('.nav-list').toggleClass('is-drilled', open);
	}

	function enterDrill($item) {
		setDrill($item, true);
		$drillNav.add($drillNav.children('.sidenav')).scrollTop(0);
		$item.find('> .nav-list > .nav-back > button').trigger('focus');
	}

	$drillNav.on('click', '.nav-drill', function() {
		enterDrill($(this).parent());
	});

	$drillNav.on('click', '.nav-back button', function() {
		const $item = $(this).closest('.nav-list').parent('.nav-item');
		setDrill($item, false);
		$item.children('.nav-row').trigger('focus');
	});

	$drillNav.on('click', '.nav-expand', function() {
		const open = $(this).attr('aria-expanded') !== 'true';
		$(this).attr('aria-expanded', open).parent().toggleClass('is-open', open);
	});

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
	function cleanNavClone($list) {
		$list.find('.nav-back').remove();
		$list.find('svg').remove();
		$list.find('.nav-drill, .nav-expand').replaceWith(function() {
			return $('<span>').text($(this).text());
		});
		$list.removeClass('is-drilled').find('.is-open, .is-drilled').removeClass('is-open is-drilled');
		return $list;
	}

	const $currentNavLink = $('.sidenav-drill [aria-current="page"]');
	if (window.location.href.includes("/overview") && $currentNavLink.length) {
		const $overviewList = $currentNavLink.closest('.nav-list').clone().removeClass('sidenav');
		$overviewList.find('[aria-current="page"]').parent().remove();
		$('#main_content_wrap .index').append(cleanNavClone($overviewList));
	}

	// Appending Content-List of Documentation
	if ($('#docusitemaphere').length) {
		$('#docusitemaphere').append(cleanNavClone($('.sidenav-drill ul.sidenav').clone()));
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
	var $docDropdowns = $('.options .version, #topic-filter');
	function closeVersionSelect() {
		var $open = $docDropdowns.filter('.active');
		if (!$open.length) return false;
		$open.removeClass('active').find('.versiontrigger').attr('aria-expanded', 'false');
		return true;
	}

	$docDropdowns.find('.versiontrigger').on('click', function(){
		var $version = $(this).closest('.version');
		var open = !$version.hasClass('active');
		closeVersionSelect();
		$version.toggleClass('active', open);
		$(this).attr('aria-expanded', open ? 'true' : 'false');
	});

	$(document).on('click', function(e){
		if ($(e.target).closest('.options .version, #topic-filter').length) return;
		closeVersionSelect();
	});

	$(document).on('keydown', function(e){
		if (e.key !== 'Escape') return;
		var $trigger = $docDropdowns.filter('.active').find('.versiontrigger');
		if (closeVersionSelect()) {
			$trigger.trigger('focus');
		}
	});

	$docDropdowns.on('keydown', function(e) {
		if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
		e.preventDefault();
		var $dropdown = $(this);
		var $links = $dropdown.find('.versionsidebar a');
		var index = $links.index(document.activeElement);
		closeVersionSelect();
		$dropdown.addClass('active').find('.versiontrigger').attr('aria-expanded', 'true');
		index = e.key === 'ArrowDown' ? (index + 1) % $links.length : (index <= 0 ? $links.length - 1 : index - 1);
		$links.eq(index).trigger('focus');
	});

	$docDropdowns.on('focusout', function(e) {
		if (!this.contains(e.relatedTarget)) {
			$(this).removeClass('active').find('.versiontrigger').attr('aria-expanded', 'false');
		}
	});

	// COPY PAGE AS MARKDOWN
	$('.headlinebar .copy-markdown').on('click', function(){
		var $btn = $(this);
		if ($btn.hasClass('copied')) return;

		var markdownPromise = fetch($btn.attr('data-source')).then(function(response){
			if (!response.ok) throw new Error('HTTP ' + response.status);
			return response.text();
		});

		function markCopied() {
			$btn.addClass('copied');
			$btn.find('use').attr('href', '#check');
			$btn.find('span').text('Copied');
			setTimeout(function(){
				$btn.removeClass('copied');
				$btn.find('use').attr('href', '#copy-01');
				$btn.find('span').text('Copy Markdown');
			}, 2000);
		}

		if (navigator.clipboard && window.ClipboardItem) {
			var item = new ClipboardItem({
				'text/plain': markdownPromise.then(function(text){
					return new Blob([text], { type: 'text/plain' });
				})
			});
			navigator.clipboard.write([item]).then(markCopied);
		} else if (navigator.clipboard) {
			markdownPromise.then(function(text){
				return navigator.clipboard.writeText(text);
			}).then(markCopied);
		}
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
	var resultSelected;
	if( OSdatid == "macos" && $('.sidenavigation').length && !$drillNav.length ){
		$('.opensearch .shortcut.win').hide();
		$('.opensearch .shortcut.mac').show();
	}
	var toggleSearch = function(){
		if( $('body').hasClass('search') ){
			$('.searchoverlay').removeClass('active');
			$('body').removeClass('search');
		} else {
			$('.searchoverlay').addClass('active');
			$('body').addClass('search');
			$( ".searchoverlay form input" ).trigger('focus');
		}
	}
	$(window).on('keydown', function (e){
		// close Search on ESC
		if( ( e.which === 27 ) && $('body').hasClass('search') ){
			$('.searchoverlay').removeClass('active');
			$('body').removeClass('search');
		}
		
		if ( e.metaKey && ( e.which === 75 ) || e.ctrlKey && ( e.which === 75 ) ) {
			// open search on cmd/ctrl + k
			e.preventDefault(); // Prevent default browser behavior for all browsers
			if( $('.searchoverlay').length ){
				toggleSearch();
			}
		}
		// de-focus input when on enter or follow the result-link
		if ( e.which === 13  && $('body').hasClass('search') ){
			if( $('.search_result.selected').length ){
				var link = $('.search_result.selected').find('a').attr('href');
				document.location.href = link
			} else {
				$( ".searchoverlay form input" ).trigger('blur');
			}
		}
		
		// scroll through results with up and down keys
		if ( !($("input").is(":focus")) && e.which === 40 && $('body').hasClass('search') || !($("input").is(":focus")) && e.which === 38 && $('body').hasClass('search') ) {
			var result = $('.search_result');
			if(e.which === 40){
				if(resultSelected){
					resultSelected.removeClass('selected');
					next = resultSelected.next();
					if(next.length > 0){
						resultSelected = next.addClass('selected');
					}else{
						resultSelected = result.eq(0).addClass('selected');
					}
				}else{
					resultSelected = result.eq(0).addClass('selected');
				}
			}else if(e.which === 38){
				if(resultSelected){
					resultSelected.removeClass('selected');
					next = resultSelected.prev();
					if(next.length > 0){
						resultSelected = next.addClass('selected');
					}else{
						resultSelected = result.last().addClass('selected');
					}
				}else{
					resultSelected = result.last().addClass('selected');
				}
			}
		}
	});
	
	$('nav .search_icon').on('click', function(){
		toggleSearch();
	});
	$('.opensearch').on('click', function(){
		toggleSearch();
	});
	$('.searchoverlay').on('click', function(e){
		if (e.target !== this)
			return;
		toggleSearch();
	});
	$('.searchoverlay .empty_input').on('click', function(){
		$(".searchoverlay form input").val('').trigger('focus');
		$("#search_results").empty();
		$(this).removeClass('visible');
	})
	
	// Show/hide empty_input button based on input content
	$(".searchoverlay form input").on('input', function() {
		if($(this).val().length > 0) {
			$('.searchoverlay .empty_input').addClass('visible');
		} else {
			$('.searchoverlay .empty_input').removeClass('visible');
		}
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
	function updateHighlight($container, $item) {
		const $highlight = $container.find(".select-highlight");
		if ($highlight.length && $item.length) {
			const itemOffset = $item.position();
			const itemWidth = $item.outerWidth();
			$highlight.css({
				left: itemOffset.left || 0,
				width: itemWidth || 0,
			});
		}
	}
	
	// QUICK INSTALLATION ON LANDING/HOME PAGE
	if ($(".install .environment").length) {
		const $envTopbar = $(".install .environment");
		const $envItems = $envTopbar.find("> ul > li");
		const $activeEnvItem = $envItems.filter(".active");
		
		function updateInstallation($item) {
			updateHighlight($envTopbar, $item);
			const activeClient = $item.attr("data-client");
			let $installDiv = $(
				`#quick-installation div[data-install='${activeClient} ${OSdatid}']`
			);
			if (!$installDiv.length) {
				$installDiv = $(
					`#quick-installation div[data-install='${activeClient}']`
				);
			}
			$(".result").html($installDiv.html());
			const version = $installDiv.attr("data-version");
			const $versionSpan = $(".bottombar .version");
			if (version) {
				$versionSpan.text("Latest version: " + version).show();
			} else {
				$versionSpan.hide();
			}
		}
		
		updateInstallation($activeEnvItem);
	
		$envItems.on('click', function () {
			$envItems.removeClass("active");
			$(this).addClass("active");
			updateInstallation($(this));
		});
	}

	// DUCKSTACK TABS ON LANDING/HOME PAGE
	if ($("section.duckstack .topbar").length) {
		const $stackTopbar = $("section.duckstack .topbar");
		const $stackItems = $stackTopbar.find("> ul > li");
		const $stackPanels = $("section.duckstack .stack-panel");

		updateHighlight($stackTopbar, $stackItems.filter(".active"));

		$stackItems.on('click', function () {
			$stackItems.removeClass("active");
			$(this).addClass("active");
			updateHighlight($stackTopbar, $(this));
			const stack = $(this).attr("data-stack");
			$stackPanels.removeClass("active");
			$stackPanels.filter(`[data-stack='${stack}']`).addClass("active");
		});
	}

	/** HIGHLIGHT TOC MENU **/
	const tocItems = $('.toc-entry > a[href^="#"]').map(function() {
		const heading = document.getElementById(decodeURIComponent(this.getAttribute('href').slice(1)));
		return heading ? { heading: heading, entry: this.parentNode } : null;
	}).get();

	if (tocItems.length) {
		const $tocEntries = $('.toc-entry');
		let tocTicking = false;

		const updateToc = function() {
			tocTicking = false;
			const scrollPos = window.scrollY + 150;
			let current = null;

			if (scrollPos + window.innerHeight >= document.documentElement.scrollHeight - 20) {
				current = tocItems[tocItems.length - 1].entry;
			} else {
				tocItems.forEach(function(item) {
					if (item.heading.getBoundingClientRect().top + window.scrollY <= scrollPos) {
						current = item.entry;
					}
				});
			}

			$tocEntries.removeClass('current');
			if (current) {
				current.classList.add('current');
			}
		};

		$(window).on('scroll', function() {
			if (!tocTicking) {
				tocTicking = true;
				window.requestAnimationFrame(updateToc);
			}
		});
	}


	/** HIDE BANNER **/
	const $homeBanner = $('.banner').not('.docversion');
	const currentBannerVersion = $homeBanner.data('banner-version') || 'default';
	const storedBannerData = getWithExpiry("homeBanner");
	const shouldShowBanner = !storedBannerData || storedBannerData.version !== currentBannerVersion;

	if (!shouldShowBanner) {
		$homeBanner.hide();
	} else {
		$homeBanner.css('display', 'flex');
	}
	$homeBanner.find('.close').on('click', function(){
		const bannerVersion = $homeBanner.data('banner-version') || 'default';
		setWithExpiry('homeBanner', {version: bannerVersion, closed: true}, 172800000); // 900000 = 15 min, 172800000 = 2 days
		$homeBanner.slideUp(300);
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
		var $rotator = $('.banner-rotator');
		var $items = $rotator.find('.banner-item');
		if ($items.length > 1) {
			var interval = ($rotator.data('interval') || 7) * 1000;
			var current = 0;
			setInterval(function() {
				$items.eq(current).removeClass('active');
				current = (current + 1) % $items.length;
				$items.eq(current).addClass('active');
			}, interval);
		}
	})();


	/** ADD WORD-BOXES TO CODE TABLES */
	$('.monospace_table + table tbody td').each(function() {
		var $cell = $(this);
		var $children = $cell.contents().filter(function() {
			return this.nodeType !== Node.TEXT_NODE || $.trim(this.nodeValue).length > 0;
		});
		if ($children.length === 1 && $children[0].nodeType === Node.ELEMENT_NODE && $children[0].tagName === 'CODE') {
			return;
		}
		$cell.wrapInner('<code class="language-plaintext"></code>');
	});
	
	/** RE-CALCULATE SELECT-ACTIVE-BUBBLES */
	$(window).on('load', function() {
		$('.topbar, .environment').each(function() {
			var $activeItem = $(this).find('li.active');
			updateHighlight($(this), $activeItem);
		});
	});
	$(window).on('resize', function() {
		$('.topbar, .environment').each(function() {
			var $activeItem = $(this).find('li.active');
			updateHighlight($(this), $activeItem);
		});
	});

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
