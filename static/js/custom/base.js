
function select_items_for_sidebar(selector) {
    var line_info = $(selector);
    var parent = line_info.parents('li');
    for (var i = 0; i < parent.length; i++) {
        var node = parent[i];
        $(node).addClass("opened active");
    }
}

