$(".menu-arrow").click(function () {
    if ($(this).parent().parent().hasClass("open")) {

    } else {
        $(this).parent().parent().children('.sub-menu').removeClass('hidden')
    }
});

