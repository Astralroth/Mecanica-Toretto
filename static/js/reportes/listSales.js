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
        order: false,
        paging: false,
        info: false,
        searching: false,
        columns: [{
                data: 'id',
            },
            {
                data: 'fecha',
            },
            {
                data: 'run'
            },
            {
                data: 'subtotal'
            },
            {
                data: 'impuesto'
            },
            {
                data: 'total'
            },
        ],
        dom: 'Bfrtip',
        buttons: [
            'excel', 'pdf'
        ]
    })

    return tbl;
}

$(function () {
    var con = new conn()
    con.connectar()

    var tbl = getData(con.data['data'])
    
    // $('#modalForm').on('submit', (e) => {
    //     e.preventDefault()
    //     var parameters = []
    //     parameters.push({
    //         name: 'id',
    //         value: $('input[name="id"]').val()
    //     })
    //     var action = $('input[name="action"]').val()

    //     parameters.push(tblProd.data().toArray())

    //     var postdata = JSON.stringify(parameters)
    //     $.ajax({
    //         url: window.location.pathname,
    //         type: 'POST',
    //         data: {
    //             'action': action,
    //             'data': postdata
    //         },
    //         success: function (data) {
    //             con.connectar()
    //             $('#myModalClient').modal('hide')
    //         }
    //     })
    // })
})