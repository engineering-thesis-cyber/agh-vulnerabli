LAB_MAP = {
    1: "webgoat",
    2: "dsvw",
    3: "bwapp",
    4: "YOUR_APP_NAME",
    # 5: "Placeholder",
}

DESCRIPTIONS = {
    "webgoat": "WebGoat image - limited to only one copy",
    "dsvw": "DSVW - Everything in one place to test your basic skills",
    "bwapp": "bWAPP - Web vulnerabilities, master challenges from SQL to XSS.",
    "YOUR_APP_NAME": "Placeholder for custom application",
    # "Name": "Placeholder",
}


def setup_app():
    adjust_onload_js()
    data = list(dict())
    for key in LAB_MAP:
        entry = dict()
        entry["name"] = f"Lab {key} - {LAB_MAP[key]}"
        entry["description"] = (
            f"{DESCRIPTIONS[LAB_MAP[key]]}<br>"
            f'<button class="button info" onclick="openPopup(\'./static/assets/writeups/writeup_lab{key}.md\')">Walkthrough</button>'
            '<div id="popup" class="popup">'
            '<div class="popup-content">'
            '<span class="close" onclick="closePopup()">&times;</span>'
            '<div id="markdown-content"></div>'
            "</div>"
            "</div>"
        )
        if key == 1:
            entry[
                "copies"
            ] = f'<input type="number" id="machine-copies{key}" name="quantity" min="1" max="1">'
        else:
            entry[
                "copies"
            ] = f'<input type="number" id="machine-copies{key}" name="quantity" min="1" max="20">'
        entry[
            "create"
        ] = f'<button class="button green" onclick="createPod({key})">Create</button>'
        entry[
            "delete"
        ] = f'<button class="button red" onclick="deletePod({key})">Delete</button>'
        entry[
            "info"
        ] = f'<button class="button info" onclick="info({key})" id="lab{key}">Info</button>'
        entry["running"] = (
            f'<select id="machines{key}" name="machines{key}">'
            '<option value="NA">NA</option>'
            "</select>"
        )
        entry[
            "reset"
        ] = f'<button class="button restart" onclick="restart({key})" id="lab{key}">Restart</button>'
        data.append(entry)
    return data


def adjust_onload_js():
    from re import sub

    with open("./static/js/onload.js", "r") as file:
        file_content = file.read()

    expression = "<\s(\d+)"
    modified_content = sub(expression, f"< {len(LAB_MAP)+1}", file_content)

    with open("./static/js/onload.js", "w") as file:
        file.write(modified_content)
