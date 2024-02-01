// Web Service Integration
var express = require('express');
var duckdb = require('duckdb');
var app = express();
var db = new duckdb.Database(':memory:');
app.get('/getnumbers', function (req, res) {
    db.all('SELECT random() AS num FROM range(10)',
    function(a, b) {
        if (a) { throw a; }
        res.end(JSON.stringify(b));
    });
})

var server = app.listen(8082, function () {
    console.log(
        "Example live at http://localhost:8082/getnumbers",
        host, port
    )
})
