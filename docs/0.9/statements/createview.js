

function GenerateCreateView(options = {}) {
	return Diagram([
		AutomaticStack([
			Sequence([
				Keyword("CREATE"),
				GenerateOrReplace(),
				GenerateTemporary(),
				Keyword("VIEW")
			]),
			Sequence([
				GenerateQualifiedTableName(options, "view-name")
			]),
			GenerateOptionalColumnList(options),
			Sequence([
				Keyword("AS"),
				Expression("select-node")
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateCreateView(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

