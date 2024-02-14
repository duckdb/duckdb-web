$(document).ready(function(){
	
	if (window.location.hash) {
		var hash = window.location.hash;
		if ($(hash).length) {
			$('html, body').animate({
				scrollTop: $(hash).offset().top-130
			}, 300, 'swing');
			if( $('.frequentlyaskedquestions').length ){
				$('h3'+hash).toggleClass('open');
				$('h3'+hash).next('p').slideToggle();
			}
		}
	}
	
	var windowWidth = $( window ).width();
	
	// Simple detect OS 
    if($('#quickinstall').length != 0 || $('.yourselection').length !=0 ){
		var OSName="Unknown OS";
		var OSdatid="Unknown OS";
		if (navigator.appVersion.indexOf("Win")!=-1) { OSName="Windows"; OSdatid="win" };
		if (navigator.appVersion.indexOf("Mac")!=-1) { OSName="macOS"; OSdatid="macos" };
		if (navigator.appVersion.indexOf("X11")!=-1) { OSName="UNIX"; OSdatid="linux" };
		if (navigator.appVersion.indexOf("Linux")!=-1) { OSName="Linux"; OSdatid="linux"};
		$('.systemdetected').html('System detected: '+OSName);
		/*$('.ver-cplusplus').not(OSdatid).remove()
		$('.ver-cli').not(OSdatid).remove()
		$('.ver-odbc').not(OSdatid).remove()*/
	}
	
	// Installation instructions on landingpage
	var landingpageevaluation = function(environment){
		if( environment == "odbc" || environment == "cli"){
			var result = $('section.hidden .quick-installation div[data-install="'+ environment +' '+ OSdatid +'"]').html();
		} else {
			var result = $('section.hidden .quick-installation div[data-install="'+ environment +'"]').html();
		}
		$('.install .result').html(result);
	}
	$('#quickinstall .environment ul li').click(function(){
		var environment = $(this).attr("data-id");
		$('#quickinstall .environment ul li.active').removeClass('active');
		$(this).addClass('active');
		landingpageevaluation(environment);
		console.log(environment)
	});
	$('body.landing .environmentselect').on('change', function() {
		landingpageevaluation(this.value);
	});
	var environment = $('#quickinstall .environment ul li.active').attr("data-id");
	landingpageevaluation(environment);
	
	
	// Get URL Parameter
	var getUrlParameter = function getUrlParameter(sParam) {
	    var sPageURL = window.location.search.substring(1),
	        sURLVariables = sPageURL.split('&'),
	        sParameterName,
	        i;
	
	    for (i = 0; i < sURLVariables.length; i++) {
	        sParameterName = sURLVariables[i].split('=');
	
	        if (sParameterName[0] === sParam) {
	            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
	        }
	    }
	};
	
	
	// Installation Selection
	var userSelection = {version: "", environment: "", pack: "", platform: ""};
	var classList = "";
	
	var evaluation = function(){
		
		var versionSelection = $('.yourselection ul.version li.selected').attr('data-id');
		if(versionSelection){ userSelection.version = versionSelection; }
		
		if( $("body.installation .environment.select .onlymobile").is(":visible") ){
			var environmentSelection = $('body.installation .environmentselect').val();
		} else {
			var environmentSelection = $('.yourselection ul.environment li.selected').attr('data-id');
		}
		if(environmentSelection){ userSelection.environment = environmentSelection; }
		
		var packSelection = $('.yourselection ul.pack li.selected').attr('data-id');
		if(packSelection){ userSelection.pack = packSelection; }
		
		var platfromSelection = $('.yourselection ul.platform li.selected').attr('data-id');
		if(platfromSelection){ userSelection.platform = platfromSelection; }
		

		if ( userSelection.environment == ".cplusplus" || userSelection.environment == ".cli" || userSelection.environment == ".odbc"){
			$('.installer.select, .platform.select').removeClass('inactive');
		} else {
			$('.installer.select, .platform.select').addClass('inactive');
			$('.installer.select ul li.selected, .platform.select ul li.selected').removeClass('selected');
			userSelection.pack = "";
			userSelection.platform = "";
		}

		if ( (userSelection.environment == ".cplusplus" || userSelection.environment == ".cli" || userSelection.environment == ".odbc") && userSelection.pack == ".source" ) {
			$('.platform.select').addClass('inactive');
			$('.platform.select ul li.selected').removeClass('selected');	
			userSelection.platform = "";
		}
		if ( (userSelection.environment == ".cplusplus" || userSelection.environment == ".cli" || userSelection.environment == ".odbc") && $('.installer.select ul li.selected').length == 0){
			$('.installer.select ul li[data-id=".binary"').addClass('selected');
			$('.platform.select ul li[data-id="'+OSdatid+'"').addClass('selected');
			userSelection.pack = ".binary";
			userSelection.platform = OSdatid;
		}
		
		var classList = userSelection.version + userSelection.environment + userSelection.pack + userSelection.platform;
		var result = $('.possibleresults div'+classList).html();
		$('.installation.output .result').html(result);

		var exampleResult = $('.possibleresults .example'+userSelection.environment).html();
		$('.example.output .result').html(exampleResult);

	}
	
	$('body.installation .yourselection .select li').click(function(){
		$(this).siblings('.selected').removeClass('selected');
		$(this).addClass('selected');
		evaluation();
	});
	
	if($('body.installation .yourselection').length != 0){
		var environment = "."+getUrlParameter('environment');
		if (environment !== '.undefined'){
			$('.yourselection ul.environment li.selected').removeClass('selected')
			$('.yourselection ul.environment li[data-id="'+environment+'"]').addClass('selected')
			evaluation();
		}
		var platform = "."+getUrlParameter('platform');
		if (platform == '.undefined'){
			$('.yourselection ul.platform li.selected').removeClass('selected')
			$('.yourselection ul.platform li[data-id=".'+OSdatid+'"]').addClass('selected')
			evaluation();
		}
	}
	$('body.installation .environmentselect').on('change', function() {
		evaluation();
	});
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
		}
	
		if ( window.location.search.length ) {
			handleQueryParameters();
		} else {
			setQueryString();
		}
		$(document).on('click', '.yourselection > .select li', setQueryString)
		window.addEventListener('popstate', handleQueryParameters);
	
	}
	

	if($('.archivedposts').length != 0){ // If Archive Page
		var year = getUrlParameter('year');
		var month = getUrlParameter('month');
		$('.postpreview').hide();
		$('.postpreview[data-year="'+year+'"][data-month="'+month+'"]').show();
		
		$('.collapse.show').removeClass('show');
		$('.card-header[data-year="'+year+'"]').next('.collapse ').addClass('show');
		$('.list-group a[data-year="'+year+'"][data-month="'+month+'"]').addClass('selected');
	}
	if($('.newsarchive').length != 0){ // If general Blog Page
		$('.archivesAccordian .card-header').click(function(){
			$(this).next('.collapse').slideToggle();
			$(this).children('.theyear').toggleClass('opened');
		})
	}

	// Sidenavigation Documentation
	$('.sidenavigation .hasSub').click(function(){
		$(this).next('ul').slideToggle();
	});
	   
    
    // arrows in menu 
    $('.sidenavigation .hasSub').click(function(){
	   $(this).toggleClass('opened'); 
    });
    // only docu or benchmarking can be opened at once
    $('.sidenavigation li.benchmarking').click(function(){
	    $('.sidenavigation li.documentation.opened').toggleClass('opened').next('ul').slideToggle();
    });
    $('.sidenavigation li.documentation').click(function(){
	    $('.sidenavigation li.benchmarking.opened').toggleClass('opened').next('ul').slideToggle();
    })
    if($('li.hasSub.opened.benchmarking').length != 0){
	    $('.sidenavigation li.documentation.opened').toggleClass('opened').next('ul').hide();
    }
    
	
	// Same Page Anchor Scroll Navigation
	$('a[href*="#"]')
    .not('[href="#"]')
    .not('[href="#0"]')
    .click(function(event) {
      if (
        location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
        &&
        location.hostname == this.hostname
      ) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');

        if (target.length) {
          // event.preventDefault();
          $('html, body').animate({
            scrollTop: target.offset().top-135
          }, 1000 );
        }
      }
    });
    
    
    // FAQs
    $('.wrap.frequentlyaskedquestions #main_content_wrap h1, .wrap.frequentlyaskedquestions #main_content_wrap h2, .wrap.frequentlyaskedquestions #main_content_wrap h3').click(function(){
	    $(this).toggleClass('open');
	    $(this).next('p').slideToggle();
    });
    
    
    // Mobile Menu
    var hamburgers = document.querySelectorAll(".hamburger");
    if ($('.hamburger').length > 0) {
		$('.hamburger').click(function(){
			if ($('body').hasClass('documentation') ){
			    $(this).toggleClass('is-active');
			    $('div.sidenavigation').toggleClass('slidein');
				$('body.documentation main .wrap').toggleClass('inactive');
				/*if ( $('body').hasClass('documentation') ){
					toggleMobileSearchIcon();
				}*/
			} else {
				$(this).toggleClass('is-active');
				$('.landingmenu nav').toggleClass('slidein');
				$('body main').toggleClass('inactive');	
			}
		})
	
    }
    
    
    // Scroll Top Button 
    $('.scrolltop').click(function(){
	    $("html, body").animate({ scrollTop: 0 }, 600, 'swing');
	    return false;
	});
    
	
	// Header Animation
	if( $('.hamburger').is(':visible') ){
		var animationpath = "/js/duckdbanimation_search.json"
	} else {
		var animationpath = "/js/duckdbanimation.json"
	}
	let duckDBicon = document.getElementById('duckdbanimation');	
    let animationduckDBicon = lottie.loadAnimation({
            container: duckDBicon,
            renderer: 'svg',
            loop: false,
            autoplay: false,
            path: animationpath
    });
    
	if( !$('.hamburger').is(':visible') ){
		$('#duckdbanimation, .duckdbhome img.downloadlogo').mouseenter(function() {
			animationduckDBicon.play();
			animationduckDBicon.setDirection(1)
		})
		$('#duckdbanimation, .duckdbhome img.downloadlogo').mouseleave(function() {
			animationduckDBicon.play();
			animationduckDBicon.setDirection(-1)
		})
	}
	
	if ($('.wrap.livedemo').length =! 0){
		lottie.loadAnimation({
		  container: document.getElementById('loading-spinner'), 
		  renderer: 'svg',
		  loop: true,
		  autoplay: true,
		  path: "/js/duckdbanimationloop.json"
		});
	}
	
	
	// Landingpage Animation
	if( $("body.landing").length != 0 ){
		let duckDBcircled = document.getElementById('duckdbdanimationcircled');	
	    let animationduckDBcircled = lottie.loadAnimation({
	            container: duckDBcircled,
	            renderer: 'svg',
	            loop: false,
	            autoplay: false,
	            path: "/js/duckdbanimation-circle.json"
	    });
		$('#duckdbdanimationcircled').mouseenter(function() {
			animationduckDBcircled.play();
			animationduckDBcircled.setDirection(1)
		})
		$('#duckdbdanimationcircled').mouseleave(function() {
			animationduckDBcircled.play();
			animationduckDBcircled.setDirection(-1)
		})
	}
	
	// Appending "Note" to Blockquote
	$('body.documentation #main_content_wrap blockquote').each(function() {
		$(this).prepend("<h4>Note</h4>");
	});
	
	
	// Appending Content-List of Overview-Pages
	if (window.location.href.indexOf("/overview") > -1) {
		pathname = window.location.pathname.replace(/\.html$/, '')
		const selector = 'li.opened a[href="' + pathname + '"]';
		clonedUL = $(selector).parent().parent().clone();
		clonedUL.find(selector).parent().remove();
		clonedUL.find('ul').show();
	    $('#main_content_wrap').append(clonedUL);
	}
	
	// Appending Content-List of Documentation
	if ( $('.wrap.documentation') != 0 ) {
	    contentlist = $('ul.sidenav').clone()
	    $('#docusitemaphere').append(contentlist).find("ul").removeAttr("style")
	}
	
	// Add class-name to external Links
	$('a').filter(function() {
		return this.hostname && this.hostname !== location.hostname;
	}).addClass("externallink").attr('target','_blank');
	$('.headercontent a.externallink, .mainlinks a.externallink').removeClass('externallink'); // Remove Class from header elements
	$('.footercontent a.externallink').removeClass('externallink'); // Remove Class from footer elements
	$('table a.externallink:contains(GitHub)').removeClass('externallink').addClass('nobg'); // Remove Class from GitHub Links in Table
	$('.supporterboard a.externallink').removeClass('externallink').addClass('nobg'); // Remove Class from GitHub Links in Table
	
	// FOUNDATION PAGE SCRIPTS
	if($('body').hasClass('foundation') && $('section.form').length){
		var hash = window.location.hash.replace('#', '');
		if( hash.length ){
			$('div.select .select-text').val(hash);
		}
		
		// AJAX FORM SEND
		$("#ajaxForm").submit(function(e){
			e.preventDefault();
			var action = $(this).attr("action");
			
			$('#ajaxForm button[type="submit"]').hide();
			$('#ajaxForm .lds-ellipsis').fadeIn();
			
			$.ajax({
				type: "POST",
				url: action,
				crossDomain: true,
				data: new FormData(this),
				dataType: "json",
				processData: false,
				contentType: false,
				headers: {
					"Accept": "application/json"
				}
			}).done(function() {
				$('#ajaxForm').addClass('inactive');
				$('#ajaxForm .lds-ellipsis').hide();
				$('.success').addClass('is-active');
			}).fail(function() {
				alert('An error occurred! Please try again later.');
				$('#ajaxForm button[type="submit"]').show();
				$('#ajaxForm .lds-ellipsis').hide();
			});
			
		});
	
	}
	
	
	// CHANGE DOC VERSION
	/*
	$('.versionsidebar ul li').click(function(){
		var clickedversion = $(this).text();
		var docversion = getUrlParameter('ver');
		if( docversion ){
			var pathname = window.location.pathname.split("/docs/archive/"+docversion);
		} else {
			var pathname = window.location.pathname.split("/docs");
		}
		
		if( $(this).hasClass('latest') ){
			var versionurl = "/docs"+pathname[1]
		} else {
			var versionurl = "/docs/archive/"+clickedversion+pathname[1]+"?ver="+clickedversion;
		}
	})
	*/
	
	// VERSION FIX ON MOBILE
	$('.headlinebar .version').click(function(){
		$('.versionsidebar').toggleClass('active');
	})
	
	
	
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
	var base_url = window.location.origin;
	var resultSelected;
	/*
	var toggleMobileSearchIcon = function(){
		if( $('.hamburger').hasClass('is-active') ){
			animationduckDBicon.play();
			animationduckDBicon.setDirection(1);
		} else {
			animationduckDBicon.play();
			animationduckDBicon.setDirection(-1);
		}
	}
	*/
	var toggleSearch = function(){
		if( $('body').hasClass('search') ){
			$('.searchoverlay').removeClass('active');
			$('body').removeClass('search');
		} else {
			$('.searchoverlay').addClass('active');
			$('body').addClass('search');
			$( ".searchoverlay form input" ).focus();
		}
	}
	$(window).keydown(function (e){
		// close Search on ESC
		if( ( e.which === 27 ) && $('body').hasClass('search') ){
			$('.searchoverlay').removeClass('active');
			$('body').removeClass('search');
		}
		// open search on cmd/ctrl + k
		if ( e.metaKey && ( e.which === 75 ) || e.ctrlKey && ( e.which === 75 ) ) {
			if( $('body').hasClass('documentation') ){
				toggleSearch();
			}
		}
		// de-focus input when on enter or follow the result-link
		if ( e.which === 13  && $('body').hasClass('search') ){
			if( $('.search_result.selected').length ){
				var link = $('.search_result.selected').find('a').attr('href');
				document.location.href = link
			} else {
				$( ".searchoverlay form input" ).blur();
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
	
	$('nav .search_icon').click(function(){
		toggleSearch();
	});
	$('.searchoverlay').click(function(e){
		if (e.target !== this)
			return;
		toggleSearch();
	});
	$('.searchoverlay .empty_input').click(function(){
		$(".searchoverlay form input").val('').focus();
		$("#search_results").empty();
	})
	if( $('.hamburger').is(':visible') ){
		$('.search_icon').click(function(e){
			if ( $('.hamburger').hasClass('is-active') ){
				if( $('body').hasClass('search') ){
					$('body.documentation main .wrap.inactive').removeClass('inactive');
					$('.sidenavigation').fadeOut();
				} else {
					$('.sidenavigation').fadeIn();
					$('body.documentation main .wrap').addClass('inactive');
				}
			}
		})
	}
	$('.hamburger').click(function(){
		if( !$(this).hasClass('is-active') && $('body').hasClass('search') ){
			toggleSearch();
			$('.sidenavigation').fadeIn();
			$('body.documentation main .wrap.inactive').removeClass('inactive');
		}
	});
	
	// ADDING LINES TO CODE FIELDS IF DEFINED
	var addLineNumbers = function(){
		if( $('.window .content.haslines').length ){
			$('.window .content.haslines').each(function(){
				var height = $(this).find('pre').height()
				var fontSize = $(this).find('pre').css('font-size');
				var lineHeight = 17;//Math.floor(parseInt(fontSize.replace('px','')) * 1.2);
				var lines = Math.ceil(height / lineHeight) + 1
				var linenumbers = '';
				for (i = 1; i < lines; i++) {
					linenumbers += i + '<br>'
				}
				$(this).find('.lines').html(linenumbers);
			})
		}
	}
	addLineNumbers();

	
	// GENERAL ACCORDION FOLDOUT
	if( $('.accordion').length ){
		$('.foldout').click(function(){
			$(this).toggleClass('active').find('.content').slideToggle();
		})
	}
	
	// STARTPAGE EXAMPLE CODE WINDOW
	var updateExample = function(){
		var exampleSelection = $('#example-select').find(":selected").val();
		var languageSelection = $('.demo.window ul.lang li.active').attr('data-language');
		var exampleCode = $('.examples.hero-demo').find('div[data-language='+languageSelection+'][data-example='+exampleSelection+']').html();
		var buttonTxt = $('.examples.hero-demo').find('div[data-language='+languageSelection+'][data-example='+exampleSelection+']').attr('data-buttontxt');
		var buttonUrl = $('.examples.hero-demo').find('div[data-language='+languageSelection+'][data-example='+exampleSelection+']').attr('data-buttonurl');
		//console.log("Example: " + exampleSelection + " Language: " + languageSelection);
		//console.log("Buttontext: " + buttonTxt);
		$('.demo.window .content .code').html(exampleCode);
		addLineNumbers();
		if( buttonTxt.length ){
			$('.demo.window .bottombar a.livedemo').text(buttonTxt);
			$('.demo.window .bottombar a.livedemo').attr('href', buttonUrl);
		}
	}
	
	if( $('section.welcome').length ){
		$('.demo.window ul.lang li').click(function(){
			$('.demo.window ul.lang li.active').removeClass('active');
			$(this).addClass('active');
			var languageChange = $('.demo.window ul.lang li.active').attr('data-language');
			var dropdown = $('.dropdown.hero-demo').find('div[data-language='+languageChange+']').html();
			$('.demo.window .bottombar #example-select').html(dropdown);
			updateExample();
		})
		$('#example-select').on('change', function() {
			updateExample();
		});
	}
	
});
