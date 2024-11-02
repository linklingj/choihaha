
function commentButton(id) {
	const commentForm = document.getElementsByClassName("answer_comment_box")[id];
	commentForm.style.display = "block";
}

function hideButton(id) {
	const commentForm = document.getElementsByClassName("answer_comment_box")[id];
	commentForm.style.display = "none";
}