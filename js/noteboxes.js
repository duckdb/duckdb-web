$(document).ready(function(){

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

	$('#main_content_wrap blockquote, .singleentry blockquote').each(function() {
		var $blockquote = $(this);
		var firstWord = $blockquote.children('p').first().text().trim().split(/\s+/)[0];

		var className = "";

		switch (firstWord) {
			case "Note":
				className = "note";
				break;
			case "Warning":
				className = "warning";
				break;
			case "Tip":
				className = "tip";
				break;
			case "Bestpractice":
				className = "bestpractice";
				break;
			case "Deprecated":
				className = "deprecated";
				break;
			case "Update":
				className = "update";
				break;
			case "Installation":
				className = "installation";
				break;
			case "Quote":
				className = "quote";
				break;
			case "New":
				className = "new";
				break;
			default:
				className = "";
				break;
		}

		var hasKeyword = className !== "";
		if (!hasKeyword) {
			className = "note";
		}

		$blockquote.addClass(className);

		if (hasKeyword) {
			$blockquote.find('p:first-child').html(function(_, oldHtml) {
				return oldHtml.replace(firstWord, '').trim();
			});
		}

		$blockquote.wrapInner('<div class="content"></div>');

		if (className === "quote") {
			var $content = $blockquote.children('.content');
			var $first = $content.children('p').first();
			if (!$first.text().trim() && !$first.find('img').length) {
				$first.remove();
			}
			var $last = $blockquote.find('.content > p:last-child');
			if (/^(\u2013|\u2014|--)/.test($last.text().trim())) {
				$last.addClass('quote-author');
				var authorName = $last.text().trim().replace(/^(\u2013|\u2014|--)\s*/, '');
				var $author = $('.postheader-author').filter(function() {
					return $(this).find('.name').text().trim() === authorName;
				}).first();
				if (!$last.find('img').length) {
					$last.prepend($author.find('img.avatar').clone());
				}
			}
			var $quoteText = $content.children('p').not('.quote-author');
			$quoteText.first().addClass('quote-open').html(function(_, html) {
				return html.replace(/^(\s*(?:<[^>]+>\s*)*)[“"]/, '$1');
			});
			if (!/[”"]$/.test($quoteText.last().text().trim())) {
				$quoteText.last().addClass('quote-close');
			}
			$content.prepend('<span class="sr-only">Quote</span>');
		} else {
			var label = (className == "bestpractice") ? 'Best practice' : (hasKeyword ? firstWord : 'Note');
			$blockquote.find('.content').prepend('<span class="sr-only">' + label + '</span>');
			$blockquote.prepend('<div class="symbol" title="' + label + '"><svg class="icon"><use href="#' + icons[className] + '"></use></svg></div>');
		}

	});

});
