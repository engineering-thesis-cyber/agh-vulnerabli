window.onload = () => {
    for (let i = 1; i < 5; i++) { // Update this number accordingly to number of laboratories!
        var xhr = new XMLHttpRequest();
        let machines_id = 'machines' + i.toString();
        var data = {
            id: i
        };
        xhr.open('POST', '/statusall', false); //synchronous for running status update
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            console.log(response);
            if (response.users){
                let select_form = "";
                response.users.forEach((user) => {
                    select_form += '<option value=' + user + '>' + user + '</option>\n';
                });
                document.getElementById(machines_id).innerHTML = select_form;
            }
        }
        };
        xhr.send(JSON.stringify(data));
    }
    console.log("Page is fully loaded");
};
  