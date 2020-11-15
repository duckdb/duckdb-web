

function GenerateCreateIndex(options = {}) {
	return Diagram([
		Stack([
			Sequence([
				Keyword("CREATE"),
				Optional(Keyword("UNIQUE"), "skip"),
				Keyword("INDEX"),
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

function GenerateDropIndex(options = {}) {
	return Diagram([
		Sequence([
			Keyword("DROP"),
			Keyword("INDEX"),
			Optional(Sequence([Keyword("IF"), Keyword("EXISTS")]), "skip"),
			Expression("name")
		]),
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateCreateIndex(options).toString();
	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateDropIndex(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

