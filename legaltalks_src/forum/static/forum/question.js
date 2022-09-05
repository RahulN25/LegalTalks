$(document).ready(function (){
	/*let upvoted = false;
    let downvoted = false;*/
    let question = window.location.pathname.slice(16).replace("/", "");

	let upvoted = {
		"q" : false
    };
    let test = $('.question-card').children(':first-child').find('.btn-group').children(':first-child').hasClass('bg-success');
    if (test){
        upvoted["q"] = true;
    }
    else{
        upvoted["q"] = false;
    }
	let downvoted = {
		"q" : false
    };
    test = $('.question-card').children(':first-child').find('.btn-group').children(':last-child').hasClass('bg-danger');
    if (test){
        downvoted["q"] = true;
    }
    else{
        downvoted["q"] = false;
    }
	let answers = $(".answer-card");
	for(var i = 0; i < answers.length; i++){
        let answer_id = $(answers[i]).attr("id").replace("answer-id-", "");
        if ($(answers[i]).find(".btn-group").children(':first-child').hasClass('bg-success')){
            upvoted[answer_id] = true;
        }
        else{
            upvoted[answer_id] = false;
        }
        if ($(answers[i]).find(".btn-group").children(':last-child').hasClass('bg-danger')){
            downvoted[answer_id] = true;
        }
        else{
            downvoted[answer_id] = false;
        }
	}
	$(".btn-group").click(function (e){
		let ans_id = $(this).parent().closest(".answer-card").attr("id");
		if (!ans_id) {
			ans_id = "q";
		}
		else {
			ans_id = ans_id.replace("answer-id-", "");
		}
		console.clear();
		console.log(ans_id);
		// s = e.target
		// console.log(s);
		let upvote_btn = $(this).children(":first-child");
		let up = upvote_btn.children()[0];
		let downvote_btn = $(this).children(":last-child");
        let down = downvote_btn.children()[0];
        let vote_count = $(this).children()[1];
		if (($(e.target).attr("title") == "Upvote") || ($(e.target)[0] == $(this).find(".fa-arrow-up")[0])){
			if (upvoted[ans_id]){
				upvote_btn.removeClass("bg-success");
				upvote_btn.addClass("border-success");
				$(up).removeClass("text-white");
				$(up).addClass("text-success");
                upvoted[ans_id] = false;
                $.ajax({
                    type: "POST",
                    url: "/forum/vote/",
                    data: {
                        "forum_obj": ans_id,
                        "question": question,
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
			else{
				if (downvoted[ans_id]) {
					downvote_btn.removeClass("bg-danger");
					downvote_btn.addClass("border-danger");
					$(down).removeClass("text-white");
					$(down).addClass("text-danger");
					downvoted[ans_id] = false;
				}
				upvote_btn.removeClass("border-success");
				upvote_btn.addClass("bg-success");
				$(up).removeClass("text-success");
				$(up).addClass("text-white");
                upvoted[ans_id] = true;
                $.ajax({
                    type: "POST",
                    url: "/forum/vote/",
                    data: {
                        "forum_obj": ans_id,
                        "question": question,
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
			console.log(ans_id + " Upvoted: " + upvoted[ans_id] + " | Downvoted: " + downvoted[ans_id]);
		}
		else if(($(e.target).attr("title") == "Downvote") || ($(e.target)[0] == $(this).find(".fa-arrow-down")[0])){
			if (downvoted[ans_id]){
				downvote_btn.removeClass("bg-danger");
				downvote_btn.addClass("border-danger");
				$(down).removeClass("text-white");
				$(down).addClass("text-danger");
                downvoted[ans_id] = false;
                $.ajax({
                    type: "POST",
                    url: "/forum/vote/",
                    data: {
                        "forum_obj": ans_id,
                        "question": question,
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
			else{
				if (upvoted[ans_id]) {
					upvote_btn.removeClass("bg-success");
					upvote_btn.addClass("border-success");
					$(up).removeClass("text-white");
					$(up).addClass("text-success");
					upvoted[ans_id] = false;
				}
				downvote_btn.removeClass("border-danger");
				downvote_btn.addClass("bg-danger");
				$(down).removeClass("text-danger");
				$(down).addClass("text-white");
                downvoted[ans_id] = true;
                $.ajax({
                    type: "POST",
                    url: "/forum/vote/",
                    data: {
                        "forum_obj": ans_id,
                        "question": question,
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
			console.log(ans_id + " Upvoted: " + upvoted[ans_id] + " | Downvoted: " + downvoted[ans_id]);
		}
		// if (this.target)
	});
});