function createPod(id) {
    var xhr = new XMLHttpRequest();
    let copies_id = 'machine-copies' + id.toString();
    var data = {
        id: id,
        copies: document.getElementById(copies_id).value
    };
    xhr.open('POST', '/create', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    document.getElementById('response').innerHTML = 'Creating deployment for lab ' + id + "...";
    xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        document.getElementById('response').innerHTML = "Response from /create " + response;
        setTimeout(function() {
            location.reload();
        }, 2000);
    }
    };
    xhr.send(JSON.stringify(data));
}

function deletePod(id) {
    var xhr = new XMLHttpRequest();
    var data = {
        id: id
    };
    xhr.open('POST', '/delete', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    document.getElementById('response').innerHTML = 'Deleting deployment for lab ' + id + "...";
    xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        document.getElementById('response').innerHTML = "Response from /delete " + response;
        setTimeout(function() {
            location.reload();
        }, 2000);
    }
    };
    xhr.send(JSON.stringify(data));
}

function info(id){
    var xhr = new XMLHttpRequest();
    let machines_id = 'machines' + id.toString();
    var data = {
        id: id,
        machines_id: machines_id
    };
    xhr.open('POST', '/info', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    document.getElementById('response').innerHTML = 'Getting info for deployment ' + id + "...";
    xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        if (response.status){
            document.getElementById('response').innerHTML = 'Response from /info ' + response.pods_info;
            let select_form = "";
            response.users.forEach((user) => {
                select_form += '<option value=' + user + '>' + user + '</option>\n';
            });
            document.getElementById(machines_id).innerHTML = select_form;
        } else {
            document.getElementById('response').innerHTML = 'Response from /info ' + response.pods_info;
            document.getElementById(machines_id).innerHTML = '<option value=' + "NA" + '>' + "NA" + '</option>\n';
        }
    }
    };
    xhr.send(JSON.stringify(data));
}

function restart(id){
    var xhr = new XMLHttpRequest();
    let machines_id = 'machines' + id.toString();
    var data = {
        id: id,
        machine_id: document.getElementById(machines_id).value
    };
    console.log(data.id, data.machine_id);
    xhr.open('POST', '/restart', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    document.getElementById('response').innerHTML = 'Restarting machine for lab ' + id + ' user: ' + data.machine_id + '...';
    xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        document.getElementById('response').innerHTML = "Response from /restart " + response;
        setTimeout(function() {
            location.reload();
        }, 2000);
    }
    };
    xhr.send(JSON.stringify(data));
}