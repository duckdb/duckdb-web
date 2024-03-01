$(document).ready(function(){
	
	if (window.location.hash) {
		var hash = window.location.hash;
		if ($(hash).length) {
			$('html, body').animate({
				scrollTop: $(hash).offset().top-90
			}, 300, 'swing');
			if( $('.frequentlyaskedquestions').length ){
				//console.log($('h3'+hash).parent('.qa-wrap'))
				$('h3'+hash).parent('.qa-wrap').addClass('open');
				$('h3'+hash).parent('.qa-wrap').find('.answer').slideToggle(300);
			}
		}
	}
	
	var windowWidth = $( window ).width();
	
	// Simple detect OS 
    if($('#quickinstall').length != 0 || $('.yourselection').length !=0 ){
	}
	
	
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
	return "undefined";
	};
	
	// Docs Installation Functions 
	function showAllSections() {
		$('.yourselection .hide').removeClass('hide');
		$('.yourselection .select ul li.inactive').removeClass('inactive')
	}
	
	function hideSections(sections) {
		if ( sections !== undefined ) {
			sections.split(',').forEach(section => {
				const $container = $(`.select[data-select="${section.trim()}"]`);
				// console.log($container)
				$container.addClass('hide')
				$container.find('.selected').removeClass('selected');
			});
		}
	}
	
	// Docs Installation Selection
	var userSelection = { version: "", environment: "", pack: "", platform: "", architecture: "", download_method: "" };
	var classList = "";
	
	var OSName="Unknown OS";
	var OSdatid="Unknown OS";
	if (navigator.appVersion.indexOf("Win")!=-1) { OSName="Windows"; OSdatid="win" };
	if (navigator.appVersion.indexOf("Mac")!=-1) { OSName="macOS"; OSdatid="macos" };
	if (navigator.appVersion.indexOf("X11")!=-1) { OSName="UNIX"; OSdatid="linux" };
	if (navigator.appVersion.indexOf("Linux")!=-1) { OSName="Linux"; OSdatid="linux"};
	$('.systemdetected').html('System detected: '+OSName);

	var evaluation = function () {
		showAllSections();
	
		if (userSelection.environment == "")
			userSelection.environment=".cli";
		if (userSelection.version == "")
			userSelection.version=".latest";

		if ((userSelection.environment == ".cli" || userSelection.environment == ".odbc") && $('.installer.select ul li.selected').length == 0) {
			if (userSelection.download_method == "" || userSelection.download_method == undefined)
				userSelection.download_method = ".package_manager";
			if (userSelection.platform == "" || userSelection.platform == undefined)
				userSelection.platform = "." + OSdatid;
		}
		else if (userSelection.environment == ".cplusplus") {
			if (userSelection.platform == "" || userSelection.platform == undefined)
				userSelection.platform = "." + OSdatid;
		}
		else if (userSelection.environment == ".java") {
			if (userSelection.download_method == "" || userSelection.download_method == undefined)
				userSelection.download_method = ".package_manager";
		}
		var currSelection = userSelection;
		if (userSelection.platform == ".macos")
			currSelection.architecture = ""
		if ((userSelection.environment == ".cli") && $('.installer.select ul li.selected').length == 0) {
		} else if (userSelection.environment == ".cplusplus") {
			currSelection.download_method = ""
		} else if (userSelection.environment == ".odbc") {
			currSelection.download_method = ".direct"
		} else if (userSelection.environment == ".java") {
			currSelection.platform = ""
			currSelection.architecture = ""
		} else {
			currSelection.download_method = ""
			currSelection.platform = ""
			currSelection.architecture = ""
		}	
		
		if (currSelection.version != "" && currSelection.version != undefined){
			$('.yourselection ul.version li.selected').removeClass('selected')
			$('.yourselection ul.version li[data-id="'+currSelection.version+'"]').addClass('selected')
		}
		if (currSelection.environment != "" && currSelection.environment != undefined){
			$('.yourselection ul.environment li.selected').removeClass('selected')
			$('.yourselection ul.environment li[data-id="'+currSelection.environment+'"]').addClass('selected')
		}
		if (currSelection.platform != "" && currSelection.platform != undefined){
			$('.yourselection ul.platform li.selected').removeClass('selected')
			$('.yourselection ul.platform li[data-id="'+currSelection.platform+'"]').addClass('selected')
		}
		if (currSelection.architecture != "" && currSelection.architecture != undefined){
			$('.yourselection ul.architecture li.selected').removeClass('selected')
			$('.yourselection ul.architecture li[data-id="'+currSelection.architecture+'"]').addClass('selected')
		}
		if (currSelection.download_method != "" && currSelection.download_method != undefined){
			$('.yourselection ul.download_method li.selected').removeClass('selected')
			$('.yourselection ul.download_method li[data-id="'+currSelection.download_method+'"]').addClass('selected')
		}
		$('.yourselection .select').each(function() {
			const $self = $(this);
			const $selfClass = $(this).data('select')
			const $selectedElm = $self.find('.selected');
			if ( $selectedElm.length ) {
				hideSections($selectedElm.data('hide-section'))
				currSelection[$selfClass] = $selectedElm.data('id')
	
				const deactivateTabs = $selectedElm.data('deactivate-tabs');
				if ( deactivateTabs !== undefined ) {
					deactivateTabs.split(',').forEach(function(deactivateTab) {
						const tab = deactivateTab.split(' ')
						$(`${tab[0]} [data-id="${tab[1]}"]`).addClass('inactive').removeClass('selected')
					});
				}
	
				const preselectTabs = $selectedElm.data('preselect-tabs');
				if ( preselectTabs !== undefined ) {
					preselectTabs.split(',').forEach(function(preselectTab) {
						const tab = preselectTab.split(' ')
						$(`${tab[0]} [data-id="${tab[1]}"]`).addClass('selected')
						userSelection[tab[0].replace('.', '')] = tab[1].replace('.', '')
						
						setQueryString();
					});
				}
			}
		})

		var classList = currSelection.version + currSelection.environment + currSelection.pack + currSelection.platform + currSelection.architecture + currSelection.download_method;

		var result = $('.possibleresults div' + classList).html();
		$('.installation.output .result').html(result);
	
		var exampleResult = $('.possibleresults .example' + currSelection.environment).html();
		$('.example.output .result').html(exampleResult);
	
	}
	evaluation();
	$('body.installation .yourselection .select li').click(function(){
		userSelection[this.parentNode.className] = this.getAttribute("data-id");
		evaluation();
	});
	
	if($('body.installation .yourselection').length != 0){
		evaluation();
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
            scrollTop: target.offset().top-90
          }, 1000 );
        }
      }
    });
    
    
    // FAQs
	$('.qa-wrap').click(function(){
		$(this).toggleClass('open');
		$(this).find('.answer').slideToggle(400);
	})
	
    
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
	
	
	// Appending Content-List of Overview-Pages
	const pathname = window.location.pathname.replace(/\.html$/, '');
	if (window.location.href.includes("/overview")) {
		const selector = `li.opened a[href="${pathname}"]`;
		const clonedUL = $(selector).parent().parent().clone();
		clonedUL.find(selector).parent().remove();
		clonedUL.find('ul').show();
		$('#main_content_wrap .index').append(clonedUL);
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
	

	$('.headlinebar .version').click(function(){
		$(this).toggleClass('active');
		$(this).find('.versionsidebar').slideToggle();
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
					$('.hamburger').removeClass('is-active');
					$('body.documentation main .wrap.inactive').removeClass('inactive');
					$('.sidenavigation.slidein').removeClass('slidein');
					$('nav.slidein').removeClass('slidein');
				} else {
					$('.sidenavigation').addClass('slidein')
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
