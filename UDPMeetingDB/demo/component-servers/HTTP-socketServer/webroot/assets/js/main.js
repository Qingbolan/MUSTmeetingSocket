(function($) {

	"use strict";

	/*
	|--------------------------------------------------------------------------
	| Template Name: Ocher
	| Author: ThemeMarch
	| Developer: Tamjid Bin Murtoza
	| Version: 1.0.0
	|--------------------------------------------------------------------------
	|--------------------------------------------------------------------------
	| TABLE OF CONTENTS:
	|--------------------------------------------------------------------------
	|
	| 1. Scripts initialization
	| 2. Preloader
	| 3. General Setup
	| 4. Primary Menu
	| 5. Scroll Function
	| 6. Section Active and Scrolling Animation
	| 7. Accordian
	| 8. Tab
	| 9. Scroll Up
	| 10. Slick Carousel
	| 11. Ajax Contact Form
	| 12. Mailchimp js
	| 13. Counter
	|
	*/

	/*--------------------------------------------------------------
		1. Scripts initialization
	--------------------------------------------------------------*/
	$.exists = function(selector) {
        return ($(selector).length > 0);
    }
    
	$(window).on('load', function() {
		$(window).trigger("scroll");
		$(window).trigger("resize");
		preloaderSetup();
	});

	$(document).ready(function() {
		$(window).trigger("resize");
		primaryMenuSetup();
		generalSetup();
		mobileMenu();
		scrollAnimation();
		sectionActive();
		accordianSetup();
		tabSetup();
		scrollUp();
		sliderCarouselSetup();
		contactForm();
		new WOW().init();
		$(".js-video-button").modalVideo();
	});

	$(window).on('resize', function() {
		mobileMenu();
	});

	$(window).on('scroll', function() {
		scrollFunction();
	});


	/*--------------------------------------------------------------
		2. Preloader
	--------------------------------------------------------------*/

	function preloaderSetup() {

		$("#tm-preloader-in").fadeOut();
		$("#tm-preloader").delay(100).fadeOut("slow");

	}
	/*--------------------------------------------------------------
		3. General Setup
	--------------------------------------------------------------*/

	function generalSetup() {

		// Social Button Active
		$(".tm-single-social-btn").on('mouseenter', function(){
			$(this).siblings().removeClass('tm-active');
	        $(this).addClass('tm-active');
	    });

	  	// Toggle Button
	    $('.tm-active-language').on('click', function() {
	      $(this).parents('.tm-language').toggleClass('tm-active');
	    });
	    $(document).on('click', function() {
	      $('.tm-language').removeClass('tm-active');
	    });
	    $('.tm-active-language, .tm-language').on('click', function(e) {
	      e.stopPropagation();
	    });

	}


	/*--------------------------------------------------------------
		4. Primary Menu
	--------------------------------------------------------------*/
	
	function primaryMenuSetup() {

		$( ".tm-primary-nav-list" ).before( "<div class='m-menu-btn'><span></span></div>" );

		$(".m-menu-btn").on('click', function(){
			$( this ).toggleClass( "m-menu-btn-ext" );
			$(this).siblings('.tm-primary-nav-list').slideToggle("slow");
		});

		$( ".menu-item-has-children > ul" ).before( "<i class='fa fa-plus m-dropdown'></i>" );

		$('.m-dropdown').on('click', function() {
			$(this).siblings('ul').slideToggle("slow");
			$(this).toggleClass("fa-plus fa-minus")
		});


		$('.maptoggle').on('click', function() {
			$( this ).siblings('.google-map').toggleClass('map-toggle');
		});

	}

	function mobileMenu() {

		if ($(window).width() <= 991){  
			$('.tm-primary-nav').addClass('m-menu').removeClass('tm-primary-nav');
		} else {
			$('.m-menu').addClass('tm-primary-nav').removeClass('m-menu');
		}

	}

	/*--------------------------------------------------------------
		5. Scroll Function
	--------------------------------------------------------------*/

	function scrollFunction() {

		var scroll = $(window).scrollTop();

		if(scroll >= 10) {
				$(".tm-site-header").addClass("small-height");
			} else {
					$(".tm-site-header").removeClass("small-height");
			}

		// For Scroll Up
		if(scroll >= 350) {
				$("#scrollup").addClass("scrollup-show");
			} else {
					$("#scrollup").removeClass("scrollup-show");
			}

	}

	/*--------------------------------------------------------------
		6. Section Active and Scrolling Animation
	--------------------------------------------------------------*/

	function scrollAnimation() {

		$('.tm-section-active a').on('click', function(event) {
			var $anchor = $(this);
			$('html, body').stop().animate({
				scrollTop: ($($anchor.attr('href')).offset().top - 30)
				}, 1250, 'easeInOutExpo');
				event.preventDefault();
		});

	}

	function sectionActive() {

		$('body').scrollspy({
			target: '.tm-section-active',
			offset: 90
		});

	}

	/*--------------------------------------------------------------
		7. Accordian
	--------------------------------------------------------------*/

	function accordianSetup() {

        var $this = $(this);
        $( ".accordian-head" ).append( "<span class='accordian-toggle'><i class='fa fa-angle-down'></i></span>" );
        $('.single-accordian').filter(':nth-child(n+2)').children('.accordian-body').hide();
        $('.single-accordian:first-child').children('.accordian-head').addClass('active');
        $('.accordian-head').on('click', function() {
            $(this).parent('.single-accordian').siblings().children('.accordian-body').slideUp();
            $(this).siblings().slideToggle();
            /* Accordian Active Class */
            $(this).toggleClass('active');
            $(this).parent('.single-accordian').siblings().children('.accordian-head').removeClass('active');
        });

    }

    /*--------------------------------------------------------------
		8. Tab
	--------------------------------------------------------------*/
	
	function tabSetup() {

		// Custom Tab
		$('.tabs.animated-fade .tab-links a').on('click',function(e){
		    var currentAttrValue = $(this).attr('href');
		    $('.tabs '+ currentAttrValue).fadeIn(400).siblings().hide();
		    $(this).parent('li').addClass('active').siblings().removeClass('active');
		    e.preventDefault();
		});
		
	}


	/*--------------------------------------------------------------
		9. Scroll Up
	--------------------------------------------------------------*/

	function scrollUp() {

		$('#scrollup').on('click', function(e) {
			e.preventDefault();
			$('html,body').animate({
				scrollTop: 0
			}, 1000);
		});

	}

	/*--------------------------------------------------------------
		10. Slick Carousel
	--------------------------------------------------------------*/

	function sliderCarouselSetup() {

		// Default Slick Slider
		$('.slider-for').slick({
		   slidesToShow: 1,
		   slidesToScroll: 1,
		   arrows: false,
		   fade: true,
		   asNavFor: '.slider-nav'
		 });

		$('.slider-nav').slick({
		   slidesToShow: 7,
		   slidesToScroll: 1,
		   asNavFor: '.slider-for',
		   dots: false,
		   focusOnSelect: true,
		   responsive: [{
		      breakpoint: 1199,
		      settings: {
		        slidesToShow: 5,
		        infinite: true
		      }

		    }, {

		      breakpoint: 991,
		      settings: {
		        slidesToShow: 3,
		        dots: true
		      }

		    },, {

		      breakpoint: 767,
		      settings: {
		        slidesToShow: 1,
		        dots: true
		      }

		    }, {

		      breakpoint: 300,
		      settings: "unslick" // destroys slick

		    }]
		 });

		// Green Slick Slider
		$('.green-slider-for').slick({
		   slidesToShow: 1,
		   slidesToScroll: 1,
		   arrows: false,
		   fade: true,
		   asNavFor: '.slider-nav'
		 });

		$('.green-slider-nav').slick({
		   slidesToShow: 1,
		   slidesToScroll: 1,
		   asNavFor: '.green-slider-for',
		   dots: false,
		   focusOnSelect: true,
		   responsive: [{
		      breakpoint: 1199,
		      settings: {
		        slidesToShow: 1,
		        infinite: true
		      }

		    }, {

		      breakpoint: 300,
		      settings: "unslick" // destroys slick

		    }]
		 });


		

	}

	/*--------------------------------------------------------------
		11. Ajax Contact Form
	--------------------------------------------------------------*/

	function contactForm() {

		$('#tm-alert').hide();
	    $('#contact-form #submit').on('click', function() {
	        var name = $('#name').val();
	        var email = $('#email').val();
	        var msg = $('#msg').val();
			var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
			
			if (!regex.test(email)) {
				$('#tm-alert').fadeIn().html('<div class="alert alert-danger"><strong>Warning!</strong> Please Enter Valid Email.</div>');
				return false;
			}

	        name = $.trim(name);
	        email = $.trim(email);
	        msg = $.trim(msg);

	        if (name != '' && email != '' && msg != '') {
	            var values = 	"name=" + name + 
	            				"&email=" + email + 
	            				"&msg=" + msg;
	            $.ajax({
	                type: "POST",
	                url: "assets/php/mail.php",
	                data: values,
	                success: function() {
	                    $('#name').val('');
	                    $('#email').val('');
	                    $('#msg').val('');

	                    $('#tm-alert').fadeIn().html('<div class="alert alert-success"><strong>Success!</strong> Email has been sent successfully.</div>');
	                    setTimeout(function() {
	                        $('#tm-alert').fadeOut('slow');
	                    }, 4000);
	                }
	            });
	        } else {
				$('#tm-alert').fadeIn().html('<div class="alert alert-danger"><strong>Warning!</strong> All fields are required.</div>');
	        }
	        return false;
	    });

	}

	/*--------------------------------------------------------------
	    12. Mailchimp js
	--------------------------------------------------------------*/

	// mailchimp start
    if ($('.mailchimp').length > 0) {
        $('.mailchimp').ajaxChimp({
            language: 'es',
            callback: mailchimpCallback
        });
    }

    function mailchimpCallback(resp) {
        if (resp.result === 'success') {
            $('.subscription-success').html('<i class="fa fa-check"></i><br/>' + resp.msg).fadeIn(1000);
            $('.subscription-error').fadeOut(500);

        } else if (resp.result === 'error') {
            $('.subscription-error').html('<i class="fa fa-times"></i><br/>' + resp.msg).fadeIn(1000);
        }
    }
    $.ajaxChimp.translations.es = {
        'submit': 'Submitting...',
        0: 'We have sent you a confirmation email',
        1: 'Please enter a value',
        2: 'An email address must contain a single @',
        3: 'The domain portion of the email address is invalid (the portion after the @: )',
        4: 'The username portion of the email address is invalid (the portion before the @: )',
        5: 'This email address looks fake or invalid. Please enter a real email address'
    };


	/*--------------------------------------------------------------
	    13. Counter
	--------------------------------------------------------------*/
if ($.exists('#tm-if-expired')) {
	// Set the date we're counting down to tm-if-expired
	var countDownDate = new Date("Nov 5, 2019 15:37:25").getTime();

	// Update the count down every 1 second
	var x = setInterval(function() {

	    // Get todays date and time
	    var now = new Date().getTime();
	    
	    // Find the distance between now an the count down date
	    var distance = countDownDate - now;
	    
	    // Time calculations for days, hours, minutes and seconds
	    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
	    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
	    
	    // Output the result in an element with id="demo"
	    document.getElementById("tm-count-days").innerHTML = days;
	    document.getElementById("tm-count-hours").innerHTML = hours;
	    document.getElementById("tm-count-minutes").innerHTML = minutes;
	    document.getElementById("tm-count-seconds").innerHTML = seconds;
	    
	    // If the count down is over, write some text 
	    if (distance < 0) {
	        clearInterval(x);
	        document.getElementById("tm-if-expired").innerHTML = "TOKEN EXPIRED";
	    }
	}, 1000);
}


$('[data-bgimage]').each(function () {
	var imageUrl = $(this).data('bgimage');
	$(this).css({
			'background-image': 'url(' + imageUrl + ')'
	});
});

})(jQuery); // End of use strict
