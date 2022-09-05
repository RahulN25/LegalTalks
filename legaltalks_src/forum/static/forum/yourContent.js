$(document).ready(function () {
    $("input[value=both]").prop("checked", true);
    $("input[value=newest]").prop("checked", true);

    $("input[name=content_type]").change(function (e) { 
        $(".row .justify-content-center").hide();
        $("#loading-icon").show();
        let cards = $(".row .justify-content-center");
        if (this.value == "questions") {
            setTimeout(function(){
                $("#loading-icon").hide();
                for (let i = 0; i < cards.length; i++) {
                    if ( !($(cards[i]).find(".badge").text() == "Question") ) {
                        $(cards[i]).hide();
                    }
                    else {
                        $(cards[i]).show();
                    }
                }
            }, 1300);
        }
        else if (this.value == "answers") {
            setTimeout(function(){
                $("#loading-icon").hide();
                for (let i = 0; i < cards.length; i++) {
                    if ( !($(cards[i]).find(".badge").text() == "Answer") ) {
                        $(cards[i]).hide();
                    }
                    else {
                        $(cards[i]).show();
                    }
                }
            }, 1300);
        }
        else {
            setTimeout(function(){
                $("#loading-icon").hide();
                for (let i = 0; i < cards.length; i++) {
                    $(cards[i]).show();
                }
            }, 1300);
        }
        $(e.target).blur();
    });
    $("input[name=order]").change(function (e) { 
        let cards = jQuery.makeArray($(".row .justify-content-center"));
        $(".row .justify-content-center").remove();
        // $(".row .justify-content-center").hide();
        cards = cards.reverse();
        $("#loading-icon").show();
        $(e.target).blur();
        setTimeout(function(){
            $("#loading-icon").hide();
            $("#card-container").after(cards);
        }, 1300);
    });
});