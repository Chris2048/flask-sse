jQuery ($) ->
    data = []
    data2 = []
    
    get_datax = (yval, data) ->
        data.push 0 until data.length is 300
        data = data.slice(1)
        data.push yval
        return [[i, data(i)] for i in 0..data.length]

    get_data = (yval) ->
        data.push 0 until data.length is 300
        data = data.slice(1)
        data.push yval
        [[i, data[i]] for i in [0..data.length]]

    get_data2 = (yval) ->
        data2.push 0 until data2.length is 300
        data2 = data2.slice(1)
        data2.push yval
        [[i, data2[i]] for i in [0..data2.length]]

    options =
        series:
            shadowSize: 0
        lines:
            show: true
            fill: true
        yaxis:
            show: false
            min: 0
            max: 100
        xaxis:
            show: false

    d1 = get_data2(0)
    d2 = get_data(0)
    plot = $.plot($("#gplot"), [{data: d1}, {data: d2}], options)

    update_gplot = (yval) ->
        d2 = get_data(yval)
        plot.setData [{data: d1}, {data: d2}]
        plot.draw()

    update_gplot2 = (yval) ->
        d1 = get_data2(yval)
        plot.setData [{data: d1}, {data: d2}]
        plot.draw()

    source = new EventSource("/stream_periodic")
    source.addEventListener "graph", (e) ->
        update_gplot e.data
    , false
    source.addEventListener "ping", (e) ->
        $("#data").text e.data
    , false
    source2 = new EventSource("/stream_redis")
    source2.addEventListener "graph", (e) ->
        update_gplot2 e.data
    , false