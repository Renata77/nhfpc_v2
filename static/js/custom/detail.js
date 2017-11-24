/* must apply only after HTML has loaded */


function init_table(parameters) {
    var selector = parameters.selector;
    var data = parameters.data;
    var table = $(selector);
    table.bootstrapTable({data: data})
}

function init_update_table(parameters) {
    var selector = parameters.selector;
    var data = parameters.data;
    var showExport = parameters.showExport;
    var url = parameters.url;
    var table = $(selector);
    table.bootstrapTable({
            data: data,
            showExport: showExport,
            onEditableSave: function (field, row, oldValue, $el) {
                $.ajax({
                    type: "get",
                    data: row,
                    dataType: 'JSON',
                    url: url,
                    success: function (data) {
                        console.log(data);
                    }
                });
                console.log("oldvalue", oldValue, $el);
            }

        }
    );
}

function remove_record_in_table(paramters) {
    var btn = paramters.button;
    var table = paramters.table;
    var url = paramters.url;
    $(btn).click(function () {
        var selected = $.map($(table).bootstrapTable('getAllSelections'), function (row) {
            return row.id;
        });
        var selected_des = $.map($(table).bootstrapTable('getAllSelections'), function (row) {
            return row.description;
        });
        if (selected.length < 1) {
            alert("选择删除项？");
            return
        }
        else {
            var sure = confirm("确认删除" + selected_des + "?");
            if (sure) {
                console.log($(table).bootstrapTable('getAllSelections'));
                console.log(selected);
                $.ajax({
                    url: url,
                    type: "GET",
                    contentType: "application/json; charset=utf-8",
                    data: "id=" + selected,
                    dataType: "json",
                    success: function (data, textStatus, jqXHR) {

                        // $('#modal-options-description').modal('hide');
                        // $('#create_message_success').modal('show');
                        window.location.reload();
                    }
                });
            } else {
                return
            }
        }
    });
}


function init_hospital_stat_table(parameters) {
    var selector = parameters.selector;
    var $table = $(selector);
    var helper = parameters.helper;
    var url = parameters.url;
    var showExport = parameters.showExport;
    $.ajax({
        url: url,
        type: "GET",
        data: parameters,
        success: function (data, textStatus, jqXHR) {
            $table.bootstrapTable({

                columns: [
                    [
                        {
                            title: helper,
                            field: 'option',
                            rowspan: 2,
                            align: 'center',
                            valign: 'middle',
                            editable: {

                                type: "text",

                                onblur: "submit",

                                showbuttons: false,

                                validate: function (v) {

                                    if (!v) return '不能为空';

                                }
                            }

                        }, {
                        title: '合计',
                        field: 'sum',
                        rowspan: 2,
                        align: 'center',
                        valign: 'middle'

                    },
                        {
                            title: '三级',
                            colspan: 4,
                            align: 'center',
                            valign: 'middle'
                        }, {
                        title: '二级',
                        colspan: 4,
                        align: 'center',
                        valign: 'middle'
                    }, {
                        title: '一级',
                        colspan: 4,
                        align: 'center',
                        valign: 'middle'
                    }, {
                        title: '未定级',
                        colspan: 4,
                        align: 'center',
                        valign: 'middle'
                    }
                    ],
                    [
                        {
                            field: 'level3_count',
                            title: '小计',
                            sortable: true,


                            align: 'center',
                            valign: 'middle'
                        }, {
                        field: 'level3_east',
                        title: '东部',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level3_middle',
                        title: '中部',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level3_west',
                        title: '西部',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level2_count',
                        title: '小计',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level2_east',
                        title: '东部',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level2_middle',
                        title: '中部',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level2_west',
                        title: '西部',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level1_count',
                        title: '小计',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level1_east',
                        title: '东部',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level1_middle',
                        title: '中部',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level1_west',
                        title: '西部',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level0_count',
                        title: '小计',
                        sortable: true,


                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level0_east',
                        title: '东部',
                        sortable: true,
                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level0_middle',
                        title: '中部',
                        sortable: true,
                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'level0_west',
                        title: '西部',
                        sortable: true,
                        align: 'center',
                        valign: 'middle'
                    }
                    ]
                ],
                data: data["data"],
                showExport: showExport
            });
        }


    });
}

function init_health_stat_table(parameters) {
    var selector = parameters.selector;
    var $table = $(selector);
    var helper = parameters.helper;
    var url = parameters.url;
    var showExport = parameters.showExport;
    $.ajax({
        url: url,
        type: "GET",
        data: parameters,
        success: function (data, textStatus, jqXHR) {
            $table.bootstrapTable({
                columns: [
                    [
                        {
                            title: helper,
                            field: 'option',
                            rowspan: 2,
                            align: 'center',
                            valign: 'middle',
                            editable: {
                                type: "text",
                                onblur: "submit",
                                showbuttons: false,
                                validate: function (v) {
                                    if (!v) return '不能为空';
                                }
                            }

                        },
                        {
                            title: '省级卫计委',
                            colspan: 4,
                            align: 'center',
                            valign: 'middle'
                        }, {
                        title: '市级卫计委',
                        colspan: 4,
                        align: 'center',
                        valign: 'middle'
                    }
                    ],
                    [
                        {
                            field: 'province_count',
                            title: '小计',
                            sortable: true,
                            align: 'center',
                            valign: 'middle'
                        }, {
                        field: 'province_east',
                        title: '东部',
                        sortable: true,
                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'province_middle',
                        title: '中部',
                        sortable: true,
                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'province_west',
                        title: '西部',
                        sortable: true,
                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'city_count',
                        title: '小计',
                        sortable: true,
                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'city_east',
                        title: '东部',
                        sortable: true,
                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'city_middle',
                        title: '中部',
                        sortable: true,
                        align: 'center',
                        valign: 'middle'
                    }, {
                        field: 'city_west',
                        title: '西部',
                        sortable: true,
                        align: 'center',
                        valign: 'middle'
                    }
                    ]
                ],
                data: data["data"],
                showExport: showExport
            });
        }
    })
}


function init_type_ui(parameters) {
    var theme = parameters.qid;
    var type = parameters.type;
    var ui_table = 'table_';
    var ui_chart = 'chart_';
    var ui_description = 'description_';

    /* 未添加显示 chart*/
    switch (theme) {
        case "location":
            switch (type) {
                case "1":
                case "2":
                    ui_description = '.select_table';
                    ui_table = '.health_table';
                    ui_chart = '.health_bar;.health_chart';
                    break;
                case "3":
                case "4":
                case "5":
                case "6":
                case "7":
                    ui_description = '.segment_table';
                    ui_table = '.health_table';
                    ui_chart = '.health_bar;.health_chart';

                    break;
                case "0":
                    ui_table = 'none';
                    ui_chart = 'none';
                    break;
                case "8":
                    ui_table = 'none';
                    ui_chart = '.health_word_cloud';
                    break;
                case "9":
                    ui_table = 'health_table';
                    ui_chart = '.health_bar;.health_chart';
                    break;

            }
            break;
        case "hospital":
            switch (type) {
                case "1":
                case "2":
                    ui_description = '.select_table';
                    ui_select = '.select_table';
                    ui_table = '.hospital_table';
                    ui_chart = '.hospital_bar;hospital_chart';
                    break;
                case "3":
                case "4":
                case "5":
                case "6":
                case "7":
                    ui_description = '.segment_table';
                    ui_table = '.hospital_table';
                    ui_chart = '.hospital_bar;.hospital_chart';

                    break;
                case "0":
                    ui_table = 'none';
                    ui_chart = 'none';
                    break;
                case "8":
                    ui_table = 'none';
                    ui_chart = '.hospital_word_cloud';
                    break;
            }
            break;
        case "bigdata":
            switch (type) {
                case "1":
                case "2":
                    ui_description = '.select_table';
                    ui_table = '.hospital_table;.health_table';
                    ui_chart = '.hospital_bar;.health_bar;.hospital_chart;.health_chart';
                    break;
                case "3":
                case "4":
                case "5":
                case "6":
                case "7":
                    ui_table = '.hospital_table;.health_table';
                    ui_chart = '.hospital_bar;.health_bar;.hospital_chart;.health_chart';
                    ui_description = '.segment_table';
                    break;
                case "0":
                    ui_table = 'none';
                    ui_chart = 'none';
                    break;
                case "8":
                    ui_table = 'none';
                    ui_chart = '.hospital_word_cloud';
                    break;
            }
            break;
    }
    /*
    * 默认所有模块是不显示的，按需显示
    * */
    var ui = '.hospital_table|.health_table|.hospital_bar|.health_bar|.hospital_word_cloud|.health_word_cloud|.hospital_bar|.health_bar';
    var ui_list = ui.split('|');
    for (var index in ui_list) {
        var u = ui_list[index];
        $(u).css('display', 'none');
        // console.log(u);
        // console.log('none');
    }
    if (ui_table !== 'none') {
        var ui_table_list = ui_table.split(';');
        for (selector in ui_table_list) {
            $(ui_table_list[selector]).css('display', 'block');
            console.log(ui_table_list[selector]);
            console.log('block');
        }
    }
    if (ui_chart !== 'none') {
        var ui_chart_list = ui_chart.split(';');
        for (selector in ui_chart_list) {
            $(ui_chart_list[selector]).css('display', 'block');
            console.log(ui_chart_list[selector]);
            console.log('block');
        }
    }
    if (ui_description !== 'none') {
        var ui_description_list = ui_description.split(';');
        for (selector in ui_description_list) {
            $(ui_description_list[selector]).css('display', 'block');
            console.log(ui_description_list[selector]);
            console.log('block');
        }
    }
}


