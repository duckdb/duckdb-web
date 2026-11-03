function GenerateCreateSchema(options = {}) {
	return Diagram([
		AutomaticStack([
			Sequence([
				Keyword("CREATE"),
				GenerateOrReplace(),
				Keyword("SCHEMA"),
				GenerateIfNotExists(),
				Expression("schema-name")
			]),
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateCreateSchema(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()
