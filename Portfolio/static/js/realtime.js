function Realtime(){
    $.ajax({
        url: '/portfolio/fetch_all?',
        type: 'GET',
        success: function(data) {
            Realtime.prototype.load_response(data["response"]);
        },
        error: function (data) {
            // console.log(data);
        }
    });
}

Realtime.prototype.load_response = function(response){
    var positions = response["positions"];
    var position_index = response["position_index"];

    var main_table = $('#main_table').DataTable({
        responsive: true,
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
                    return "<div style='font-size: medium'>" + "<a href='#' onClick='edit_modal(this);' data-val='"+JSON.stringify(row)+"'>"+row["symbol"] + "</a>" +
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
                        var shares;
                        if(row["market"] === "US"){
                            shares = row["shares"].toFixed(2);
                        }else{
                            shares = row["shares"].toFixed(4);
                        }
                        return "<div style='font-size: medium'>" + shares +
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
            },
        ]
    });

    var reset_crypto_news = function (data) {
        var quote = data.val();
        var path_list = data["ref"]["path"]["n"];
        symbol_ref = path_list[0]+"/"+path_list[1];


        var html = "";
        for(var i=0;i<quote.length;i++){
            var symbol_class = quote[i]['source'];
            $("div."+symbol_class).remove();
            var date_str = timeConverter(quote[i]['published_on']);
            html += '<div class="list-group list-group-flush small '+ symbol_class +'">' +
                '<a class="list-group-item list-group-item-action"\n' +
                '                   target="_blank" href="'+ quote[i]["url"] +'">\n' +
                '                  <div class="media">\n' +
                '                    <div class="media-body">\n' + quote[i]['title'] +' - <strong>'+ symbol_class +'</strong>\n' +
                '                      <div class="text-muted smaller timeago" title="'+ date_str +'"></div>\n' +
                '                    </div>\n' +
                '                  </div>\n' +
                '                </a></div>';
        }
        $("#crypto_feed").prepend(html);
        $(".timeago").timeago();
    };

    var reset_current_holding = function (data) {
        var quote = data.val();
        var path_list = data["ref"]["path"]["n"];
        symbol_ref = path_list[0]+"/"+path_list[1]+"/"+path_list[2];
        var position = positions[position_index[symbol_ref]];
        if(path_list.length === 4 && path_list[3]==="news"){
            var symbol_class = path_list[2];
            $("div."+symbol_class).remove();
            var html = "";
            for(i=0;i<quote.length;i++){
                html += '<div class="list-group list-group-flush small '+ symbol_class +'">' +
                    '<a class="list-group-item list-group-item-action"\n' +
                    '                   target="_blank" href="'+ quote[i]["url"] +'">\n' +
                    '                  <div class="media">\n' +
                    '                    <div class="media-body">\n' +
                    '                      <strong>'+ symbol_class +': </strong>'+ quote[i]['headline'] +' - '+ quote[i]['source'] +'\n' +
                    '                      <div class="text-muted smaller timeago" title="'+ quote[i]['datetime'] +'"></div>\n' +
                    '                    </div>\n' +
                    '                  </div>\n' +
                    '                </a></div>';
            }
            $("#us_market_feed").prepend(html);
            $(".timeago").timeago();
            return;
        }
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
            $("#odo_total_p_p_1").css('background-color', '#C0493C');
            $("#odo_total_p_p_2").css('background-color', '#C0493C');
            $("#odo_total_gain").html(response["overall_change"]);
            $("#odo_total_gain_pc").html(response["overall_change_%"]);

            $('#odo_total').html(response["market_price"]);
        }else{
            $("#odo_total_p_p_1").css('background-color', '#85bb65');
            $("#odo_total_p_p_2").css('background-color', '#85bb65');
            $("#odo_total_gain").html(response["overall_change"]);
            $("#odo_total_gain_pc").html(response["overall_change_%"]);

            $('#odo_total').html(response["market_price"]);
        }

        if(response["24hr_change"] < 0){
            $("#odo_day_p_p").css('background-color', '#D3241B');
            $("#odo_day_gain").html(response["24hr_change"]);
            $("#odo_day_gain_pc").html(response["24hr_change_%"]);
        }else{
            $("#odo_day_p_p").css('background-color', '#85bb65');
            $("#odo_day_gain").html(response["24hr_change"]);
            $("#odo_day_gain_pc").html(response["24hr_change_%"]);
        }


    };

    for(var symbol_ref in position_index){
        (function (symbol_ref) {
            firebase.database().ref(symbol_ref).on('child_changed', reset_current_holding);
            firebase.database().ref(symbol_ref).on('child_added', reset_current_holding);
        })(symbol_ref)
    }

    firebase.database().ref("/crypto").on('child_changed', reset_crypto_news);
    firebase.database().ref("/crypto").on('child_added', reset_crypto_news);

};

function timeConverter(UNIX_timestamp){
    var a = new Date(UNIX_timestamp * 1000);
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
    return time;
}

function edit_modal(row) {
    var data = $(row).data("val");
    console.log(data);

    var table_html = "";
    for(var i=0; i< data['lots'].length; ++i){
        table_html += "<tr>\n" +
            "\t<table style='background-color: #dddddd; width: 100%; padding: 1rem;'>\n" +
            "  <tr>\n" +
            "    <td align='left' style='padding-left: 2rem;'><b>Date Purchased</b></td>\n" +
            "    <td align='right' style='padding-right: 2rem'>"+data["lots"][i]["purchased_at"]+"</td>\n" +
            "  </tr>\n" +
            "  <tr>\n" +
            "    <td align='left' style='padding-left: 2rem;'><b>Shares<b></td>\n" +
            "    <td align='right' style='padding-right: 2rem'>"+data["lots"][i]["shares"]+"</td>\n" +
            "  </tr>\n" +
            "  <tr>\n" +
            "    <td align='left' style='padding-left: 2rem;'><b>Purchase Price<b></td>\n" +
            "    <td align='right' style='padding-right: 2rem'>"+"$"+data["lots"][i]["cost_price"]+"</td>\n" +
            "  </tr>\n" +
            "  <tr>\n" +
            "    <td align='left' style='padding-left: 2rem;'><b> Market Value<b></td>\n" +
            "    <td align='right' style='padding-right: 2rem'>"+"$"+data["lots"][i]["market_price"].toFixed(2)+"</td>\n" +
            "  </tr>\n" +
            "  <tr>\n" +
            "    <td align='left' style='padding-left: 2rem;'><b> Total Return<b></td>\n" +
            "    <td align='right' style='padding-right: 2rem'>"+"$"+data["lots"][i]["overall_change"].toFixed(2)+ " (" + data["lots"][i]["overall_change_%"].toFixed(2)+"%"+")"+"</td>\n" +
            "  </tr>\n" +
            "   \n" +
            "  </table>\n" +
            "  <br>\n" +
            "</tr>";
    }
    $("#edit_modal").html("<table>"+table_html+"</table>");

    $('#myModal').modal('show');
}