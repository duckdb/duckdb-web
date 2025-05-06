$(document).ready(function(){

	let installationData = [];

	$.get('/data/installation-data-1.2.yml?121a', function(data) {
		// console.log(data)
		installationData = jsyaml.load(data);
		evaluation();
	});

	// Docs Installation Functions 
	function showAllSections() {
		$('.yourselection .hide').removeClass('hide');
		$('.yourselection .select ul li.inactive').removeClass('inactive')
	}
	
	function hideSections(sections) {
		if ( sections !== undefined ) {
			sections.split(',').forEach(section => {
				const $container = $(`.select[data-select="${section.trim()}"]`);
				$container.addClass('hide')
				$container.find('.selected').removeClass('selected');
			});
		}
	}
	
	// Docs Installation Selection
	
	var OSName="Unknown OS";
	var OSdatid="Unknown OS";
	if (navigator.appVersion.indexOf("Win")!=-1) { OSName="Windows"; OSdatid="win" };
	if (navigator.appVersion.indexOf("Mac")!=-1) { OSName="macOS"; OSdatid="macos" };
	if (navigator.appVersion.indexOf("X11")!=-1) { OSName="UNIX"; OSdatid="linux" };
	if (navigator.appVersion.indexOf("Linux")!=-1) { OSName="Linux"; OSdatid="linux"};
	$('.systemdetected').html('System detected: '+OSName);
	
	function replaceHtmlEntities( markup ) {
		markup = markup.replace( /&/g, '&amp;' );
		markup = markup.replace( /</g, '&lt;' );
		markup = markup.replace( />/g, '&gt;' );
		markup = markup.replace( /\n/g, '<br>' );
		return markup
	}
	
	function simpleCodeHighlight( markup ) {
		markup = markup.replace( /&amp;&amp;\s*/g, '&amp;&amp;<br>' );
		markup = markup.replace( /("(.*?)")/g, '<span class="s2">$1</span>' );
		markup = markup.replace( /^install\.packages\((.*)\)$/, '<span class="n">install.packages</span><span class="p">(</span>$1<span class="p">)</span>' );
		markup = markup.replace( 'brew install', '<span class="nb">brew install</span>' );
		markup = markup.replace( 'cargo add', '<span class="nb">cargo add</span>' );
		markup = markup.replace( 'npm install', '<span class="nb">npm install</span>' );
		markup = markup.replace( 'pip install', '<span class="nb">pip install</span>' );
		markup = markup.replace( 'winget install', '<span class="nb">winget install</span>' );
		markup = markup.replace( 'curl', '<span class="nb">curl</span>' );
		markup = markup.replace( '| sh', '| <span class="nb">sh</span>' );
		markup = markup.replace( /([^-._'"/])duckdb([^-._'"/])/, '$1<span class="nb">duckdb</span>$2' );
		markup = markup.replace( /^duckdb$/, '<span class="nb">duckdb</span>' );
		markup = markup.replace( 'go get', '<span class="nb">go get</span>' );
		markup = markup.replace( '--upgrade', '<span class="nt">--upgrade</span>' );
		markup = markup.replace( '--features', '<span class="nt">--features</span>' );
		markup = markup.replace( '--pre', '<span class="nt">--pre</span>' );
		markup = markup.replace( /(&lt;\/?.*?&gt;)/g, '<span class="nt">$1</span>' );
		return markup;
	}
	
	var evaluation = function () {
		showAllSections();
	
		if ( installationData.length == 0 ) {
			return;
		}
	
		// Check the selected items
		var variant = $( '.yourselection .version .selected' ).attr( 'data-id' ).replace(/^\./, '' );
		var environment = $( '.yourselection .environment .selected' ).text();
		var platform = $( '.yourselection .platform .selected' ).text();
		var download_method = $( '.yourselection .download_method .selected' ).text();
		var architecture = $( '.yourselection .architecture .selected' ).text();
	
		if ( variant != 'stable' ) {
			variant = 'nightly';
		}
	
		var configurables = [];
		var configurablesMinusArchitecture = [];
		for( var i in installationData ) {
			if ( installationData[i].variant == variant && installationData[i].environment == environment ) {
				configurables.push( installationData[i] );
			}
		}
	
		// Disable any language that is not applicable in configurables
		$( '.environment li' ).addClass( 'disabled-choice' );
		for ( var i in installationData ) {
			$( '.environment li' ).each( function() {
				if ( installationData[i].variant == variant && $( this ).text().toLowerCase() == installationData[i].environment.toLowerCase() ) {
					$( this ).removeClass( 'disabled-choice' );
				}
			});
		}
	
		if ( $( '.environment .disabled-choice.selected' ).length > 0 ) {
			$( '.environment .selected' ).removeClass( 'selected' ).siblings( 'li:not(.disabled-choice)' ).first().trigger( 'click' );
			return;
		}
	
		configurablesMinusArchitecture = configurables;
		
		var sectionsToHide = [];
	
		if ( configurables.length == 1 ) {
			sectionsToHide.push( 'download_method' );
			sectionsToHide.push( 'architecture' );
			sectionsToHide.push( 'platform' );
		}
	
		// Check if we have multiple options of platform across different configurables
		if ( configurables.length > 1 ) {
			var hasPlatforms = false;
			for ( var i in configurables ) {
				if ( configurables[i].platform != 'all' ) {
					hasPlatforms = true;
				}
			}
	
			if ( ! hasPlatforms ) {
				hideSections( 'platform' );
			}
		}
	
		if ( hasPlatforms ) {
			if ( $( '.yourselection .platform .selected' ).length == 0 ) {
				// select first one and return
				$( '.yourselection .platform li:first-child' ).click();
				return;
			}
	
			configurables = configurables.filter( function ( item ) {
				return item.platform.toLowerCase() == platform.toLowerCase();
			} );
	
			configurablesMinusArchitecture = configurablesMinusArchitecture.filter( function ( item ) {
				return item.platform.toLowerCase() == platform.toLowerCase();
			});
		}
		
	

		
	
		// Check if we have multiple download_method across different configurables
		var download_methods = configurables.map( function ( item ) {
			return item.download_method.toLowerCase();
		});
	
		// Get possible architectures
		var architectures = configurables.map( function ( item ) {
			return item.architecture.toLowerCase();
		});
	
		// Get unique download_methods
		// new Set(download_methods).size == 1 || 
		if ( download_methods.length == 0 ) {
			hideSections( 'download_method' );
		}
	
		if ( configurables.length == 0 && architecture != '' && $( '.architecture .selected' ).length > 0 ) {
			$( '.architecture .selected' ).siblings( 'li' ).first().trigger( 'click' );
			return;
		}
	
		$( '.download_method li' ).addClass( 'disabled-choice' );
	
		// Add disabled-choice to all applicable download_methods
		$('.download_method li').each(function() {
			const liText = $(this).text().toLowerCase().trim(); 
			if ( download_methods.includes(liText) ) {
				$(this).removeClass('disabled-choice');
			}
		});
	
		$( '.download_method li.disabled-choice' ).removeClass( 'selected' );
	
		// Check if download method is visible, but no option is yet chosen
		if ( $( '.yourselection .download_method.select:not(.hide)').length > 0 && $( '.yourselection .download_method .selected' ).length == 0 ) {
			// select first one and return
			$( '.yourselection .download_method li:not(.disabled-choice)' ).first().click();
			return;
		}
	
		if ( $( '.yourselection .download_method.select:not(.hide)').length ) {
			configurables = configurables.filter( function ( item ) {
				return item.download_method.toLowerCase() == download_method.toLowerCase();
			});
			configurablesMinusArchitecture = configurablesMinusArchitecture.filter( function ( item ) {
				return item.download_method.toLowerCase() == download_method.toLowerCase();
			});
		}
	
		// Check if Architecture is visible, but no option is chosen
		if ( $( '.yourselection .architecture.select:not(.hide)').length > 0 && $( '.yourselection .architecture .selected' ).length == 0 ) {
			// select first one and return
			$( '.yourselection .architecture li:first-child' ).click();
			return;
		}
	
		// Make only possible architectures selectable
		if ( $( '.architecture.hide' ).length == 0 ) {
	
			
			$( 'ul.architecture li' ).addClass( 'disabled-choice' );
	
			for ( var i in configurablesMinusArchitecture ) {
				$( 'ul.architecture li' ).each( function() {
					if ( $( this ).text().toLowerCase() == configurablesMinusArchitecture[i].architecture.toLowerCase() ) {
						$(this).removeClass( 'disabled-choice' );
					}
				} );
			}
			
		}
		
		// Check architecture options and if current selection is universal
		const allAreUniversal = configurables.length > 0 && configurables.every(item => item.architecture.toLowerCase() === 'universal');
		if (allAreUniversal) {
			
			sectionsToHide.push('architecture');
			$('.architecture .info').show();
			
		} else {
			
			configurables = configurables.filter(function(item) {
				return (
				  item.architecture.toLowerCase() === architecture.toLowerCase()
				  || item.architecture.toLowerCase() === 'universal'
				);
				
			});
			
			$('.architecture .info').hide();
		}
		
		hideSections( sectionsToHide.join(',') );
		
		// Check if SHA512 is available
		function sha512Exists(config) {
		  return config.sha_512;
		}
	
		// If platform.select has .hide class, then show .info in it, otherwise hide .info
		if ( $( '.yourselection .platform.select.hide').length > 0 ) {
			$( '.yourselection .platform .info' ).show();
		} else {
			$( '.yourselection .platform .info' ).hide();
		}
	
		// Load in the Installation Instructions
		if ( configurables[0].installation_code ) {
			$( '.installation.output' ).show()
			$( '.installation.output .result code' ).html( simpleCodeHighlight( replaceHtmlEntities( configurables[0].installation_code ) ) );
		} else {
			$( '.installation.output' ).hide()
		}
	
		if ( configurables[0].usage_example ) {
			$( '.example.output' ).show();
			$( '.example code' ).html( simpleCodeHighlight( replaceHtmlEntities( configurables[0].usage_example ) ) );
		} else {
			$( '.example.output' ).hide();
		}
	
		if (configurables[0].link) {
			$('.link.output').show();
			let linkHtml = '<a href="' + configurables[0].link + '">' + configurables[0].link + '</a>';
			if (sha512Exists(configurables[0])) {
				linkHtml += ' <span class="sha512_btn">SHA-512</span>';
			}
			$('.link.output .result').html(linkHtml);
		} else {
			$('.link.output').hide();
		}
		
		if (sha512Exists(configurables[0])) {
			$('.sha512.output .result').html(configurables[0].sha_512);
		} else {
			$('.sha512.output').hide();
		}
	
		if ( configurables[0].note ) {
			$( '.note.output' ).show()
			$( '.note.output .result' ).html( configurables[0].note );
		} else {
			$( '.note.output' ).hide();
		}
		
		
	}
	
	evaluation();
	$('body.installation .yourselection .select li').click(function(){
		$( this ).addClass( 'selected' ).siblings( '.selected' ).removeClass( 'selected' );
		evaluation();
	});
	
	if( $('body.installation .yourselection').length != 0 ) {
		evaluation();
	}
	
	if( $('body.installation').length ){
		setTimeout(function() {
			evaluation();
		}, 100);
	}
	
	if ($('.yourselection > .select').length) {
		function setQueryString() {
			const urlSearchP = new URLSearchParams();
	
			$('.yourselection > .select').each(function () {
				if (!$(this).hasClass('inactive') && $(this).find('.selected').length) {
					const queryParam = $(this).data('select');
					const selected = $(this).find('.selected').data('id').replace('.', '');
					urlSearchP.set(queryParam, selected);
				}
			});
	
			// Get the current URL and append the new query parameters
			const currentURL = window.location.href;
			const newURL = new URL(currentURL);
			newURL.search = urlSearchP.toString();
	
			// Update the URL with the new query parameters
			window.history.pushState({}, '', newURL.toString());
		}
	
		function handleQueryParameters() {
			const urlSearchParams = new URLSearchParams(window.location.search);
			urlSearchParams.forEach(function(value, key) {
				const parentWrapper = $('[data-select="' + key + '"]');
				parentWrapper.find('.selected').removeClass('selected');
				parentWrapper.find('[data-id=".' + value + '"]').addClass('selected')
			});
			evaluation();
		}
	
		if ( window.location.search.length ) {
			handleQueryParameters();
		} else {
			setQueryString();
		}
		$(document).on('click', '.yourselection > .select li', setQueryString)
		window.addEventListener('popstate', handleQueryParameters);
	
	}
	
	setTimeout(function() {
		if (!window.location.search.length) {
			$('.platform li').removeClass('selected');
			$(`.platform li[data-id=".${OSdatid}"]`).addClass('selected');
			evaluation();
		}
	}, 100);

});

$(document).on('click', '.sha512_btn', function(e) {
	e.preventDefault();
	$(this).toggleClass('active');
	if ($(this).hasClass('active')) {
		$('.sha512.output').css('display', 'flex');
	} else {
		$('.sha512.output').hide();
	}
});