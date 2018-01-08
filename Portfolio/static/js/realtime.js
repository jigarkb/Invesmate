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
    var positions = response["positions"];
    var position_index = response["position_index"];

    var main_table = $('#main_table').DataTable({
        data: positions,
        paging: false,
        deferRender: true,
        order: [[ 3, 'desc' ]],
        columnDefs: [
            {
                data: null,
                targets: 0,
                sortable: false,
                render: function (data, type, row) {
                    return "<div style='font-size: medium'>" + row["symbol"] +
                        "</br><div style='font-size: x-small'>" + row["market"] + "</div></div>";
                }
            },
            {
                data: null,
                targets: 1,
                sortable: true,
                defaultContent: -1,
                render: {
                    _: function (data, type, row) {
                        return "<div style='font-size: medium'>" + row["shares"].toFixed(4) +
                            "</br><div style='font-size: x-small'></div></div>";
                    },
                    sort: "shares",
                    type: "numerical"
                }
            },
            {
                data: null,
                targets: 2,
                sortable: true,
                defaultContent: -1,
                render: {
                    _: function (data, type, row) {
                        return "<div style='font-size: medium'>" + row["cost_price"].toFixed(2) +
                        "</br><div style='font-size: x-small'>" + row["cost_price_ps"].toFixed(2) + "</div></div>";
                    },
                    sort: "cost_price",
                    type: "numerical"
                }
            },
            {
                data: null,
                targets: 3,
                sortable: true,
                defaultContent: -1,
                render: {
                    _: function (data, type, row) {
                        return "<div style='font-size: medium'>" + row["market_price"].toFixed(2) +
                            "</br><div style='font-size: x-small'>" + row["market_price_ps"].toFixed(2) + "</div></div>";
                    },
                    sort: "market_price",
                    type: "numerical"
                }
            },
            {
                data: null,
                targets: 4,
                sortable: true,
                defaultContent: -1,
                render: {
                    _: function (data, type, row) {
                        var color = "#ff333a";
                        var sign = "";
                        if(row["24hr_change"] >= 0){
                            color = "#093";
                            sign = "+";
                        }
                        return "<div style='font-size: medium; color: "+color+";'>" + sign + Number(row["24hr_change"].toFixed(2)) +
                            "</br><div style='font-size: x-small'>" + sign + row["24hr_change_%"].toFixed(2) + "%</div></div>";
                    },
                    sort: "24hr_change",
                    type: "numerical"
                }
            },
            {
                data: null,
                targets: 5,
                sortable: true,
                defaultContent: -1,
                render: {
                    _: function (data, type, row) {
                        var color = "#ff333a";
                        var sign = "";
                        if(row["overall_change"] >= 0){
                            color = "#093";
                            sign = "+"
                        }
                        return "<div style='font-size: medium; color: "+color+";'>" + sign + row["overall_change"].toFixed(2) +
                            "</br><div style='font-size: x-small'>" + sign + row["overall_change_%"].toFixed(2) + "%</div></div>";
                    },
                    sort: "overall_change",
                    type: "numerical"
                }
            }
        ]
    });


    var reset_current_holding = function (data) {
        var quote = data.val();
        var path_list = data["ref"]["path"]["n"];
        symbol_ref = path_list[0]+"/"+path_list[1]+"/"+path_list[2];
        var position = positions[position_index[symbol_ref]];
        position["market_price_ps"] = quote['latestPrice'];
        position["market_price"] = quote['latestPrice']*position["shares"];
        position["overall_change"] = position["market_price"] - position["cost_price"];
        position["overall_change_%"] = 100*(position["market_price"] - position["cost_price"])/position["cost_price"];
        position["24hr_change"] = position["shares"]*(quote["latestPrice"]-quote["previousClose"]);
        position["24hr_change_%"] = 100*(quote["latestPrice"]-quote["previousClose"])/quote["previousClose"];

        for(var i = 0; i < position["lots"].length; i++){
            var lot = position["lots"][i];
            lot["market_price_ps"] = quote['latestPrice'];
            lot["market_price"] = quote['latestPrice']*lot["shares"];
            lot["overall_change"] = lot["market_price"] - lot["cost_price"];
            lot["overall_change_%"] = 100*(lot["market_price"] - lot["cost_price"])/lot["cost_price"];
            lot["24hr_change"] = lot["shares"]*(quote["latestPrice"]-quote["previousClose"]);
            position["24hr_change_%"] = 100*(quote["latestPrice"]-quote["previousClose"])/quote["previousClose"];

        }
        main_table.clear().rows.add(positions).draw();
        response["market_price"] = 0;
        response["24hr_change"] = 0;

        for(var holding in positions){
            response["market_price"]+=positions[holding]["market_price"];
            response["24hr_change"]+=positions[holding]["24hr_change"];
        }
        response["overall_change"] = response["market_price"] - response["cost_price"];
        response["overall_change_%"] = 100*(response["overall_change"]/response["cost_price"]);
        response["24hr_change_%"] = 100*response["24hr_change"]/(response["market_price"] - response["24hr_change"]);
        if(response["overall_change"] < 0){
            $("#odo_total_gain").css('color', '#ff333a').html(response["overall_change"]);
            $("#odo_total_gain_pc").css('color', '#ff333a').html(response["overall_change_%"]);
            $("#odo_total_gain_pc_p").css('color', '#ff333a');

            $('#odo_total').css('color', "#ff333a").html(response["market_price"]);
            $('#odo_total_p').css('color', "#ff333a");
        }else{
            $("#odo_total_gain").css('color', '#093').html(response["overall_change"]);
            $("#odo_total_gain_pc").css('color', '#093').html(response["overall_change_%"]);
            $("#odo_total_gain_pc_p").css('color', '#093');

            $('#odo_total').css('color', "#093").html(response["market_price"]);
            $('#odo_total_p').css('color', "#093");
        }

        if(response["24hr_change"] < 0){
            $("#odo_day_gain").css('color', '#ff333a').html(response["24hr_change"]);
            $("#odo_day_gain_pc").css('color', '#ff333a').html(response["24hr_change_%"]);
            $("#odo_day_gain_pc_p").css('color', '#ff333a');
        }else{
            $("#odo_day_gain").css('color', '#093').html(response["24hr_change"]);
            $("#odo_day_gain_pc").css('color', '#093').html(response["24hr_change_%"]);
            $("#odo_day_gain_pc_p").css('color', '#093');
        }


    };

    for(var symbol_ref in position_index){
        (function (symbol_ref) {
            firebase.database().ref(symbol_ref).on('child_changed', reset_current_holding);
            firebase.database().ref(symbol_ref).on('child_added', reset_current_holding);
        })(symbol_ref)
    }
};

