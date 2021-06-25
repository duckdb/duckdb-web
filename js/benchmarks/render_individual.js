var callback_prefix = "https://duckdbdemo.project.cwi.nl/";
var urlParams = new URLSearchParams(window.location.search);
if (!urlParams.has('id')) {
	$("#benchmark-header").html("No benchmark specified, expected ?id={id}");
}

benchmark_id = urlParams.get('id');
// initial query: fetch meta information about the benchmark
var sql = "SELECT name, \"group\", description, to_base64(images) FROM parquet_scan('benchmark-results/benchmarks.parquet') WHERE id=" + benchmark_id
$.ajax({
	dataType: 'jsonp',
	jsonp: 'callback',
	data: {q: sql},
	url: callback_prefix + '/query?callback=?',
	success: function(data) {
		$(document).ready(function() {
			if (!data.success) {
				$("#benchmark-header").html("Failed to query database: " + data.error);
				return;
			}
			if (data.data.length == 0) {
				$("#benchmark-header").html("No benchmark header data found");
				return;
			}
			var header = data.data[0][0];
			var group = data.data[1][0];
			var description = data.data[2][0];
			var image_data = data.data[3][0];
			var benchmark_html = "";
			$('.headlinebar').html(header + " - [" + group + "]")
			benchmark_html += description;
			benchmark_html += '<img src="data:image/png;base64,' + image_data + '"/>'
			$("#benchmark-header").html(benchmark_html);
		});
	}
});

var sql = "SELECT hash, date, timing, error, message FROM parquet_scan('benchmark-results/benchmarks/" + benchmark_id + ".parquet') ORDER BY date DESC";
$.ajax({
	dataType: 'jsonp',
	jsonp: 'callback',
	data: {q: sql},
	url: callback_prefix + '/query?callback=?',
	success: function(data) {
		$(document).ready(function() {
			if (!data.success) {
				$("#benchmark-header").html("Failed to query database: " + data.error);
				return;
			}
			if (data.data.length == 0) {
				$("#benchmark-header").html("No benchmark results found");
				return;
			}
			var table_html = '<tr class="table-header"><th>Commit</th><th>Date</th><th>Result</th><th>Logs</th><th>Message</th></tr>';
			var even = true;
			for(var i = 0; i < data.data[0].length; i++) {
				if (even) {
					table_html += '<tr class="table-even">';
				} else {
					table_html += '<tr class="table-odd">';
				}
				var commit_hash = data.data[0][i];
				var date = data.data[1][i].substr(0, 10);
				var timing = data.data[2][i];
				var error = data.data[3][i];
				var message = data.data[4][i];

				table_html += "<td>";
				table_html += '<a href="https://github.com/duckdb/duckdb/commit/' + commit_hash + '">';
				table_html += commit_hash.substring(0, 4)
				table_html += '</a>';
				table_html += "</td>";
				table_html += "<td>" + date + "</td>";
				if (error == undefined || error == null || !error) {
					table_html += "<td>" + timing.toFixed(2) + "</td>";
				} else {
					table_html += '<td><span color="red">E</span></td>';
				}
				// add query graph and log links
				table_html += "<td>["
				table_html += '<a href="/benchmarks/graph.html?id=' + benchmark_id + "&commit=" + commit_hash + '">Q</a>/'
				table_html += '<a href="/benchmarks/log.html?log=0&id=' + benchmark_id + "&commit=" + commit_hash + '">L</a>/'
				table_html += '<a href="/benchmarks/log.html?log=1&id=' + benchmark_id + "&commit=" + commit_hash + '">E</a>]</td>'
				table_html += "<td>" + message + "</td>";
				table_html += '</tr>'
				even = !even;
			}
			$('#benchmark-table').html(table_html);
		});
	}
});