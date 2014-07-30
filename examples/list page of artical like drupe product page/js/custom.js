
jQuery.noConflict()(function($){
$(document).ready(function($) {
if ( $( '#cute-slider' ).length && jQuery() ) {
      var slider = new Cute.Slider();
		slider.setup("my-cute-slider" , "cute-slider");		
}


if ( $( '.grey-img' ).length && jQuery() ) {
 $(window).load(function(){
		
		// Fade in images so there isn't a color "pop" document load and then on window load
		$(".grey-img img").fadeIn(500);
		
		// clone image
		$('.grey-img img').each(function(){
			var el = $(this);
			el.css({"display":"relative"}).wrap("<div class='img_wrapper'>").clone().addClass('img_grayscale').insertBefore(el).queue(function(){
				var el = $(this);
				el.parent().css({"width":this.width,});
				el.dequeue();
			});
			this.src = grayscale(this.src);
		});
		
		// Fade image 
		$('.grey-img img').mouseover(function(){
			$(this).parent().find('img:first').stop().animate({opacity:1}, 1000);
		})
		$('.img_grayscale').mouseout(function(){
			$(this).stop().animate({opacity:0}, 1000);
		});		
	});
	
	// Grayscale w canvas method
	function grayscale(src){
		var canvas = document.createElement('canvas');
		var ctx = canvas.getContext('2d');
		var imgObj = new Image();
		imgObj.src = src;
		canvas.width = imgObj.width;
		canvas.height = imgObj.height; 
		ctx.drawImage(imgObj, 0, 0); 
		var imgPixels = ctx.getImageData(0, 0, canvas.width, canvas.height);
		for(var y = 0; y < imgPixels.height; y++){
			for(var x = 0; x < imgPixels.width; x++){
				var i = (y * 4) * imgPixels.width + x * 4;
				var avg = (imgPixels.data[i] + imgPixels.data[i + 1] + imgPixels.data[i + 2]) / 3;
				imgPixels.data[i] = avg; 
				imgPixels.data[i + 1] = avg; 
				imgPixels.data[i + 2] = avg;
			}
		}
		ctx.putImageData(imgPixels, 0, 0, 0, 0, imgPixels.width, imgPixels.height);
		return canvas.toDataURL();
    }
    }
	
	

if ( $( '.banner' ).length && jQuery() ) {
 api =  jQuery('.banner').revolution(
								{
									delay:5000,
									startheight:500,
									startwidth:960,

									hideThumbs:300,

									thumbWidth:100,							// Thumb With and Height and Amount (only if navigation Tyope set to thumb !)
									thumbHeight:50,
									thumbAmount:5,

									navigationType:"both",					//bullet, thumb, none, both		(No Thumbs In FullWidth Version !)
									navigationArrows:"verticalcentered",		//nexttobullets, verticalcentered, none
									navigationStyle:"round",				//round,square,navbar

									touchenabled:"on",						// Enable Swipe Function : on/off
									onHoverStop:"on",						// Stop Banner Timet at Hover on Slide on/off

									navOffsetHorizontal:0,
									navOffsetVertical:20,

									stopAtSlide:-1,
									stopAfterLoops:-1,

									shadow:1,								//0 = no Shadow, 1,2,3 = 3 Different Art of Shadows  (No Shadow in Fullwidth Version !)
									fullWidth:"off"							// Turns On or Off the Fullwidth Image Centering in FullWidth Modus
								});		

 

}





 if ( $( '.flexslider.slide,.flexslider.fade,.flexslider.blog-post' ).length && jQuery() ) { 
    var target_flexslider = $('.flexslider.slide');
  target_flexslider.flexslider({
        animation: "slide",
		controlNav: true,
		smoothHeight: true,
		directionNav: true,
		slideshowSpeed: 5000,          
		animationDuration: 5000,
		nextText:"&rsaquo;",
		prevText:"&lsaquo;",
		keyboardNav: true,
		easing: 'easeInOutBack',
		useCSS: false,
        start: function(slider) { target_flexslider.removeClass('loading'); }    
    });

    var target_flexslider = $('.flexslider.fade');
  target_flexslider.flexslider({
        animation: "fade",
		controlNav: true,
		smoothHeight: true,
		directionNav: true,
		slideshowSpeed: 7000,          
		animationDuration: 7000,
		nextText:"&rsaquo;",
		prevText:"&lsaquo;",
		keyboardNav: true,
        start: function(slider) { target_flexslider.removeClass('loading'); }    
    });

    var target_flexslider = $('.flexslider.blog-post.slide');
  target_flexslider.flexslider({
        animation: "fade",
		controlNav: false,
		smoothHeight: true,
		directionNav: true,
		slideshowSpeed: 7000,          
		animationDuration: 7000,
		nextText:"&rsaquo;",
		prevText:"&lsaquo;",
		keyboardNav: true,
        start: function(slider) { target_flexslider.removeClass('loading'); }    
    });
    
}








initAccordionToggle();
function initAccordionToggle() {
	jQuery('.accordion-item-toggle').each(function(i) {
		var item=jQuery(this);
		item.find('.accordion-content-toggle').slideUp(0);
		item.find('.accordion-switch-toggle').click(function() {
		 var displ = item.find('.accordion-content-toggle').css('display');
		 item.closest('ul').find('.accordion-switch-toggle').each(function() {
		  var li = jQuery(this).closest('li');
			item.removeClass("selected");
		 });
		 if (displ=="block") {
		  item.find('.accordion-content-toggle').slideUp(300) 
		  item.removeClass("selected");
		 } else {
		  item.find('.accordion-content-toggle').slideDown(300) 
		  item.addClass("selected");
		  
		 }
		});
	});
}	

$(function() {

	// grab the initial top offset of the navigation 
	var sticky_navigation_offset_top = $('#sticky_navigation').offset().top;
	
	// our function that decides weather the navigation bar should have "fixed" css position or not.
	var sticky_navigation = function(){
		var scroll_top = $(window).scrollTop(); // our current vertical position from the top
		
		// if we've scrolled more than the navigation, change its position to fixed to stick to top, otherwise change it back to relative
		if (scroll_top > sticky_navigation_offset_top) { 
			$('#sticky_navigation').css({ 'position': 'fixed', 'top':0, 'left':0 });
			$('#sticky_navigation').addClass("shadow");
			$('#sticky_navigation #main-navigation').addClass("small-nav");
			$('#sticky_navigation #logo').addClass("small-logo");
			 
			
		} else {
			$('#sticky_navigation').css({ 'position': 'relative' }); 
			 $('#sticky_navigation #main-navigation').removeClass("small-nav");
			 $('#sticky_navigation').removeClass("shadow");
			 $('#sticky_navigation #logo').removeClass("small-logo");
		}   
	};
	
	// run our function on load
	sticky_navigation();
	
	// and run it again every time you scroll
	$(window).scroll(function() {
		 sticky_navigation();
	});
	
 
	
});

 


/*ACCORDION STARTS*/ 
initAccordion();
function initAccordion() {
	jQuery('.accordion-item').each(function(i) {
		var item=jQuery(this);
		item.find('.accordion-content').slideUp(0);
		item.find('.accordion-switch').click(function() {
		 var displ = item.find('.accordion-content').css('display');
		 item.closest('ul').find('.accordion-switch').each(function() {
		  var li = jQuery(this).closest('li');
		  li.find('.accordion-content').slideUp(300);
		  jQuery(this).parent().removeClass("selected");
		 });
		 if (displ=="block") {
		  item.find('.accordion-content').slideUp(300) 
		  item.removeClass("selected");
		 } else {
		  item.find('.accordion-content').slideDown(300) 
		  item.addClass("selected");
		 }
		});
	});
}
/*ACCORDION ENDS*/ 	


 /*TABS MENU JQUERY STARTS*/ 
		(function() {
		var $tabsNav    = $('.tabs-nav'),
		$tabsNavLis = $tabsNav.children('li'),
		$tabContent = $('.tab-content');
		$tabContent.hide();
		$tabsNavLis.first().addClass('active').show();
		$tabContent.first().show();
		$tabsNavLis.on('click', function(e) {
		var $this = $(this);
		$tabsNavLis.removeClass('active');
		$this.addClass('active');
		$tabContent.hide();		
		$( $this.find('a').attr('href') ).fadeIn(700);
		e.preventDefault();
		});
	})();
  /*TABS MENU JQUERY ENDS*/ 	
  
  
/*PORTFOLIO DETAILS PAGINATION STARTS*/  
	$( '.project-pagination li' ).hover( function() {	
		$(this).find( 'a.prev' ).stop().animate({ paddingRight: '60px', opacity: 1 }, 200);	
	}, function() {	
		$(this).find( 'a.prev' ).stop().animate({ paddingRight: 0}, 200);	
	});
	$( '.project-pagination li' ).hover( function() {	
		$(this).find( 'a.next' ).stop().animate({ paddingLeft: '40px', opacity: 1 }, 200);	
	}, function() {	
		$(this).find( 'a.next' ).stop().animate({ paddingLeft: 0}, 200);	
	});
	$( '.project-pagination li' ).hover( function() {	
		$(this).find( 'a.all-projects' ).stop().animate({ paddingLeft: '60px', opacity: 1 }, 200);	
	}, function() {	
		$(this).find( 'a.all-projects' ).stop().animate({ paddingLeft: 0}, 200);	
	});
/*PORTFOLIO DETAILS PAGINATION ENDS*/ 

/*JQUERY HOVER OPACITY EFFECT STARTS*/	
  		$(".item-hover").hover(function(){
		$(this).find(".portfolio-thumbnail").stop(true, true).animate({ opacity: 'show' }, 500);
	}, function() {
		$(this).find(".portfolio-thumbnail").stop(true, true).animate({ opacity: 'hide' }, 500);		
	});
  /*JQUERY HOVER OPACITY EFFECT ENDS*/  
/*PRETTYPHOTO JQUERY CODE STARTS*/ 	
 $("a[data-rel^='prettyPhoto']").prettyPhoto({overlay_gallery: false});

 /*PRETTYPHOTO JQUERY CODE ENDS*/ 

 
  
  
/*DRIBBBLE SHOTS JQUERY STARTS*/ 	
	 $.jribbble.getShotsByPlayerId('envato', function (playerShots) {
		var html = [];
		$.each(playerShots.shots, function (i, shot) {
			html.push('<li>');
			html.push('<a href="' + shot.url + '" target="_blank">');
			html.push('<img src="' + shot.image_teaser_url + '" ');
			html.push('alt="' + shot.title + '"></a></li>');
		});	
		$('.dribbble-photos').html(html.join(''));
	}, {page: 1, per_page: 12});	
 /*DRIBBBLE SHOTS JQUERY ENDS*/ 	
 
 /*GOOGLE MAP ENDS*/
 /* $('.grey-img').BlackAndWhite( {
        hoverEffect : true, // default true
        // set the path to BnWWorker.js for a superfast implementation
        webworkerPath : false,
        // for the images with a fluid width and height 
        responsive:true,
        // to invert the hover effect
        invertHoverEffect: false,
        speed : { //this property could also be just speed: value for both fadeIn and fadeOut
            fadeIn: 200,
            fadeOut: 200,
			
        }
    });
*/
 /*INSTAGRAM PHOTOS FEEDS STARTS*/
   var clientId = 'baee48560b984845974f6b85a07bf7d9';  
      $(".instagram-photos").instagram({
        hash: 'envato',
        show: 12,
        clientId: clientId
      });
/*INSTAGRAM PHOTOS FEEDS ENDS*/ 

 /*DRIBBBLE SHOTS JQUERY STARTS*/ 	
	 $.jribbble.getShotsByPlayerId('envato', function (playerShots) {
		var html = [];
		$.each(playerShots.shots, function (i, shot) {
			html.push('<li>');
			html.push('<a href="' + shot.url + '" target="_blank"><span></span>');
			html.push('<img src="' + shot.image_teaser_url + '" ');
			html.push('alt="' + shot.title + '"></a></li>');
		});	
		$('.dribbble-photos').html(html.join(''));
	}, {page: 1, per_page: 12});	
 /*DRIBBBLE SHOTS JQUERY ENDS*/ 	

$(".flexslider").hover( function() {
			$('.flex-direction-nav').fadeIn(200);
		},
		function () {
			$('.flex-direction-nav').fadeOut(600);
		});
 /*FLEX SLIDER HOEMPAGE ENDS*/
 

 
 /*JQUERY MAIN NANVIGATION STARTS*/
  if ( $( '#main-navigation' ).length && jQuery() ) {
        $('ul.main-menu').superfish({ 
            delay:       100,                            // one second delay on mouseout 
            animation:   {opacity:'show',height:'show'},  // fade-in and slide-down animation 
            speed:       'fast',                          // faster animation speed 
            autoArrows:  false                           // disable generation of arrow mark-up 
        });
}
 
$('.screen-roll').hover(function() {
            $(this).find('span.hover_bg,span.hover_bg_video').animate({opacity:1}, 400);

        }, function() {
            $(this).find('span.hover_bg,span.hover_bg_video').stop(0,0).animate({opacity: 0}, 400);
      
        });

 
 $('.thumbnail-roll').hover(function() {
            $(this).find('span').animate({opacity:1}, 400);

        }, function() {
            $(this).find('span').stop(0,0).animate({opacity: 0}, 400);
      
        });
  if ( $( '.twitter-feeds' ).length && jQuery()) {
$(".twitter-feeds").tweet({
	 username: "trendywebstar",
	 join_text: null,
	 avatar_size: null,
	 count: 2,
	 auto_join_text_default: "we said,", 
	 auto_join_text_ed: "we",
	 auto_join_text_ing: "we were",
	 auto_join_text_reply: "we replied to",
	 auto_join_text_url: "we were checking out",
	 loading_text: "loading tweets..."
 });
 }
 /*GOOGLE MAP STARTS*/  
if ( $( '#google-map' ).length && jQuery() ) {
var $map = $('#google-map');

			$map.gMap({
			address: 'Level 13, 2 Elizabeth St, Melbourne Victoria 3000 Australia', 
			zoom: 16,
			markers: [{ 'address' : 'Level 13, 2 Elizabeth St, Melbourne Victoria 3000 Australia' }, ]	

			});
}


 /*GOOGLE MAP ENDS*/
 /*FLICKR PHOTOS FEEDS JQUERY STARTS*/ 	
	$('.flickr-feeds').jflickrfeed({
		limit: 9,
		qstrings: {
			id: '52617155@N08'
		},
		itemTemplate: '<li><a href="{{image_b}}" target="_blank"><span></span></a><img src="{{image_s}}" alt="{{title}}" /></li>'
	});
		 
		
		$('.flickr-feeds-inner').jflickrfeed({
		limit: 12,
		qstrings: {
			id: '52617155@N08'
		},
		itemTemplate: '<li><a href="{{image_b}}" target="_blank"><span></span></a><img src="{{image_s}}" alt="{{title}}" /></li>'
	}); 
	 
  /*FLICKR PHOTOS FEEDS JQUERY ENDS*/ 
 $("body").fitVids();
 /*AUDIO VIDEO PLAYER STARTS*/
 $('audio').mediaelementplayer();
/*AUDIO VIDEO PLAYER ENDS*/ 
   /*RESPONSIVE MAIN NAVIGATION STARTS*/							
	var $menu_select = $("<select />");	
	$("<option />", {"selected": "selected", "value": "", "text": "Site Main Navigation"}).appendTo($menu_select);
	$menu_select.appendTo("#main-navigation");
	$("#main-navigation ul li a").each(function(){
		var menu_url = $(this).attr("href");
		var menu_text = $(this).text();
		if ($(this).parents("li").length == 2) { menu_text = '- ' + menu_text; }
		if ($(this).parents("li").length == 3) { menu_text = "-- " + menu_text; }
		if ($(this).parents("li").length > 3) { menu_text = "--- " + menu_text; }
		$("<option />", {"value": menu_url, "text": menu_text}).appendTo($menu_select)
	})
	field_id = "#main-navigation select";
	$(field_id).change(function()
	{
	   value = $(this).attr('value');
	   window.location = value;	
	});
/*RESPONSIVE MAIN NAVIGATION ENDS*/

/*JQUERY CONTACT FORM STARTS*/
if ( $( '#contact-form' ).length && jQuery() ) {
$('form#contact-form').submit(function() {
function resetForm($form) {
    $form.find('input:text, input:password, input:file, select, textarea').val('');
    $form.find('input:radio, input:checkbox')
    .removeAttr('checked').removeAttr('selected');
}
$('form#contact-form .error-message').remove();
var hasError = false;
$('.requiredField').each(function() {
if(jQuery.trim($(this).val()) == '') {
 var labelText = $(this).prev('label').text();
 $(this).parent().append('<div class="error-message">You forgot to enter '+labelText+'</div>');
 $(this).addClass('inputError');
 hasError = true;
 } else if($(this).hasClass('email')) {
 var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
 if(!emailReg.test(jQuery.trim($(this).val()))) {
 var labelText = $(this).prev('label').text();
 $(this).parent().append('<div class="error-message">You entered an invalid '+labelText+'</div>');
 $(this).addClass('inputError');
 hasError = true;
 }
 }
});
if(!hasError) {
$('form#contact-form input.submit').fadeOut('normal', function() {
$(this).parent().append('');
});
var formInput = $(this).serialize();
$.post($(this).attr('action'),formInput, function(data){
$('#contact-form').prepend('<div class="success-message">Your email was successfully sent. We will contact you as soon as possible.</div>');
resetForm($('#contact-form'));
$('.success-message').fadeOut(5000);
 
});
}
return false;
});
}
/*JQUERY CONTACT FORM STARTS*/

/*PORTFOLIO JQUERY STARTS*/ 
 
(function() {
		var $container = $('.portfolio-items');
		if( $container.length ) {
			var $itemsFilter = $('#filterable');	
			$('li', $container).each(function(i) {
				var $this = $(this);
				$this.addClass( $this.attr('data-categories') );
			});
			$(window).on('load', function() {
				$container.isotope({
					itemSelector : 'li',
					layoutMode   : 'fitRows'
				});
			});
			$itemsFilter.on('click', 'a', function(e) {
				var $this = $(this),
				currentOption = $this.attr('data-categories');
				$itemsFilter.find('a').removeClass('active');
				$this.addClass('active');
				if( currentOption ) {
					if( currentOption !== '*' ) currentOption = currentOption.replace(currentOption, '.' + currentOption)
					$container.isotope({ filter : currentOption });
				}
				e.preventDefault();
			});
			$itemsFilter.find('a').first().addClass('active');
		}
	})();
 
 /*PORTFOLIO JQUERY ENDS*/ 
	
 });
 });