$('.cover').parallax({
    speed: 0.5
});

// On scroll add class
$(window).scroll(function () {
    var scroll = $(window).scrollTop();

    //>=, not <=
    if (scroll >= 50) {
        //clearHeader, not clearheader - caps H
        $("nav").addClass("stick_header");
    } else {
        $("nav").removeClass("stick_header");
    }
});


// On click smooth scroll
$(".scroll").click(function () {
    $('html, body').animate({
        scrollTop: $("#section_info").offset().top
    }, 2000);
});

// Slider 
$(document).ready(function () {

    $('.team_slider').bxSlider({
        slideWidth: 200,
        minSlides: 3,
        maxSlides: 4,
        moveSlides: 1,
        slideMargin: 10
    });
});
