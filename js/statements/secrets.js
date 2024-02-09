

function GenerateCreateSecret(options = {}) {
	return Diagram([
		Stack([
			Sequence([
				Keyword("CREATE"),
				Keyword("SECRET"),
				Expression("name"),
				Keyword("ON"),
				Expression("table"),
			]),
			Sequence([
				Keyword("("),
				OneOrMore(
					Choice(0, [
						Expression("column"),
						Sequence([Keyword("("),  Expression("expression"), Keyword(")")])
					]),
				Keyword(",")),
				Keyword(")")
			]),
		])
	])
}

function GenerateDropSecret(options = {}) {
	return Diagram([
		Sequence([
			Keyword("DROP"),
			Keyword("SECRET"),
			Optional(Sequence([Keyword("IF"), Keyword("EXISTS")]), "skip"),
			Expression("name")
		]),
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateCreateSecret(options).toString();
	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateDropSecret(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

