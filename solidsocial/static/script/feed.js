document.addEventListener('DOMContentLoaded', function() {
    // Markdown Editor
    let feedsize = 50;
    const emd = new EasyMDE({element: document.getElementById('np-text'), placeholder: "Erstelle einen neuen Post!", hideIcons: ['fullscreen', 'side-by-side', 'image'], status: false, spellChecker: false});

    // Date of Feed Load
    const curdate = new Date();
    const curdatestr = curdate.toISOString().slice(0,18) + '.000000';

    // Submit new oost botton
    document.getElementById('np-submit').addEventListener('click', function(event) {
            event.preventDefault();
            submitNewPost(emd);
        });

    // Mehr Button
    if (document.getElementById('feed-more')) {
        document.getElementById('feed-more').addEventListener('click', function(event) {
                loadMoreFeed(event, feedsize);
                feedsize += 50;
        });
    }

    eventifyButtons();

    // Start Feed Update
    updateFeed(curdatestr);

});

function eventifyButtons () {
    // Post control buttons
    const likebuttons = document.querySelectorAll('button.like-button');
    likebuttons.forEach(el => el.addEventListener('click', event => { reactPost(event,  el)}, false));

    const replybuttons = document.querySelectorAll('button.reply-button');
    replybuttons.forEach(el => el.addEventListener('click', event => { replyPost(event,  el)}, false));

    const sharebuttons = document.querySelectorAll('button.share-button');
    sharebuttons.forEach(el => el.addEventListener('click', event => { sharePost(event,  el)}, false));

    // Delete post button on own posts
    const delbuttons = document.querySelectorAll('button.del-own');
    delbuttons.forEach(el => el.addEventListener('click', event => { deletePost(event,  el)}, false));

    // Clear Modal on closing
    document.getElementById('modal-close').addEventListener('click', function(event) {
            clearModal(emd);
        });

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
}

function sharePost(e, el) {
    e.preventDefault();
    const id = get_id(el.id);
    if (confirm("Do you want to repost this post?") == true) {
        document.getElementById('postId').value = id;
        document.getElementById('np-submit').click();
    } 
}

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

function loadMoreFeed(e, start) {
    e.preventDefault();

    const successfunc = result => {
        const feed = document.getElementById('feed');
        feed.insertAdjacentHTML('beforeend', result);
        eventifyButtons();
    }
    const end = start + 50;
    fetch_call(`${POSTS_URL}?feed=${end}&start=${start}`, "GET", null, successfunc, null, 'json');
};

function updateFeed(curdatestr) {

    const successfunc = result => {
        if (result.status == "started") {
            var iId = window.setInterval(function(){
                const successHandler = result => {
                    if (result.status == "updated") {
                        const feed = document.getElementById('feed');
                        if (result.data != null) {
                            feed.insertAdjacentHTML('afterbegin', result.data);
                        }
                        clearInterval(iId);
                    }
                }
                fetch_call(`${FEEDUPDATE_URL}?date=${curdatestr}`, "GET", null, successHandler, null, 'json');
            }, 3000);
        }
    }
    if (!demo == "True"){
        fetch_call(`${FEEDUPDATE_URL}?date=${curdatestr}`, "GET", null, successfunc, null, 'json');
    }

}

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

function replyPost(e, el) {
    e.preventDefault();
    const id = get_id(el.id);
    const ref = el.parentElement.dataset.ref;
    document.getElementById('postId').value = id;
    const refpost = document.getElementById(`${id}-post`); 
    const refpostcopy = refpost.cloneNode(true);
    document.getElementById('ref-box').appendChild(refpostcopy);
    document.getElementById('np-modal').checked = true;
    document.getElementById('modal-h').innerText = "Auf Post antworten"
}

function submitNewPost(emd) {
    const content = emd.value();
    const mediaFile = document.getElementById('np-media').files;
    const ref = document.getElementById('postId').value;


    const data = new FormData();
    if (content) {
        data.append('content', content);
    }
    if (mediaFile.length > 0){
        data.append('media', mediaFile[0]);
    }
    if (document.getElementById('np-sign').checked) {
        data.append('sign', true);
    }
    if (document.getElementById('np-priv').checked) {
        data.append('priv', true);
    }
    data.append('html', true);
    if (ref) {
        data.append('response', ref)
    }

    const successfunc = result => {
        document.getElementById('np-modal').checked = false;
        const postdiv = document.getElementById('feed');
        postdiv.insertAdjacentHTML('afterbegin', result.html)
        clearModal(emd);
    }

    fetch_call(POSTS_URL, "POST", data, successfunc, null);
};

function clearModal(emd) {
    emd.value('');
    document.getElementById('postId').value = '';
    document.getElementById('np-media').value = null;
    document.getElementById('modal-h').innerText = "Post erstellen"
    document.getElementById('ref-box').innerHTML = '';
}
