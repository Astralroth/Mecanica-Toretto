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
                data: 'nombre',
            },
            {
                data: 'provider'
            },
            {
                data: 'precio'
            },
            {
                data: 'estado'
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
                    buttons += '<btn id="' + meta.row + '" rel="edit" class="btn btn-warning btn-xs btn-flat m-1"><i class="fas fa-edit"></i></btn> ';
                    return buttons;
                } else {
                    if (row.estadoss == "Cerrada" && row.usertype == "Administrador") {
                        var button = '<btn id="' + meta.row + '" rel="enable" class="btn btn-primary btn-xs btn-flat m-1"><i class="fas fa-backward"></i></btn> ';
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


$(function () {
    var con = new conn()
    con.connectar()

    var tbl = getData(con.data['data'])

    
    tbl.on('click', 'btn[rel="edit"]', (e) => {
        var cellData = tbl.row(e.currentTarget.id).data();
        $('input[name="action"]').val('edit')
        $('input[name="id"]').val(cellData.id)
        $('input[name="nombre"]').val(cellData.nombre)
        $('input[name="descripcion"]').val(cellData.descripcion)
        $('select[name="provider"]').val(cellData.provider)
        $('input[name="precio"]').val(cellData.precio)
        $('select[name="estado"]').val(cellData.estado)

        $('#myModalClient').modal('show')
    })


    $('#myModalClient').on('click', '.close', (e) => {
        $('#myModalClient').modal('hide')
    })

    $('#myModalClient').on('hide.bs.modal', (e) => {
        tbl.clear()
        tbl.rows.add(con.data['data']).draw()
    })

    $('#modalForm').on('submit', (e) => {
        e.preventDefault()
        var parameters = []
        parameters.push({
            name: 'id',
            value: $('input[name="id"]').val()
        })
        var action = $('input[name="action"]').val()

        parameters.push(tbl.data().toArray()[0])

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