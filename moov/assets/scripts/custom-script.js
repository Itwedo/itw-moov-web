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


// let articleHeight = $(".current-article").offset().top + $(".current-article").height()
// let articlePart1Height = $(".text-part-1").offset().top + $(".text-part-1").height()

// let text = $(".text-part-1").text().trim()
// text = text.split(" ")
// let lastWds = text[text.length - 4] + " " + text[text.length - 3] + " " + text[text.length - 2] + " " + text[text.length - 1]
// let text2 = $(".text-part-2").text().trim()
// let apparition = text2.search(text[text.length - 1])
// text2 = text2.slice(apparition + (text[text.length - 1]).length, (text2.length))

// $(".text-part-1").text($(".text-part-1").text().trim())
// $(".text-part-2").text(text2)