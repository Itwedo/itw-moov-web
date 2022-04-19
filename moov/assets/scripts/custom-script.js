$(".menu-arrow").click(function () {
    if ($(this).parent().parent().hasClass("open")) {

    } else {
        $(this).parent().parent().children('.sub-menu').removeClass('hidden')
    }
});

$(".menu-item").click(function () {
    if ($(this).parent().parent().hasClass("open")) {

    } else {
        $(this).parent().parent().children('.sub-menu').removeClass('hidden')
    }
});


$("#read-more-article").click(function () {
    $(".current-article").removeClass('croped-article')
    $("#read-more-article").toggle()
    $(".article-overlay").toggle()


    window.addEventListener("scroll", () => {
        let sectionPubPos = $('.pub-section-slide').offset().top;
        console.log(sectionPubPos)
        if (window.scrollY >= 980) {
            // $("#article-side-pub-container").css({ "object-fit": "cover", "z-index": "100", "width": "400px" });
            $("#article-side-pub-container").addClass("fixed-article-side-pub")
            let sidePubPos = ($('#article-side-pub-container').offset().top + $('#article-side-pub-container').height())
            if ((sectionPubPos - sidePubPos) < 40) {
                $("#article-side-pub-container").removeClass("fixed-article-side-pub")

            }


        } else {
            $("#article-side-pub-container").removeClass("fixed-article-side-pub")
        }
    })


})

$("#read-more-article-static").click(function () {
    $("#read-more-article-static").toggle()
    $("#suite").removeClass('hidden')
})

