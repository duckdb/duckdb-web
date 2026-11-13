(function () {

	var icons = {
		note: "info-circle",
		warning: "alert-triangle",
		tip: "lightbulb-02",
		bestpractice: "thumbs-up",
		deprecated: "alert-circle",
		update: "refresh-cw-02",
		installation: "settings-02",
		new: "stars-01"
	};

	var keywords = {
		Note: "note",
		Warning: "warning",
		Tip: "tip",
		Bestpractice: "bestpractice",
		Deprecated: "deprecated",
		Update: "update",
		Installation: "installation",
		Quote: "quote",
		New: "new"
	};

	var dashPattern = /^(?:–|—|--|-(?=\s))/;

	function childParagraphs(el) {
		return Array.prototype.filter.call(el.children, function (child) {
			return child.tagName === 'P';
		});
	}

	document.querySelectorAll('#main_content_wrap blockquote, .singleentry blockquote').forEach(function (blockquote) {
		var firstParagraph = childParagraphs(blockquote)[0];
		var firstWord = firstParagraph ? firstParagraph.textContent.trim().split(/\s+/)[0] : '';

		var className = Object.prototype.hasOwnProperty.call(keywords, firstWord) ? keywords[firstWord] : '';
		var hasKeyword = className !== '';
		if (!hasKeyword) {
			className = 'note';
		}

		blockquote.classList.add(className);

		if (hasKeyword) {
			blockquote.querySelectorAll('p:first-child').forEach(function (p) {
				p.innerHTML = p.innerHTML.replace(firstWord, '').trim();
			});
		}

		var content = document.createElement('div');
		content.className = 'content';
		while (blockquote.firstChild) {
			content.appendChild(blockquote.firstChild);
		}
		blockquote.appendChild(content);

		if (className === 'quote') {
			var first = childParagraphs(content)[0];
			if (first && !first.textContent.trim() && !first.querySelector('img')) {
				first.remove();
			}
			var last = content.querySelector(':scope > p:last-child');
			if (last && dashPattern.test(last.textContent.trim())) {
				last.classList.add('quote-author');
				var authorName = last.textContent.trim().replace(dashPattern, '').trim();
				// Match if the attribution starts with the author's name,
				// e.g., "Ilya Boyandin, creator of SQLRooms" matches "Ilya Boyandin"
				var author = Array.prototype.find.call(document.querySelectorAll('.postheader-author'), function (el) {
					var nameEl = el.querySelector('.name');
					var name = nameEl ? nameEl.textContent.trim() : '';
					return name !== '' && authorName.indexOf(name) === 0 &&
						!/^[\p{L}\p{N}]/u.test(authorName.slice(name.length));
				});
				var avatar = author && author.querySelector('img.avatar');
				if (!last.querySelector('img') && avatar) {
					last.prepend(avatar.cloneNode(true));
				}
				var walker = document.createTreeWalker(last, NodeFilter.SHOW_TEXT);
				var dashNode;
				while ((dashNode = walker.nextNode()) && !dashNode.nodeValue.trim()) {}
				if (dashNode) {
					dashNode.nodeValue = dashNode.nodeValue.replace(/^\s*/, '').replace(dashPattern, '').replace(/^\s*/, '');
				}
			}
			var quoteText = childParagraphs(content).filter(function (p) {
				return !p.classList.contains('quote-author');
			});
			if (quoteText.length) {
				quoteText[0].classList.add('quote-open');
				quoteText[0].innerHTML = quoteText[0].innerHTML.replace(/^(\s*(?:<[^>]+>\s*)*)[“"]/, '$1');
				var lastQuote = quoteText[quoteText.length - 1];
				if (!/[”"]$/.test(lastQuote.textContent.trim())) {
					lastQuote.classList.add('quote-close');
				}
			}
			content.insertAdjacentHTML('afterbegin', '<span class="sr-only">Quote</span>');
		} else {
			var label = (className === 'bestpractice') ? 'Best practice' : (hasKeyword ? firstWord : 'Note');
			content.insertAdjacentHTML('afterbegin', '<span class="sr-only">' + label + '</span>');
			blockquote.insertAdjacentHTML('afterbegin', '<div class="symbol" title="' + label + '"><svg class="icon"><use href="#' + icons[className] + '"></use></svg></div>');
		}

	});

})();
