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
        if (window.scrollY >= 980) {
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


//share popover
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
