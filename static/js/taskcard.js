document.getElementById('submitComment').addEventListener('click', function() {
    const commentText = document.getElementById('commentText').value;
    if (commentText.trim() !== "") {
        const commentList = document.getElementById('commentsList');
        const newComment = document.createElement('div');
        newComment.classList.add('comment');
        newComment.textContent = commentText;
        commentList.appendChild(newComment);
        document.getElementById('commentText').value = '';
    }
});