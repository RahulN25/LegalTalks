$(document).ready(function () {
    $(".edit-answer-button").click(function (e) { 
        console.clear();
        $("#answer-anonymous").prop("checked", false);
        let answer_id = $(this).parent().closest(".answer-card").attr("id");
        answer_id = answer_id.replace("answer-id-", "") + "/";
        $("#edit-answer").attr("action", "/forum/answer/edit/" + answer_id);
        let img_name = $(this).parent().closest(".answer-card").find("img").attr("src").replace("/media/", "");
        if (img_name == "anonymous.png"){
            $("#answer-anonymous").prop("checked", true);
        }
        let answer_text = $(this).parent().closest(".answer-card").find("p").html();
        let regex = /<br\s*[\/]?>/gi;
        $("#edit-answer-detail").val(answer_text.replace(regex, "\n"));
    });
    $(".delete-answer").click(function (e) { 
        console.clear();
        let answer_id = $(this).parent().closest(".answer-card").attr("id");
        answer_id = answer_id.replace("answer-id-", "") + "/";
        $("#delete-answer").attr("action", "/forum/answer/delete/" + answer_id);
        let answer_card = $(this).parent().closest(".answer-card");
        console.log(answer_card.attr("id"));
    });
});