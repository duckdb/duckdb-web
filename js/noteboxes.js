$(document).ready(function(){

	var icons = {
		note: "info-circle",
		warning: "alert-triangle",
		tip: "lightbulb-02",
		bestpractice: "thumbs-up",
		deprecated: "alert-circle",
		update: "refresh-cw-02",
		installation: "target-05"
	};

	$('#main_content_wrap blockquote, .singleentry blockquote').each(function() {
		var $blockquote = $(this);
		var blockquoteText = $blockquote.text().trim();
		var firstWord = blockquoteText.split(' ')[0];

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
			var $last = $blockquote.find('.content > p:last-child');
			if (/^(\u2013|\u2014|--)/.test($last.text().trim())) {
				$last.addClass('quote-author');
			}
		} else {
			var label = (className == "bestpractice") ? 'Best practice' : (hasKeyword ? firstWord : 'Note');
			$blockquote.find('.content').prepend('<span class="sr-only">' + label + '</span>');
			$blockquote.prepend('<div class="symbol" title="' + label + '"><svg class="icon"><use href="#' + icons[className] + '"></use></svg></div>');
		}

	});

});
