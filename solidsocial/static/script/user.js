document.addEventListener('DOMContentLoaded', function() {

    // Post control buttons
    const likebuttons = document.querySelectorAll('button.like-button');
    likebuttons.forEach(el => el.addEventListener('click', event => { reactPost(event,  el)}, false));

    // Delete post button on own posts
    const delbuttons = document.querySelectorAll('button.del-own');
    delbuttons.forEach(el => el.addEventListener('click', event => { deletePost(event,  el)}, false));

    // Collapsible for hidden posts
    const coll = document.getElementsByClassName("collapsible");
    let i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            let content = this.nextElementSibling;
            if (content.style.maxHeight){
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            } 
        });
    }

});

function deletePost(e, el) {
    e.preventDefault();
    const id = get_id(el.id);
    if (confirm("Möchten sie den Post wirklich entfernen?") == true) {
        fetchCall(`${POST_URL}/${id}`, "DELETE", null, null);
        document.getElementById(`${id}-post`).remove();
    } 
}

function fetch_call(url, method, data, success=()=>null, error=null, ctype=null) {
    const errorfunc = () => {
        if (typeof error === "function") {
            error();
        } else {
            console.error('Error:', error);
        }
    }   
    let fetch_data = {method: method, body: data};
    if (ctype == "json"){
        fetch_data.headers = {"Content-Type": "application/json",};
        if ( method != "GET" ) {
            fetch_data.body = JSON.stringify(data);
        }
    }
    fetch(url, fetch_data )
        .then(res => {
            return res.json();
        })
        .then(res => {
            success(res);
        })
        .catch(error => {
            errorfunc();
        });
};

function reactPost(e, el) {
    e.preventDefault();
    const ref = el.parentElement.dataset.ref;

    if (el.classList.contains("liked")) {
        return 0;
    }

    const successfunc = result => {
        el.classList.add("liked");
    }

    fetch_call(REACTS_URL, "POST", {post: ref}, successfunc, null, 'json');
}
