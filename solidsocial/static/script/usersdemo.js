document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-author').addEventListener('click', function(event) {
            event.preventDefault();
            demoNotice("Adding new users");
        });
    const followbuttons = document.querySelectorAll('button.follow');
    followbuttons.forEach(el => el.addEventListener('click', event => { demoNotice("Changing follow status")}, false));

    const removebuttons = document.querySelectorAll('button.u-remove');
    removebuttons.forEach(el => el.addEventListener('click', event => { demoNotice("Removing users")}, false));

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

function demoNotice(info) {
    alert(`${info} disable in demo modus.`);
}
