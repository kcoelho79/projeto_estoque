$( function() {


    // document.getElementById("movimentacao").onclick =  function () {
    //     alert("apertou botao de movimentacao")
    //     console.log("teste")

    // }

    $("#movimentacao").click( function () {
        alert("jquery esta funconado")
    })


    // funcao retornar data hoje (now)
    
    function data_hoje(padrao) {
        // arg padrao br - data no formato dd/mm/yyyy
        // us = yyyy-mm-dd  
        var padrao         
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1; //January is 0!

        var yyyy = today.getFullYear();
        if (dd < 10) {
        dd = '0' + dd;
        } 
        if (mm < 10) {
        mm = '0' + mm;
        } 

        if (padrao == 'br'){
            var today = dd + '/' + mm + '/' + yyyy;
        }if (padrao == 'us') {
            var today = yyyy + '-' + mm + '-' + dd;
        }
        return  today;
    }
    
    

    // estoque.html
    // configuracoes datapicker

    $("#datepicker_data").val(data_hoje('us'));


    $( "#datepicker_data" ).datepicker({
        format: "yyyy-mm-dd",
        startDate: "2019-01-01",
        todayBtn: true,
        todayHighlight: true,
        language: "pt-BR",
        autoclose: true,
        multidateSeparator: "-"

    });

    // estoque_detalhe.html
    // configuracoes dos Datapicker

    $( "#datepicker_inicial" ).datepicker({
        format: "dd/mm/yyyy",
        startDate: "01/01/2019",
        todayBtn: true,
        todayHighlight: true,
        language: "pt-BR",
        autoclose: true

    });

    $( "#datepicker_final" ).datepicker({
        dateFormat: "dd/mm/yyyy",
        startDate: "01/01/2019",
        todayBtn: true,
        todayHighlight: true,
        language: "pt-BR",
        autoclose: true

    });


  
} );
