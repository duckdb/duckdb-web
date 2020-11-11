
var callback_prefix = "https://duckdbdemo.project.cwi.nl/";
var sql = "SELECT hash, date, benchmark_name, benchmark_id, timing, success FROM parquet_scan('benchmark-results/groups/" + benchmark_group + ".parquet')";

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
			// iterate over the result and fetch all the benchmarks that were run
			var commits = {};
			var benchmarks = {};
			var commit_benchmarks = {}
			for(var i = 0; i < data.data[0].length; i++) {
				var commit_hash = data.data[0][i];
				var commit_date = data.data[1][i];
				var benchmark_name = data.data[2][i];
				var benchmark_id = data.data[3][i];
				var benchmark_timing = data.data[4][i];
				var benchmark_success = data.data[5][i];
				commits[commit_hash] = commit_date;
				if (commit_benchmarks[commit_hash] === undefined) {
					commit_benchmarks[commit_hash] = {};
				}
				commit_benchmarks[commit_hash][benchmark_name] = [benchmark_timing, benchmark_success];
				benchmarks[benchmark_name] = benchmark_id;
			}
			// order the commits by date
			var ordered_commits = [];
			for(var key in commits) {
				ordered_commits.push([key, commits[key]])
			}
			ordered_commits.sort(function(a, b) {
				if (a[1] > b[1]) {
					return -1;
				}
				if (a[1] < b[1]) {
					return 1;
				}
				return 0;
			});
			// order the benchmarks alphabetically
			var ordered_benchmarks = [];
			for(var key in benchmarks) {
				ordered_benchmarks.push(key);
			}
			ordered_benchmarks.sort();
			var table_html = '<tr class="table-header"><th></th>';
			// create the header
			for(i in ordered_commits) {
				var commit = ordered_commits[i];
				table_html += '<th class="table-active">';
				table_html += '<a href="https://github.com/cwida/duckdb/commit/' + commit[0] + '">';
				table_html += commit[0].substring(0, 4)
				table_html += '</a>';
				table_html += '</th>';
			}
			table_html += '</tr>';
			var even = true;
			for(var i in ordered_benchmarks) {
				var benchmark = ordered_benchmarks[i];
				var benchmark_id = benchmarks[benchmark];
				if (even) {
					table_html += '<tr class="table-even">';
				} else {
					table_html += '<tr class="table-odd">';
				}
				table_html += '<td class="table-row-header">';
				table_html += '<a href="/benchmarks/individual_results.html?id=' + benchmark_id + '">' + benchmark + '</a>'
				table_html += '</td>';
				for(i in ordered_commits) {
					var commit = ordered_commits[i][0];
					table_html += '<td>';
					if (commit_benchmarks[commit] === undefined) {
						table_html += '?';
					} else if (commit_benchmarks[commit][benchmark] === undefined) {
						table_html += '-';
					} else {
						var timing = commit_benchmarks[commit][benchmark][0];
						var success = commit_benchmarks[commit][benchmark][1];
						if (success) {
							table_html += timing.toFixed(2);
						} else {
							table_html += "E";
						}
					}
					table_html += " ["
					table_html += '<a href="/benchmarks/graph.html?id=' + benchmark_id + "&commit=" + commit + '">Q</a>/'
					table_html += '<a href="/benchmarks/log.html?log=0&id=' + benchmark_id + "&commit=" + commit + '">L</a>/'
					table_html += '<a href="/benchmarks/log.html?log=1&id=' + benchmark_id + "&commit=" + commit + '">E</a>]'
					table_html += '</td>';
				}
				table_html += '</tr>';
				even = !even;
			}
			$('#benchmark-table').html(table_html);
		});
	}
}); // </ajax()>
