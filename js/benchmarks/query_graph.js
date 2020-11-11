var callback_prefix = "https://duckdbdemo.project.cwi.nl/";
var urlParams = new URLSearchParams(window.location.search);
if (!urlParams.has('id')) {
	$("#meta-info").html("No benchmark specified, expected ?id={id}");
}
if (!urlParams.has('commit')) {
	$("#meta-info").html("No benchmark specified, expected ?commit={commit}");
}

benchmark_id = urlParams.get('id');
commit_hash = urlParams.get('commit');

var sql = "select profile from parquet_scan('benchmark-results/benchmarks/" + benchmark_id + ".parquet') where hash='" + commit_hash + "'";

$.ajax({
	dataType: 'jsonp',
	jsonp: 'callback',
	data: {q: sql},
	url: callback_prefix + '/query?callback=?',
	success: function(data) {
		$(document).ready(function() {
			if (!data.success) {
				$("#meta-info").html("Failed to query database: " + data.error);
				return;
			}
			if (data.data.length == 0) {
				$("#meta-info").html("No query graph found");
				return;
			}
			result = parse_profiling_output(data.data[0][0])
			var meta_info = result[0]
			var graph_data = result[1]
			$('#meta-info').html(meta_info)
			if (graph_data === null || graph_data === undefined) {
				return;
			}
			create_graph(graph_data, '#query-profile', '.chart')
		});
	}
});
