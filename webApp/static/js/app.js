$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newData', function(msg) {
        var d = JSON.parse(msg.data)
        var ctx = document.getElementById('myChart').getContext('2d');
        var chart = new Chart(ctx, {
            type: 'line',
            data: d,
            options: {}
        });
    });

    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {},
        options: {}
    });

    
    $('#dateForm').submit(function(){
        socket.emit('charts', [$('#dateFrom').val(),$('#dateTo').val(),$('#freq').val()]);
        return false;
    });

    $("#dateRange").dateRangePicker({
        separator: " to ",
        getValue: function() {
        if ($("#dateFrom").val() && $("#dateTo").val())
            return $("#dateFrom").val() + " to " + $("#dateTo").val();
        else return "";
        },
        setValue: function(s, s1, s2) {
            $("#dateFrom").val(s1);
            $("#dateTo").val(s2);
        },
        startOfWeek: "monday",
        format: "DD/MM/YYYY"
    });
});
