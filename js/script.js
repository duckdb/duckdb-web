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
	
	
	/** DARK MODE SWITCH */
	var isDark = document.documentElement.classList.contains('darkmode');
	$('.versionselect .mode').attr('data-mode', isDark ? 'light' : 'dark').find('.name').text(isDark ? 'Light Mode' : 'Dark Mode');

	setTimeout(() => {
		document.documentElement.classList.remove('disable-transitions');
	}, 300);
	
	$('.versionselect .mode').click(function() {
		var isDark = $(this).attr('data-mode') === 'dark';
		$('html').toggleClass('darkmode', isDark);
		$(this).attr('data-mode', isDark ? 'light' : 'dark').find('.name').text(isDark ? 'Light Mode' : 'Dark Mode');
		localStorage.setItem('mode', isDark ? 'dark' : 'light');
		document.documentElement.classList.add('disable-transitions');
		setTimeout(() => {
			document.documentElement.classList.remove('disable-transitions');
		}, 300);
	});

	
	
	// Simple detect OS 
	var OSName="Unknown OS";
	var OSdatid="Unknown OS";
	if (navigator.appVersion.indexOf("Win")!=-1) { OSName="Windows"; OSdatid="win" };
	if (navigator.appVersion.indexOf("Mac")!=-1) { OSName="macOS"; OSdatid="macos" };
	if (navigator.appVersion.indexOf("X11")!=-1) { OSName="UNIX"; OSdatid="linux" };
	if (navigator.appVersion.indexOf("Linux")!=-1) { OSName="Linux"; OSdatid="linux"};
	$('.systemdetected').html('System detected: '+OSName);
	
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
	var scrollspeed = 1000;
	$('a[href*="#"]')
		.not('[href="#"]')
		.not('[href="#0"]')
		.click(function(event) {
			if ($(this).parent().hasClass('toc-entry')) {
				scrollspeed = 100;
			}
			if (
				location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') &&
				location.hostname == this.hostname
			) {
				var target = $(this.hash);
				target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
	
				if (target.length) {
					// event.preventDefault();
					$('html, body').animate({
						scrollTop: target.offset().top - 90
					}, scrollspeed);
				}
			}
		});

    
    // FAQs
	$('.qa-wrap').click(function(event) {
		if ($(event.target).is('a') && !$(event.target).parent().is('h3')) {
			return;
		}
		$(this).toggleClass('open');
		$(this).find('.answer').slideToggle(400);
	});
	$('.qa-wrap .answer a').click(function(event) {
		event.stopPropagation();
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
	/*
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
	*/
	
	// Landing Page Typewriter Animation
	if( $('.landing .type').length ){
		var $typeElement = $('.type');
		var strings = $typeElement.data('strings').split('|');
		var typewriter = new Typewriter($typeElement[0], {
			loop: true, 
			wrapperClassName: "typewrapper",
			cursorClassName: "typecursor",
			cursor: "|"
			//cursor: "⎪"
		});
		
		strings.forEach(function(str) {
			typewriter.typeString(str)
				.pauseFor(2500)
				.deleteAll();
		});
		
		typewriter.start();
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
		
		if( $(this).hasClass('stable') ){
			var versionurl = "/docs"+pathname[1]
		} else {
			var versionurl = "/docs/archive/"+clickedversion+pathname[1]+"?ver="+clickedversion;
		}
	})
	*/
	

	$('.headlinebar .version').click(function(){
		var $this = $(this);
		$this.toggleClass('active');
		$this.find('.versionsidebar').slideToggle(200);
		
		// MAKE IT SAME AS ON START PAGE
		var selectedVersion = $this.find('.selectedversion');
		var currentVersion = selectedVersion.attr('data-current');
	
		selectedVersion.text($this.hasClass('active') ? 'Select' : currentVersion);
	
		$this.find('.versionsidebar li').removeClass('current') 
			.filter(function() { 
				return $(this).text().trim() === currentVersion; 
			}).addClass('current');
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
	var base_url = window.location.origin;
	var resultSelected;
	if( OSdatid == "macos" && $('.sidenavigation').length ){
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
			$( ".searchoverlay form input" ).focus();
		}
	}
	$(window).keydown(function (e){
		// close Search on ESC
		if( ( e.which === 27 ) && $('body').hasClass('search') ){
			$('.searchoverlay').removeClass('active');
			$('body').removeClass('search');
		}
		
		if ( e.metaKey && ( e.which === 75 ) || e.ctrlKey && ( e.which === 75 ) ) {
			// open search on cmd/ctrl + k
			var isFirefox = typeof InstallTrigger !== 'undefined';
			if (isFirefox) {
				e.preventDefault();
			}
			if( $('body').hasClass('documentation') || $('body').hasClass('landing') ){
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
	$('.sidenavigation .opensearch').click(function(){
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
				var lineHeight = 18;//Math.floor(parseInt(fontSize.replace('px','')) * 1.2);
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
		//var exampleSelection = $('#example-select').find(":selected").val();
		var exampleSelection = $('#example-select ~ ul.select-options li.is-selected').attr('rel');
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

	// STARTPAGE INSTALLATION WINDOW
	var updateInstallation = function(){
		var exampleSelection = $('#example-select').find(":selected").val();
		var languageSelection = $('.demo.window ul.lang li.active').attr('data-language');
		var exampleCode = $('.examples.hero-demo').find('div[data-install='+languageSelection+'][data-install='+exampleSelection+']').html();
		var buttonTxt = $('.examples.hero-demo').find('div[data-install='+languageSelection+'][data-install='+exampleSelection+']').attr('data-buttontxt');
		var buttonUrl = $('.examples.hero-demo').find('div[data-install='+languageSelection+'][data-install='+exampleSelection+']').attr('data-buttonurl');
		//console.log("Example: " + exampleSelection + " Language: " + languageSelection);
		//console.log("Buttontext: " + buttonTxt);
		$('.demo.window .content .code').html(exampleCode);
	}

	if( $('section.welcome').length ){
		$('.demo.window .topbar > ul.lang > li').click(function(){
			$('.demo.window .topbar > ul.lang > li.active').removeClass('active');
			$(this).addClass('active');
			var languageChange = $(this).attr('data-language');
			var dropdown = $('.dropdown.hero-demo').find('div[data-language='+languageChange+']').html();
			$('.demo.window .bottombar #example-select').empty().html(dropdown); // Leere die Select-Box und füge die neuen Optionen ein
			
			$('.select-styled, .select-options').remove();
			generateSelectBoxes(); 
			updateExample();
		});

		$('#example-select').on('change', function() {
			updateExample();
		});
	}

	/** QUICK INSTALLATION ON HOME PAGE */
	if ($('section#quickinstall').length) {
		function displayInstallation() {
			var activeClient = $('.install > .window > .environment > ul > li.active').attr('data-client');
			var installation = $('#quick-installation').find('div[data-install="' + activeClient + ' ' + OSdatid + '"]').html();
			if (installation === undefined) {
				installation = $('#quick-installation').find('div[data-install=' + activeClient + ']').html();
			}
			$('.result').html(installation);
		}
		$('.install > .window > .environment > ul > li').click(function() {
			$('.install > .window > .environment > ul > li.active').removeClass('active');
			$(this).addClass('active');
			displayInstallation();
		});
		setTimeout(function() {
			if ($('.install > .window > .environment > ul > li.active').length === 0) {
				$('.install > .window > .environment > ul > li:first').addClass('active');
			}
			displayInstallation();
		}, 500);
	}
	
	/** CUSTOM SELECT ON HOME **/
	var generateSelectBoxes = function(){   
		$('body.landing select').each(function() {
			var $this = $(this),
				numberOfOptions = $(this).children('option').length;
	
			$this.addClass('select-hidden');
			$this.after('<div class="select-styled">' + ($this.children('option:selected').text() || 'Select') + '</div>'); 
	
			var $styledSelect = $this.next('div.select-styled');
			var $list = $('<ul />', {
				'class': 'select-options'
			}).insertAfter($styledSelect);
	
			for (var i = 0; i < numberOfOptions; i++) {
				$('<li />', {
					text: $this.children('option').eq(i).text(),
					rel: $this.children('option').eq(i).val()
				}).appendTo($list);
				if ($this.children('option').eq(i).is(':selected')) {
					$('li[rel="' + $this.children('option').eq(i).val() + '"]').addClass('is-selected');
				}
			}
	
			var $listItems = $list.children('li');
	
			$styledSelect.click(function(e) {
				e.stopPropagation();
				$('div.select-styled.active').not(this).each(function() {
					$(this).removeClass('active').next('ul.select-options').hide();
				});
				$(this).toggleClass('active').next('ul.select-options').slideToggle(200); 
				if ($(this).hasClass('active')) {
					$(this).html('<span>Select</span>'); 
				} else {
					var selectedText = $this.children('option:selected').text() || 'Select';
					$(this).html(selectedText); 
				}
			});
	
			$listItems.click(function(e) {
				e.stopPropagation();
				var selectedText = $(this).text();
				$styledSelect.html(selectedText).removeClass('active');
				$this.val($(this).attr('rel'));
				$list.find('li.is-selected').removeClass('is-selected');
				$(this).addClass('is-selected');
				$list.hide();
				updateExample();
			});
	
			$(document).click(function() {
				$styledSelect.removeClass('active');
				$list.hide();
				var selectedText = $this.children('option:selected').text() || 'Select';
				$styledSelect.html(selectedText); 
			});
	
			$this.change(function() {
				var selectedText = $(this).children('option:selected').text() || 'Select';
				$styledSelect.html(selectedText); 
			});
		});
	}
	
	generateSelectBoxes();




	
	/** HIGHLIGHT TOC MENU **/
	if ( $('body').hasClass('documentation') ) {
		var headings = $('#main_content_wrap h1, #main_content_wrap h2');
		var tocEntries = $('.toc-entry');
	
		$(window).on('scroll', function() {
			var scrollPos = $(window).scrollTop() + 150; // top offset
			var documentHeight = $(document).height();
	
			headings.each(function(index, element) {
				var id = $(element).attr('id');
				var offset = $(element).offset().top;
	
				if (scrollPos >= offset) {
					tocEntries.removeClass('current');
					$('.toc-entry a[href="#' + id + '"]').parent().addClass('current');
				}
			});
	
			if (scrollPos + $(window).height() >= documentHeight - 20) {
				tocEntries.removeClass('current'); 
				$('.toc-entry:last').addClass('current'); 
			}
		});
	}
	
	/** HIGHLIGHT TOC MENU ON BLOG POSTS **/
	if ( $('.postcontent .toc_sidebar').length ){
		var headings = $('.singleentry h1, .singleentry h2,  .singleentry h3');
		var tocEntries = $('.toc-entry');
		
		$(window).on('scroll', function() {
			var scrollPos = $(window).scrollTop() + 150; // top offset
			var documentHeight = $(document).height();
		
			headings.each(function(index, element) {
				var id = $(element).attr('id');
				var offset = $(element).offset().top;
		
				if (scrollPos >= offset) {
					tocEntries.removeClass('current');
					$('.toc-entry a[href="#' + id + '"]').parent().addClass('current');
				}
			});
		
			if (scrollPos + $(window).height() >= documentHeight - 20) {
				tocEntries.removeClass('current'); 
				$('.toc-entry:last').addClass('current'); 
			}
		});
	}
	
	
	/** HIDE BANNER **/
	const showbanner = getWithExpiry("homeBanner");
	if(showbanner == false){
		$('.banner').css('display', 'none');
		if( $('body').hasClass('documentation') ){
			$('main').removeAttr('class');
		}
	} else {
		$('.banner').css('display', 'flex');
	}
	$('.banner .close').click(function(){
		setWithExpiry('homeBanner', false, 172800000); // 900000 = 15 min, 172800000 = 2 days
		$('.banner').slideUp(300);
		if( $('body').hasClass('documentation') ){
			$('main').removeAttr('class');
		} 
	});
	// setWithExpiry('homeBanner', '', -1); // deletes content
	
});
