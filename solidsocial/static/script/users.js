document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-author').addEventListener('click', function(event) {
            event.preventDefault();
            addAuthor();
        });
    const followbuttons = document.querySelectorAll('button.follow');
    followbuttons.forEach(el => el.addEventListener('click', event => { toggleFollow(event,  el)}, false));

    const removebuttons = document.querySelectorAll('button.u-remove');
    removebuttons.forEach(el => el.addEventListener('click', event => { removeAuthor(event,  el)}, false));

    const allcheckbox = document.getElementById("showall");
    console.log(allcheckbox)
    allcheckbox.addEventListener('change', function() {
        const usertrs = document.querySelectorAll('tr.not_followed')
        if (this.checked) {
            usertrs.forEach( (el) => {el.style.display = "table-row";} )
        } else {
            usertrs.forEach( (el) => {el.style.display = "none";} )
        }
    });
});

function addAuthor() {
    const webid = document.getElementById('aa-webid').value;

    const successfunc = result => {
        console.log('in add author succ')
        const html = `
            <tr id="at-${ result.id }">
                <td><a href="/user/${ result.id }">${ result.name }</a></td>
                <td><a href="${ result.url }">${ result.url.replace('https://', '@').replace('/profile/card#me','') }</a></td>
                <td>
                    <button class="follow" id="${ result.id }-follow"><i class="fa-solid fa-user-plus"></i></button>
                    <button class="u-remove mute" id="${ result.id }-remove"><i class="fa-solid fa-user-slash"></i></button>
                </td>
            </tr>
        `
        const userstable = document.getElementById('users-tb');
        userstable.insertAdjacentHTML('afterbegin', html);
        document.getElementById('aa-webid').value = '';

        console.log(result.id)

        fetchCall(`${FOLLOWEE_URL}/${result.id}`, "PUT", {follow: true}, null, null);
    }
    const data = {url: webid};
    fetchCall(AUTHORS_URL, "POST", data, successfunc, null, "json");
}

function toggleFollow(e, el) {
    e.preventDefault();
    const id = get_id(el.id)
    const fcheck = el.classList.contains('mute');
    const data = {follow: fcheck}
    fetchCall(`${FOLLOWEE_URL}/${id}`, "PUT", data, null, null, "json");
    if (fcheck) {
        el.classList.remove('mute');
    } else {
        el.classList.add('mute');
    }
}

function removeAuthor(e, el) {
    e.preventDefault();
    const id = get_id(el.id)
    if (confirm("Möchten sie den Nutzer wirklich entfernen?") == true) {
        fetchCall(`${AUTHOR_URL}/${id}`, "DELETE", null, null);
        el.parentElement.parentElement.remove(); 
    } 
}
