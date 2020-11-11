var callback_prefix = "https://duckdbdemo.project.cwi.nl/";
var urlParams = new URLSearchParams(window.location.search);
if (!urlParams.has('id')) {
	$("#log-data").html("No benchmark specified, expected ?id={id}");
}
if (!urlParams.has('commit')) {
	$("#log-data").html("No benchmark specified, expected ?commit={commit}");
}
if (!urlParams.has('log')) {
	$("#log-data").html("No benchmark specified, expected ?log={0,1}");
}

var benchmark_id = urlParams.get('id');
var commit_hash = urlParams.get('commit');
var log = urlParams.get('log');

var log_param;
if (log == "0") {
	log_param = "stdout";
} else {
	log_param = "stderr";
}
$('.headlinebar').html(log_param + " output");

var sql = "select " + log_param + " from parquet_scan('benchmark-results/benchmarks/" + benchmark_id + ".parquet') where hash='" + commit_hash + "'";

$.ajax({
	dataType: 'jsonp',
	jsonp: 'callback',
	data: {q: sql},
	url: callback_prefix + '/query?callback=?',
	success: function(data) {
		$(document).ready(function() {
			if (!data.success) {
				$("#log-data").html("Failed to query database: " + data.error);
				return;
			}
			if (data.data.length == 0) {
				$("#log-data").html("No query graph found");
				return;
			}
			var log_data = data.data[0][0];
			$("#log-data").html("<pre>" + log_data + "</pre>");
		});
	}
});
