function GenerateAlterDatabase(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("ALTER DATABASE"),
			Optional(Sequence([
				Keyword("IF EXISTS")
			])),
			Expression("database-name"),
			Keyword("RENAME TO"),
			Expression("new-name")
		])
	]);
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateAlterDatabase(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {};
Initialize();