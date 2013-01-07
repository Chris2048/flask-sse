    jQuery( function($) {
        var data = [];
        function get_data(yval) {
            while (data.length != 300) {
                data.push(0);
            }
            data = data.slice(1);
            data.push(yval);
            // zip the generated y values with the x values
            var res = [];
            for (var i = 0; i < data.length; ++i) {
                res.push([i, data[i]]); }
            return res;
        }

        var data2 = [];
        function get_data2(yval) {
            while (data2.length != 300) {
                data2.push(0);
            }
            data2 = data2.slice(1);
            data2.push(yval);
            // zip the generated y values with the x values
            var res = [];
            for (var i = 0; i < data2.length; ++i) {
                res.push([i, data2[i]]); }
            return res;
        }

        var options = {
            series: { shadowSize: 0 },
            lines: { show: true, fill: true },
            yaxis: { show: false, min: 0, max: 100 },
            xaxis: { show: false }
        };

        d1 = get_data2(0);
        d2 = get_data(0);
        
        var plot = $.plot( $("#gplot"),
            [ { data: d1 }, { data: d2 } ], options
        );


        function update_gplot(yval) {
            d2 = get_data(yval);
            plot.setData([ { data: d1 }, { data: d2 } ]);
            plot.draw();
        }
        function update_gplot2(yval) {
            d1 = get_data2(yval);
            plot.setData([ { data: d1 }, { data: d2 } ]);
            plot.draw();
        }

        var source = new EventSource('/stream/periodic');
        source.addEventListener(
            'graph', function(e) {
                update_gplot(e.data);
            }, false
        );
        source.addEventListener(
            'ping', function(e) {
                $('#data').text(e.data);
            }, false
        );

        var source2 = new EventSource('/stream/redis');
        source2.addEventListener(
            'graph', function(e) {
                update_gplot2(e.data);
            }, false
        );
    } );