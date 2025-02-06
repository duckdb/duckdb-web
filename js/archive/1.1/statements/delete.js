function GenerateDelete(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("DELETE FROM"),
			GenerateQualifiedTableName(),
			Optional(Sequence([
				Keyword("USING"),
				OneOrMore(Sequence(GenerateTableOrSubquery(options)), Keyword(","))
			])),
			Optional(Sequence([
				Keyword("WHERE"),
				Expression()
			]))
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateDelete(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

