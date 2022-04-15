var socket = new WebSocket('ws://10.2.12.208:7000/', );
let scale = true;
console.log("Hello");

function autoscale() {
    let btn = document.getElementById("btnScale");
    scale = !scale;
    btnScale.innerText = (scale == true) ? "Scale" : "No Scale";
    if (scale) {
        socket.send("true");
    }
    else {
        socket.send("false");
    }
}

socket.onmessage = function (message) {
    console.log(message);
    console.log(message.data);
    data = JSON.parse(message.data);
    plot_workload(data.workload);
    plot_response_time(data.response_time);
    plot_application_size(data.application_size);
}

function plot_workload(data) {
    workload_plot = document.getElementById('workload_plot');
    console.log(data);
    var layout = {
        title: "Workload Plot",
        xaxis: {
            title: "Time",
            autorange: true
        },
        yaxis: {
            title: "Requests/sec",
            autorange: true
        }
    };
    var trace = {
        mode: "lines",
        type: "scatter",
        x: data.x,
        y: data.y
    };
    Plotly.newPlot(workload_plot, [trace], layout);
}

function plot_response_time(data) {
    response_time_plot = document.getElementById('response_time_plot');
    console.log(data);
    var layout = {
        title: "Response Time Plot",
        xaxis: {
            title: "Time",
            autorange: true
        },
        yaxis: {
            title: "Avg Response Time",
            autorange: true
        }
    };
    var trace = {
        mode: "lines",
        type: "scatter",
        x: data.x,
        y: data.y
    };
    Plotly.newPlot(response_time_plot, [trace], layout);
}

function plot_application_size(data) {
    application_size_plot = document.getElementById('application_size_plot');
    console.log(data);
    var layout = {
        title: "Application Size Plot",
        xaxis: {
            title: "Time",
            autorange: true
        },
        yaxis: {
            title: "Number of replicas",
            autorange: true
        }
    };
    var trace = {
        mode: "lines",
        type: "scatter",
        x: data.x,
        y: data.y
    };
    Plotly.newPlot(application_size_plot, [trace], layout);
}