function showHide (container_class) {
    let items = document
                    .querySelectorAll(container_class);
    for (let item of items) {
        if (item.style.display == "none"){
            item.setAttribute("style", "display:block;")
        } else {
            item.setAttribute("style", "display:none;")
        }
    }
}

