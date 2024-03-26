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

if ($(window).width() < 1000) {
    if ($("#article-side-pub-container")) handleClickReadMore()
}

// actualite
window.onresize = function () {

    if ($(window).width() < 1000) {
        if ($("#article-side-pub-container")) handleClickReadMore()
    }
};


function handleClickReadMore() {
    window.onresize = function () {

        if ($(window).width() < 760) {
            if ($("#article-side-pub-container")) {
                $("#article-side-pub-container").width($("#side-pub-container").width())
                $("#article-side-pub-container").removeClass("fixed-article-side-pub")
            }
        }
    };

    $(".current-article").removeClass('croped-article')
    $("#read-more-article").toggle()
    $(".article-overlay").toggle()

    $("#read-more-article").hide()
    $(".article-overlay").hide()


    document.body.addEventListener("scroll", () => {

        let sectionPubPos = $('.pub-section-slide').offset().top;

        var scrollPosition = document.documentElement.scrollTop || document.body.scrollTop;

        // if (window.scrollY >= 980 && $(window).width() > 760) {
        if (scrollPosition >= 980 && $(window).width() > 640) {
            $("#article-side-pub-container").addClass("fixed-article-side-pub")
            $("#article-side-pub-container").width($("#side-pub-container").width())
            let sidePubPos = ($('#article-side-pub-container').offset().top + $('#article-side-pub-container').height())

            const differenceHeight = sectionPubPos - sidePubPos
            console.log('differenceHeight', differenceHeight)
            if ((differenceHeight) < 40) {
                $("#article-side-pub-container").removeClass("fixed-article-side-pub")

            }


        } else {
            $("#article-side-pub-container").removeClass("fixed-article-side-pub")
        }
    })
}

$("#read-more-article").click(handleClickReadMore)

$("#read-more-article-static").click(function () {
    $("#read-more-article-static").toggle()
    $("#suite").removeClass('hidden')
})


// share popover
function setLinkToShare(link) {
    $(".to-copy-link .platform-name").text("Copier le lien")
    $(".fb-link").attr("href", "https://www.facebook.com/share.php?u=https://moov-web.sudo.mg" + link)
    $(".tw-link").attr("href", `https://twitter.com/intent/tweet?url=moov-web.sudo.mg${link}`)
    $(".in-link").attr("href", `https://www.linkedin.com/sharing/share-offsite/?url=moov-web.sudo.mg${link}`)
    $(".to-copy-link").attr("data-clipboard-text", `https://moov-web.sudo.mg${link}`)
}

PopoverComponent.init({
    ele: '.popover-share'
});

// clipboard
var clipboard = new ClipboardJS('.to-copy-link');
clipboard.on('success', function (e) {
    $(".to-copy-link .platform-name").text("Lien copié")
    e.clearSelection();
});



