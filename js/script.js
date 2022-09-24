$(document).ready(function(){
	
	var windowWidth = $( window ).width();
	
	// Simple detect OS 
    if($('#quickinstall').length != 0 || $('.yourselection').length !=0 ){
		var OSName="Unknown OS";
		var OSdatid="Unknown OS";
		if (navigator.appVersion.indexOf("Win")!=-1) { OSName="Windows"; OSdatid=".win" };
		if (navigator.appVersion.indexOf("Mac")!=-1) { OSName="macOS"; OSdatid=".macos" };
		if (navigator.appVersion.indexOf("X11")!=-1) { OSName="UNIX"; OSdatid=".linux" };
		if (navigator.appVersion.indexOf("Linux")!=-1) { OSName="Linux"; OSdatid=".linux"};
		$('.systemdetected').html('System detected: '+OSName);
		$('.ver-cplusplus').not(OSdatid).remove()
		$('.ver-cli').not(OSdatid).remove()
		$('.ver-odbc').not(OSdatid).remove()
	}
	
	// Installationshinweise Landingpage
	$('.environment ul li').click(function(){
		var environment = $(this).attr("data-id");
		$('.environment ul li.active').removeClass('active');
		$(this).addClass('active');
		var result = $('.install .hidden .'+environment).html();
		$('.install .result').html(result);		
	});
	
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
	var userSelection = {version: ".latest", environment: ".python", pack: "", platform: ""};
	var classList = "";
	
	var evaluation = function(){
		
		var versionSelection = $('.yourselection ul.version li.selected').attr('data-id');
		if(versionSelection){ userSelection.version = versionSelection; }
		
		var environmentSelection = $('.yourselection ul.environment li.selected').attr('data-id');
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
		if ( userSelection.version == ".master" && (userSelection.environment == ".cplusplus" || userSelection.environment == ".odbc") ) {
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
		$('.installartion.output .result').html(result);
		
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
	
	// Select Everything when Clicking on Result-Div
	function SelectText(element) {
	    var doc = document
	        , text = doc.getElementById(element)
	        , range, selection
	    ;    
	    if (doc.body.createTextRange) {
	        range = document.body.createTextRange();
	        range.moveToElementText(text);
	        range.select();
	    } else if (window.getSelection) {
	        selection = window.getSelection();        
	        range = document.createRange();
	        range.selectNodeContents(text);
	        selection.removeAllRanges();
	        selection.addRange(range);
	    }
	}
	$('.installartion.output .result').click(function(){
		SelectText('resultselection')
	})
	

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
      // On-page links
      if (
        location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
        &&
        location.hostname == this.hostname
      ) {
        // Figure out element to scroll to
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');

        if (target.length) {
          // Only prevent default if animation is actually gonna happen
          event.preventDefault();
          $('html, body').animate({
            scrollTop: target.offset().top
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
	let duckDBicon = document.getElementById('duckdbanimation');	
    let animationduckDBicon = lottie.loadAnimation({
            container: duckDBicon,
            renderer: 'svg',
            loop: false,
            autoplay: false,
            path: "/js/duckdbanimation.json"
    });
    
	$('#duckdbanimation, .duckdbhome img.downloadlogo').mouseenter(function() {
		animationduckDBicon.play();
		animationduckDBicon.setDirection(1)
	})
	
	if ($('.wrap.livedemo').length =! 0){
		lottie.loadAnimation({
		  container: document.getElementById('loading-spinner'), 
		  renderer: 'svg',
		  loop: true,
		  autoplay: true,
		  path: "/js/duckdbanimationloop.json"
		});
	}
	
	$('#duckdbanimation, .duckdbhome img.downloadlogo').mouseleave(function() {
		animationduckDBicon.play();
		animationduckDBicon.setDirection(-1)
	})
	
	
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
	if (window.location.href.indexOf("overview") > -1) {
	    //contentlist = $('li.opened ~ .parentnav li.active ~ li').clone();
	    // ontentlist = $('li.opened.'+expanded+' ~ .parentnav li.active ~ li').clone();
		var selector = 'li.opened a[href="' + window.location.pathname + '"]';
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
	$('.landingmenu .external a.externallink, .mainlinks a.externallink, .discord a.externallink').removeClass('externallink'); // Remove Class from header elements
	$('.footercontent a.externallink').removeClass('externallink'); // Remove Class from footer elements

	
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
	// CLOSE DISCORD BANNER ON HOME PAGE
	const showdiscord = getWithExpiry("discordBanner");
	if(showdiscord == false){
		$('.discord').css('display', 'none');
	} else {
		$('.discord').css('display', 'flex');
	}
	$('.discordclose').click(function(){
		setWithExpiry('discordBanner', false, 172800000); // 900000 = 15 min, 172800000 = 2 days
		//$('.discord').slideUp();
		$('.discord').animate({ height: 0 }, 300);
	});
	
});
