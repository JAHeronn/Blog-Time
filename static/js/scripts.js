/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
// Navbar scroll behavior
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    if (!mainNav) return;

    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function () {
        const currentTop = document.body.getBoundingClientRect().top * -1;

        if (currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove('is-visible');
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
});

// Enable edit comment
function enableEdit(commentId) {
    document.getElementById('comment-display-' + commentId).style.display = 'none';
    document.getElementById('comment-form-' + commentId).style.display = 'block';
}

// Cancel edit comment
function cancelEdit(commentId) {
    document.getElementById('comment-form-' + commentId).style.display = 'none';
    document.getElementById('comment-display-' + commentId).style.display = 'block';
}

// Submit new comment via AJAX
function submitNewComment(event) {
    console.log('Form submitted!');
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        console.log('Response status:', response.status);

        if (response.headers.get('content-type')?.includes('application/json')) {
            return response.json();
        } else {
            return response.text().then(text => {
                console.log('HTML response:', text);
                throw new Error('Server returned HTML instead of JSON');
            });
        }
    })
    .then(data => {
        console.log('Data received:', data);
        if (data.success) {
            // Clear the form
            form.reset();

            // Add the new comment to the comments list
            const commentsList = document.querySelector('ul.commentList'); // Changed this line
            console.log('Comments list element:', commentsList);
            if (commentsList && data.comment_html) {
                const temp = document.createElement('div');
                temp.innerHTML = data.comment_html.trim();
                const newCommentElement = temp.firstElementChild; // This will be the <li>

                // Add to top of comments list
                commentsList.insertBefore(newCommentElement, commentsList.firstChild);
            }
        } else if (data.errors) {
            console.log('Form errors:', data.errors);
            displayFormErrors(data.errors);
        } else if (data.error) {
            console.log('Auth error:', data.error);
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}


// Submit the comment edit via AJAX
function submitCommentEdit(event, commentId) {
    event.preventDefault();

    const form = document.getElementById('comment-form-' + commentId);
    const formData = new FormData(form);

    fetch(`/edit-comment/${commentId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const commentElement = document.getElementById('comment-' + commentId);
        if (commentElement && data.updated_html) {
            const temp = document.createElement('div');
            temp.innerHTML = data.updated_html.trim();
            const newCommentElement = temp.firstElementChild;
            commentElement.replaceWith(newCommentElement);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Submit comment delete via AJAX
function deleteComment(commentId) {
    if (!confirm("Are you sure you want to delete this comment?")) return;

    fetch(`/delete-comment/${commentId}`, {
        method: 'DELETE',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (response.ok) {
            const commentElement = document.getElementById('comment-' + commentId);
            if (commentElement) {
                commentElement.remove();
            }
        } else {
            console.error("Failed to delete comment.");
        }
    })
    .catch(err => console.error(err));
}

