var socket = new WebSocket('wss://localhost:3000/');
console.log("Hello");

socket.onmessage = function (message) {
    console.log(message);
    console.log(message.data);
    data = JSON.parse(nessage.data);
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
            title: "Time"
        },
        yaxis: {
            title: "Requests/sec"
        }
    };
    var trace = {
        mode: "lines",
        type: "scatter",
        x: data.x,
        y: data.y
    };
    Plotly.react(workload_plot, trace, layout);
}

function plot_response_time(data) {
    response_time_plot = document.getElementById('response_time_plot');
    console.log(data);
    var layout = {
        title: "Response Time Plot",
        xaxis: {
            title: "Time"
        },
        yaxis: {
            title: "Avg Response Time"
        }
    };
    var trace = {
        mode: "lines",
        type: "scatter",
        x: data.x,
        y: data.y
    };
    Plotly.react(response_time_plot, trace, layout);
}

function plot_application_size(data) {
    application_size_plot = document.getElementById('application_size_plot');
    console.log(data);
    var layout = {
        title: "Application Size Plot",
        xaxis: {
            title: "Time"
        },
        yaxis: {
            title: "Number of replicas"
        }
    };
    var trace = {
        mode: "lines",
        type: "scatter",
        x: data.x,
        y: data.y
    };
    Plotly.react(application_size_plot, trace, layout);
}