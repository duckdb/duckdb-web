
var callback_prefix = "https://duckdbdemo.project.cwi.nl/";
var groups_sql = "SELECT name, subgroup, display_name, description FROM parquet_scan('benchmark-results/groups.parquet') WHERE name='" + benchmark_group + "'";
var sql = "SELECT hash, date, benchmark_name, subgroups, benchmark_id, timing, success FROM parquet_scan('benchmark-results/groups/" + benchmark_group + ".parquet')";

var groups_data = undefined;
var benchmark_data = undefined;

function generate_table(expected_subgroup) {
	// iterate over the result and fetch all the benchmarks that were run
	var commits = {};
	var benchmarks = {};
	var commit_benchmarks = {}
	var entry_count = 0;
	for(var i = 0; i < benchmark_data.data[0].length; i++) {
		var commit_hash = benchmark_data.data[0][i];
		var commit_date = benchmark_data.data[1][i];
		var benchmark_name = benchmark_data.data[2][i];
		var subgroup = benchmark_data.data[3][i];
		var benchmark_id = benchmark_data.data[4][i];
		var benchmark_timing = benchmark_data.data[5][i];
		var benchmark_success = benchmark_data.data[6][i];
		commits[commit_hash] = commit_date;
		if (expected_subgroup !== true && subgroup !== expected_subgroup) {
			continue;
		}
		entry_count++;
		if (commit_benchmarks[commit_hash] === undefined) {
			commit_benchmarks[commit_hash] = {};
		}
		commit_benchmarks[commit_hash][benchmark_name] = [benchmark_timing, benchmark_success];
		benchmarks[benchmark_name] = benchmark_id;
	}
	if (entry_count == 0) {
		return "";
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

	var table_html = '<table class="table bench">'
	table_html += '<tr class="table-header"><th></th>';
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
	table_html += '</table>'
	return table_html;
}

function generate_group_benchmarks() {
	var html = "";
	if (groups_data === "" || groups_data.data.length == 0 || groups_data.data[0].length == 0) {
		html = generate_table(true);
	} else {
		for(var i = 0; i < groups_data.data[0].length; i++) {
			var subgroup = groups_data.data[1][i];
			var render_name = groups_data.data[2][i];
			var description = groups_data.data[3][i];
			var table_html = generate_table(subgroup);
			if (table_html === '') {
				continue;
			}
			if (subgroup !== undefined) {
				html += "<h1>" + render_name + "</h1>";
			}
			if (description !== undefined) {
				html += "<div>" + description + "</div>";
			}
			html += table_html;
		}
	}
	$('#benchmark-table').html(html);
}


$.ajax({
	dataType: 'jsonp',
	jsonp: 'callback',
	data: {q: groups_sql},
	url: callback_prefix + '/query?callback=?',
	success: function(data) {
		$(document).ready(function() {
			if (!data.success) {
				$("#benchmark-header").html("Failed to query database: " + data.error);
				return;
			}
			groups_data = data;
			if (benchmark_data != undefined) {
				generate_group_benchmarks();
			}
		});
	}
});
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
			benchmark_data = data;
			if (groups_data != undefined) {
				generate_group_benchmarks();
			}
		});
	}
});
