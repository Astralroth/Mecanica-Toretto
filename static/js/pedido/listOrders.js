class conn {
    data = null

    connectar() {
        var request = $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'getData'
            },
            async: false,
        })
        this.data = request.responseJSON
        return request.status
    }
}

function getData(data) {
    var tbl = $('#tbl').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        data: data,
        columns: [{
                data: 'id',
            },
            {
                data: 'name',
            },
            {
                data: 'state'
            },
            {
                data: 'options'
            }
        ],
        columnDefs: [{
            targets: [-1],
            class: 'text-center',
            orderable: false,
            // * Para cambiar las opciones
            render: function (data, type, row, meta) {
                if (row.estadoss != "Cerrada") {
                    var buttons = ''
                    buttons += '<btn id="' + row.id + '" rel="edit" class="btn btn-warning btn-xs btn-flat m-1"><i class="fas fa-edit"></i></btn> ';
                    buttons += '<btn id="' + row.id + '" rel="detail" class="btn btn-info btn-xs btn-flat m-1"><i class="fas fa-info-circle"></i></btn>';
                    return buttons;
                } else {
                    if (row.estadoss == "Cerrada" && row.usertype == "Administrador") {
                        var button = '<btn id="' + row.id + '" rel="enable" class="btn btn-primary btn-xs btn-flat m-1"><i class="fas fa-backward"></i></btn> ';
                        return button;
                    } else {
                        return '';
                    }
                }
            }
        }]
    })

    return tbl;
}

function getProductList(data, products) {
    var tbl = $('#productList').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        searching: false,
        paging: false,
        info: false,
        data: data,
        order: [1, 'desc'],
        columns: [{
                data: 'product',
                render: function (data, type, row, meta) {
                    options = '<option value=""> - - - </option>'
                    for (var prod in products) {
                        if (products[prod] == row.product) {
                            options += `<option value="${products[prod]}" selected>${products[prod]}</option>`
                        } else {
                            options += `<option value="${products[prod]}">${products[prod]}</option>`
                        }
                    }
                    return `<select name="selectProduct" id=${meta.row} required> ${options} </select>`
                },
            },
            {
                data: 'quantity',
                render: function (data, type, row, meta) {
                    return `<input type="number" name="quantity" id=${meta.row} min="1" value="${row.quantity}" required>`
                }
                // createdCell: function (td, cellData, rowData, row, col) {
                //     // add contenteditable attribute
                //     $(td).attr('contenteditable', true);
                // }
            },
            {
                data: 'options',
                render: function (data, type, row, meta) {
                    var buttons = ''
                    buttons += '<btn id="' + meta.row + '" rel="del" class="btn btn-danger btn-xs btn-flat m-1"><i class="fas fa-xmark"></i></btn> ';
                    return buttons;
                }
            }
        ],
        // columnDefs: [{
        //     targets: [-1],
        //     class: 'text-center',
        //     orderable: false,
        //     // * Para cambiar las opciones
        //     render: function (data, type, row, meta) {
        //         console.log(row.quantity)
        //         var buttons = ''
        //         buttons += '<btn id="' + meta.row + '" rel="edit" class="btn btn-danger btn-xs btn-flat m-1"><i class="fas fa-xmark"></i></btn> ';
        //         return buttons;
        //     }
        // }]
    })
    return tbl;
}

$(function () {
    var con = new conn()
    con.connectar()

    var tbl = getData(con.data['data'])

    var tblProd = getProductList([], con.data['products'])

    function limitar() {
        var cellData = tblProd.rows().data();
        var options = $('select').children()
        for (var i = 0; i < options.length; i++) {
            for (var j = 0; j < cellData.length; j++) {
                if (options[i].value == cellData[j].product) {
                    options[i].disabled = true
                }
                // si hay un producto restante desahabilita la primera opcion
                if (options[i].value == "" && cellData.length < con.data['products'].length) {
                    options[i].disabled = true
                }
            }
        }
    }

    $('#addProduct').on('click', (e) => {
        // si ya se agregaron todos los productos no se agrega otro
        if (tblProd.data().count() == con.data['products'].length) {
            return
        } else {
            tblProd.rows.add([{
                "product": "",
                "quantity": 1,
            }]).draw(false);
        }
    })

    tbl.on('click', 'btn[rel="edit"]', (e) => {
        var cellData = tbl.row(e.currentTarget.id).data();
        $('input[name="action"]').val('edit')
        $('input[name="id"]').val(cellData.id)
        $('input[name="name"]').val(cellData.name).attr('disabled', true)

        tblProd.rows.add(cellData.json).draw(false);

        $('#myModalClient').modal('show')
    })

    tblProd.on('change', 'select', (e) => {
        var cellData = tblProd.row(e.currentTarget.id).data();
        cellData.product = e.currentTarget.value
        tblProd.row(e.currentTarget.id).data(cellData).draw();
    })

    tblProd.on('change', 'input', (e) => {
        var cellData = tblProd.row(e.currentTarget.id).data();
        cellData.quantity = e.currentTarget.value
        tblProd.row(e.currentTarget.id).data(cellData).draw();
    })

    tblProd.on('click', 'btn[rel="del"]', (e) => {
        tblProd.row(e.currentTarget.parentNode.parentNode).remove().draw();
    })

    tblProd.on('draw', (e) => {
        limitar()
    })

    $('#myModalClient').on('show.bs.modal', (e) => {
        limitar()
    })

    $('#myModalClient').on('click', '.close', (e) => {
        $('#myModalClient').modal('hide')
        tblProd.clear()
    })

    $('#myModalClient').on('hide.bs.modal', (e) => {
        tblProd.clear()
        tbl.clear()
        tbl.rows.add(con.data['data']).draw()
    })

    $('btn[rel="detail"]').on('click', (e) => {
        e.preventDefault()
        var parameters = []
        parameters.push({
            name: 'id',
            value: e.currentTarget.id
        })

        var postdata = JSON.stringify(parameters)
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'detail',
                'data': postdata
            },
            async: false,
            success: function (data) {
                window.location.href = data.url
            }
        })
    })

    $('#modalForm').on('submit', (e) => {
        e.preventDefault()
        var parameters = []
        parameters.push({
            name: 'id',
            value: $('input[name="id"]').val()
        })
        var action = $('input[name="action"]').val()

        parameters.push(tblProd.data().toArray())

        var postdata = JSON.stringify(parameters)
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': action,
                'data': postdata
            },
            success: function (data) {
                con.connectar()
                $('#myModalClient').modal('hide')
            }
        })
    })
})