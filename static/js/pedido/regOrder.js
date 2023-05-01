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

function getData(products) {
    var tbl = $('#productList').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        searching: false,
        paging: false,
        info: false,
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
    })

    return tbl;
}

$(function () {
    var con = new conn()
    con.connectar()

    console.log(con.data)
    var tbl = getData(con.data['products'])

    function limitar() {
        var cellData = tbl.rows().data();
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
        if (tbl.data().count() == con.data['products'].length) {
            return
        } else {
            tbl.rows.add([{
                "product": "",
                "quantity": 1,
            }]).draw(false);
        }
    })

    tbl.on('change', 'select', (e) => {
        var cellData = tbl.row(e.currentTarget.id).data();
        cellData.product = e.currentTarget.value
        tbl.row(e.currentTarget.id).data(cellData).draw();
    })

    tbl.on('change', 'input', (e) => {
        var cellData = tbl.row(e.currentTarget.id).data();
        cellData.quantity = e.currentTarget.value
        tbl.row(e.currentTarget.id).data(cellData).draw();
    })

    tbl.on('click', 'btn[rel="del"]', (e) => {
        tbl.row(e.currentTarget.parentNode.parentNode).remove().draw();
    })

    tbl.on('draw', (e) => {
        limitar()
    })

    $('#modalForm').on('submit', (e) => {
        e.preventDefault()
        var parameters = []
        parameters.push({
            name: $('input[name="name"]').val()
        })

        parameters.push(tbl.data().toArray())

        var postdata = JSON.stringify(parameters)
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'addOrder',
                'data': postdata
            },
            async: false,
            success: function (data) {
                con.connectar()
                $('#myModalClient').modal('hide')
            }
        })
    })
})