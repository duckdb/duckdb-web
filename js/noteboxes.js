$(document).ready(function(){
	
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
			default:
				className = "default"; 
				break;
		}
		
		$blockquote.addClass(className);
		
		if (className !== "default") {
			$blockquote.find('p:first-child').html(function(_, oldHtml) {
				return oldHtml.replace(firstWord, '').trim();
			});
		}
		
		$blockquote.wrapInner('<div class="content"></div>');
		
		if (className == "bestpractice") {
			$blockquote.find('.content').prepend('<h4>Best Practice</h4>');
		} else if (className !== "default") {
			$blockquote.find('.content').prepend('<h4>' + firstWord + '</h4>');
		}

		$blockquote.prepend('<div class="symbol"></div>');
		
	});
		
	
});
