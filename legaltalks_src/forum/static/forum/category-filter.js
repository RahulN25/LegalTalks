$(document).ready(function () {
    $(".cat-values > input[type=checkbox]").prop("checked", false);
    let upvoted = {};
    let downvoted = {};
    let questions_ = $(".question-card");
    for(var i = 0; i < questions_.length; i++){
        let question_id = $(questions_[i]).attr("id").replace("question-id-", "");
        if($(questions_[i]).find(".btn-group").children(':first-child').hasClass('bg-success')){
            upvoted[question_id] = true;
        }
        else{
            upvoted[question_id] = false;
        }
        if($(questions_[i]).find(".btn-group").children(':last-child').hasClass('bg-danger')){
            downvoted[question_id] = true;
        }
        else{
            downvoted[question_id] = false;
        }
    }
    $(".btn-group").click(function (e){
        let ques_id = $(this).parent().closest(".question-card").attr("id").replace("question-id-", "");
        let upvote_btn = $(this).children(":first-child");
		let up = upvote_btn.children()[0];
		let downvote_btn = $(this).children(":last-child");
        let down = downvote_btn.children()[0];
        let vote_count = $(this).children()[1];

        if (($(e.target).attr("title") == "Upvote") || ($(e.target)[0] == $(this).find(".fa-arrow-up")[0])){
            if (upvoted[ques_id]){
                upvote_btn.removeClass("bg-success");
				upvote_btn.addClass("border-success");
				$(up).removeClass("text-white");
				$(up).addClass("text-success");
                upvoted[ques_id] = false;
                $.ajax({
                    type: "POST",
                    url: "/forum/vote/",
                    data: {
                        "forum_obj": "q",
                        "question": ques_id,
                        0: "up",
                        1: "rmv_upvote"
                    },
                    success: function (response) {
                        e.preventDefault();
                        if (response["login"]){
                            window.location.href = response["login"];
                        }
                        else{
                            $(vote_count).text(response["votes"]);
                        }
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            }
            else {
                if (downvoted[ques_id]) {
					downvote_btn.removeClass("bg-danger");
					downvote_btn.addClass("border-danger");
					$(down).removeClass("text-white");
					$(down).addClass("text-danger");
					downvoted[ques_id] = false;
				}
				upvote_btn.removeClass("border-success");
				upvote_btn.addClass("bg-success");
				$(up).removeClass("text-success");
				$(up).addClass("text-white");
                upvoted[ques_id] = true;
                $.ajax({
                    type: "POST",
                    url: "/forum/vote/",
                    data: {
                        "forum_obj": "q",
                        "question": ques_id,
                        0: "up",
                        1: "add_upvote"
                    },
                    success: function (response) {
                        e.preventDefault();
                        if (response["login"]){
                            window.location.href = response["login"];
                        }
                        else{
                            $(vote_count).text(response["votes"]);
                        }
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            }
            upvote_btn.blur();
            console.log(ques_id + " Upvoted: " + upvoted[ques_id] + " | Downvoted: " + downvoted[ques_id]);
        }
        else if(($(e.target).attr("title") == "Downvote") || ($(e.target)[0] == $(this).find(".fa-arrow-down")[0])){
            if (downvoted[ques_id]){
                downvote_btn.removeClass("bg-danger");
				downvote_btn.addClass("border-danger");
				$(down).removeClass("text-white");
				$(down).addClass("text-danger");
                downvoted[ques_id] = false;
                $.ajax({
                    type: "POST",
                    url: "/forum/vote/",
                    data: {
                        "forum_obj": "q",
                        "question": ques_id,
                        0: "down",
                        1: "rmv_downvote"
                    },
                    success: function (response) {
                        e.preventDefault();
                        if (response["login"]){
                            window.location.href = response["login"];
                        }
                        else{
                            $(vote_count).text(response["votes"]);
                        }
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            }
            else {
                if (upvoted[ques_id]) {
					upvote_btn.removeClass("bg-success");
					upvote_btn.addClass("border-success");
					$(up).removeClass("text-white");
					$(up).addClass("text-success");
					upvoted[ques_id] = false;
				}
				downvote_btn.removeClass("border-danger");
				downvote_btn.addClass("bg-danger");
				$(down).removeClass("text-danger");
				$(down).addClass("text-white");
                downvoted[ques_id] = true;
                $.ajax({
                    type: "POST",
                    url: "/forum/vote/",
                    data: {
                        "forum_obj": "q",
                        "question": ques_id,
                        0: "down",
                        1: "add_downvote"
                    },
                    success: function (response) {
                        e.preventDefault();
                        if (response["login"]){
                            window.location.href = response["login"];
                        }
                        else{
                            $(vote_count).text(response["votes"]);
                        }
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            }
            downvote_btn.blur();
            console.log(ques_id + " Upvoted: " + upvoted[ques_id] + " | Downvoted: " + downvoted[ques_id]);
        }
    });
    $(".cat-values > .form-check-input").change(function (e) {
        $("#loading-icon").show();
        $(".question-card").parent().hide();
        setTimeout(function(){
            $("#loading-icon").hide();
            $(".question-card").parent().show();
        }, 2000);

        let categories = document.querySelectorAll(".cat-values > .form-check-input");
        let questions = $(".question-card");
        let checked_categories = [];
        console.clear();
        // console.log(questions);
        for(let i = 0; i < categories.length; i++){
            if (categories[i].checked){
                checked_categories.push($(categories[i]).next().text());
                // console.log("CHECKED" + $(categories[i]).next().text());
            }
        }
        for(let q_index = 0; q_index < questions.length; q_index++){
            if (checked_categories.length == 0){
                for (let i = 0; i < questions.length; i++){
                    $(questions[i]).show();
                }
                break;
            }
            let current_question = questions[q_index];
            // console.log(current_question);
            let category_text = current_question.querySelector(".badge").textContent;
            // let category_text = $(current_question).children(".badge .badge-info").text();
            console.log(category_text);
            let exists = false;
            for (let i = 0; i < checked_categories.length; i++){
                if (category_text == checked_categories[i].trim()){
                    exists = true;
                    break;
                }
            }
            if (exists){
                $(current_question).show();
            }
            else{
                $(current_question).hide();
            }
        }
    });

});