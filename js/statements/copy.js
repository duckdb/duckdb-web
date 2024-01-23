
function GenerateCopyFrom(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("COPY"),
			Expression("table-name"),
			GenerateOptionalColumnList(options),
			Sequence([
				Keyword("FROM"),
				Expression("file-name")
			]),
			Expandable("copy-from-options", options, "copy-from-options", GenerateCopyFromOptions)
		])
	])
}


function GenerateCopyTo(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("COPY"),
			Choice(0, [
				Sequence([
					Expression("table-name"),
					GenerateOptionalColumnList(options)
				]),
				Sequence([
					Keyword("("),
					Expression("select-node"),
					Keyword(")")
				])
			]),
			Sequence([
				Keyword("TO"),
				Expression("file-name")
			]),
			Expandable("copy-to-options", options, "copy-to-options", GenerateCopyToOptions)
		])
	])
}


function GenerateCopyFromDatabase(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("COPY"),
			Keyword("FROM"),
			Keyword("DATABASE"),
			Expression("source-database"),
			Keyword("TO"),
			Expression("target-database"),
			Choice(0, [
				Sequence([
					Keyword("("),
					Keyword("SCHEMA"),
					Keyword(")")
				])
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram3").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateCopyFrom(options).toString()
	document.getElementById("rrdiagram2").innerHTML = GenerateCopyTo(options).toString();
	document.getElementById("rrdiagram3").innerHTML = GenerateCopyFromDatabase(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()
