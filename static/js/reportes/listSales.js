class conn {
    data = null
    init_date = moment().format('YYYY-MM-DD')
    end_date = moment().format('YYYY-MM-DD')

    connectar() {
        console.log(this.init_date)
        console.log(this.end_date)
        var request = $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_sales',
                'init_date': this.init_date,
                'end_date': this.end_date
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
        paging: true,
        info: true,
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
        dom: 'Bfrtlp',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['20%','20%','15%','15%','15%','15%'];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
    })

    return tbl;
}

var date_range = null;

$(function () {
    var con = new conn()
    con.connectar()

    // Cargamos el rango de fechas
    $('input[name="dates"]').daterangepicker()

    // Cargamos la tabla
    var tbl = getData(con.data['data'])

    $('input[name="dates"]').on('apply.daterangepicker', function (ev, picker) {
        console.log(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'))
        date_range = picker
        con.init_date = date_range.startDate.format('YYYY-MM-DD')
        con.end_date = date_range.endDate.format('YYYY-MM-DD')
        con.connectar()
        tbl = getData(con.data['data'])
    })
})