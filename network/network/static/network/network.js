document.addEventListener('DOMContentLoaded', function() {
    // function to load the div that displays the 'like' or 'unlike'
    document.getElementById("all_User_posts").addEventListener("load", load_like (curr_user));
});


// implement the follow function
function follow() {
    // create a follow and unfollow button
    fetch(`/users/${profile}`)
    .then(response => response.json())
    .then(data => {
        // check if the visiting user is not the owner of the profile
        if (curr_user != profile) {
            // create new button element
            const follow_btn = document.createElement('button');
            follow_btn.setAttribute('class', 'btn btn-sm btn-outline-primary ml-2');

            // check condition if user is following profile
            var follow_len = data[0].fields.followers;

            // change text of button depending on 'follow' status
            follow_btn.textContent =  follow_len.includes(parseInt(curr_user_id)) ? "Unfollow" : "Follow";        
            // add button to html
            document.querySelector('#follow_button').appendChild(follow_btn);
            
            // make an API PUT request to update the database
            follow_btn.addEventListener('click', () => {
               fetch(`/users/${profile}`, {
                method: 'PUT',
                body: JSON.stringify({
                    is_following: !(data[0].fields.is_following),
                    following: data[0].fields.user,
                })
              })
            // Reload the page automatically
            window.location.reload();
            })
        }
    });   
    return false;
}

// function to save an edited post
function edit(post_id) {
    // hide and show text are and edit link as appropriate
    document.querySelector(`#E${post_id}`).style.display = 'block';
    document.querySelector(`#A${post_id}`).style.display = 'none';

    // GET API to get the number of likes
    fetch(`/edit/${curr_user}/${post_id}`)
    .then(response => response.json())
    .then(data => {
        // create text area
        const textarea = document.createElement('textarea');
        textarea.setAttribute('class', 'ml-2');
        textarea.rows = 10;
        textarea.cols = 30;
        textarea.innerHTML = data[0].fields.post_content;

        // create button
        const btn = document.createElement('button');
        btn.setAttribute('class', 'btn btn-sm btn-outline-primary ml-2');
        btn.textContent = 'Save';
    
        // insert created element
        document.querySelector(`#E${post_id}`).append(textarea);
        document.querySelector(`#E${post_id}`).append(btn);

        btn.addEventListener('click', function() {
            fetch(`/edit/${curr_user}/${post_id}`, {
                method: 'POST',
                body: JSON.stringify({
                    edited_post: textarea.value
                })
              })
                //   set new post to inner html
                document.querySelector(`#post_content${post_id}`).innerHTML = textarea.value;
                document.querySelector(`#E${post_id}`).style.display = 'none';
                document.querySelector(`#A${post_id}`).style.display = 'block';
              return false; 
        });
    });
}


// fumctiion on load to decide whether to show 'like' and 'unlike'
function load_like (curr_user){
         // API fetch GET request
        fetch(`/like/${curr_user}`)
        .then(response => response.json())
        .then(posts => {

            // console.log(posts)    
           var x = document.querySelectorAll('.article-title');
           for (var i = 0; i< x.length; i++) {
                var num_id = parseInt(x[i].id);

               if(posts.includes(num_id)) {
                    x[i].innerHTML = 'Unlike'
                }else{
                    x[i].innerHTML = 'Like'
               }               
           }        
        });        
}


//function to like and unlike a post
function umptenth(post_id) {
    // make a get api request
    fetch(`/edit/${curr_user}/${post_id}`)
    .then(response => response.json())
    .then(post_info => {

        // get the number of likes
        var like_count = post_info[0].fields.user_like.length;

        // change to like or dislike
        var x = document.getElementById(`${post_id}`);
        if(x.innerHTML === 'Like') {
            x.innerHTML = 'Unlike'
            // make API PUT request
            fetch(`/edit/${curr_user}/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    user_like: curr_user_id,
                    has_liked: true
                })
            })
            // Update like on webpage
            document.querySelector(`#like_count${post_id}`).innerHTML = like_count + 1;
            // console.log(has_liked)
        }else{
            x.innerHTML = 'Like'
             // make API PUT request
            fetch(`/edit/${curr_user}/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    user_like: curr_user_id,
                    has_liked: false
                })
            })
            // Update like on webpage
            document.querySelector(`#like_count${post_id}`).innerHTML = like_count - 1;
       }   
    });
}
