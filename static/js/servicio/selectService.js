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

$(function () {
    var con = new conn()
    con.connectar()
    console.log(con.data['services'])

    // cycle for to add options to select
    for (var i = 0; i < con.data['services'].length; i++) {
        $('#selectService').append('<option value="' + con.data['services'][i]['id'] + '">' + con.data['services'][i]['nombre'] + '</option>')
    }

    $('#selectService').selectpicker({
        liveSearch: true,
        selectedTextFormat: 'count > 1',
    });

    var subtotal = 0
    var tax = 0
    var total = 0

    // on select some services change subtotal, tax and total values
    $('#selectService').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
        var service = con.data['services'][clickedIndex]

        var selsubtotal = Number(service['precio'])
        // if service is selected add values, else remove values
        if (isSelected) {   
            subtotal += selsubtotal
        }
        else {
            subtotal -= selsubtotal
        }

        tax = subtotal * 0.19
        total = subtotal + tax

        console.log(subtotal)
        console.log(tax)
        console.log(total)
        // set values to html

        if(subtotal > 0){
        $("input[name='subtotal']").val(subtotal)
        $("input[name='impuesto']").val(tax)
        $("input[name='total']").val(total)
        }
        else{
            $("input[name='subtotal']").val('')
            $("input[name='impuesto']").val('')
            $("input[name='total']").val('')
        }
    })
    $('#modalForm').on('submit', (e) => {
        e.preventDefault()
        var parameters = []
        parameters.push({
            firstname: $('input[name="firstname"]').val(),
            lastname: $('input[name="lastname"]').val(),
            run : $('input[name="run"]').val(),
            service: $('#selectService').val(),
            subtotal: $('input[name="subtotal"]').val(),
            tax: $('input[name="impuesto"]').val(),
            total: $('input[name="total"]').val(),
        })

        console.log($('#selectService').val())

        var postdata = JSON.stringify(parameters)
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'addTicket',
                'data': postdata
            },
            async: false,
            success: function (data) {
                alert("Pago agregado")
                window.location.href = data.url
            }
        })
    })
})