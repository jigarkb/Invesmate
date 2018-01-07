function Realtime(){
    $.ajax({
        url: '/portfolio/fetch_all?',
        type: 'GET',
        success: function(data) {
            console.log(data["response"]);
            Realtime.prototype.load_response(data["response"]);
        },
        error: function (data) {
            console.log(data);
        }
    });
}

Realtime.prototype.load_response = function(response){
    main_table = $('#main_table').DataTable({
        data: response["positions"],
        // iDisplayLength: 10,
        // deferRender: true,
        order: [[ 2, 'desc' ]],
        columnDefs: [
            {
                data: null,
                targets: 0,
                sortable: false,
                render: function (data, type, row) {
                    return "<div style='font-size: medium'>" + row["symbol"] +
                        "</br><div style='font-size: smaller'>" + row["market"] + "</div></div>";
                }
            },
            {
                data: null,
                targets: 1,
                sortable: true,
                render: {
                    _: function (data, type, row) {
                        return "<div style='font-size: medium'>" + row["cost_price"] +
                        "</br><div style='font-size: smaller'>" + row["cost_price_ps"] + "</div></div>";
                    },
                    sort: "cost_price",
                    type: "numerical"
                }
            },
            {
                data: null,
                targets: 2,
                sortable: true,
                render: {
                    _: function (data, type, row) {
                        return "<div style='font-size: medium'>" + row["market_price"] +
                            "</br><div style='font-size: smaller'>" + row["market_price_ps"] + "</div></div>";
                    },
                    sort: "market_price",
                    type: "numerical"
                }
            },
            {
                data: null,
                targets: 3,
                sortable: true,
                render: {
                    _: function (data, type, row) {
                        return "<div style='font-size: medium'>" + row["24hr_change"] +
                            "</br><div style='font-size: smaller'>" + "" + "</div></div>";
                    },
                    sort: "24hr_change",
                    type: "numerical"
                }
            },
            {
                data: null,
                targets: 4,
                sortable: true,
                render: {
                    _: function (data, type, row) {
                        return "<div style='font-size: medium'>" + row["overall_change"] +
                            "</br><div style='font-size: smaller'>" + "" + "</div></div>";
                    },
                    sort: "overall_change",
                    type: "numerical"
                }
            }
        ]
    });


    // response = response["positions"];
    //
    //
    // var reset_current_holding = function (data) {
    //     var quote = data.val();
    //     var path_list = data["ref"]["path"]["n"];
    //     symbol_ref = path_list[0]+"/"+path_list[1]+"/"+path_list[2];
    //     response[symbol_ref]["market_price_ps"] = quote['latestPrice'];
    //     response[symbol_ref]["market_price"] = quote['latestPrice']*response[symbol_ref]["shares"];
    //     response[symbol_ref]["overall_change"] = response[symbol_ref]["market_price"] - response[symbol_ref]["cost_price"];
    //     response[symbol_ref]["24hr_change"] = response[symbol_ref]["shares"]*(quote["close"]-quote["previousClose"]);
    //
    //     for(var i = 0; i < response[symbol_ref]["lots"].length; i++){
    //         var lot = response[symbol_ref]["lots"][i];
    //         lot["market_price_ps"] = quote['latestPrice'];
    //         lot["market_price"] = quote['latestPrice']*lot["shares"];
    //         lot["overall_change"] = lot["market_price"] - lot["cost_price"];
    //         lot["24hr_change"] = lot["shares"]*(quote["close"]-quote["previousClose"]);
    //     }
    //     console.log(quote);
    //
    //     $('#portfolio').html(json2html.transform(response,transform));
    // };
    // for(var symbol_ref in response){
    //     (function (symbol_ref) {
    //         firebase.database().ref(symbol_ref).on('child_changed', reset_current_holding);
    //         firebase.database().ref(symbol_ref).on('child_added', reset_current_holding);
    //     })(symbol_ref)
    // }
};

