function fetchCall(url, method, data, success=()=>null, error=null, ctype=null) {
    const errorfunc = () => {
        if (typeof error === "function") {
            error();
        } else {
            alert(`${method} call to ${url} failed`);
        }
    }   
    let fetch_data = {method: method, body: data};
    if (ctype == "json"){
        fetch_data.headers = {"Content-Type": "application/json",};
        fetch_data.body = JSON.stringify(data);
    }
    fetch(url, fetch_data )
        .then(res => res.json())
        .then( res => success)
        .catch(error => {
            console.error('Error:', error);
            errorfunc();
        });
};

function get_id(text, part=0, seperator='-') {
    return text.split(seperator)[part]
}
