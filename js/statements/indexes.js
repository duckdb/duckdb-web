

function GenerateCreateIndex(options = {}) {
	return Diagram([
		Stack([
			Sequence([
				Keyword("CREATE"),
				Optional(Keyword("UNIQUE"), "skip"),
				Keyword("INDEX"),
				GenerateIfNotExists(),
				Expression("name"),
				Keyword("ON"),
				Expression("table"),
				Optional(Sequence([Keyword("USING"), Expression("index type")]), "skip"),
			]),
			Sequence([
				Keyword("("),
				OneOrMore(
					Choice(0, [
						Expression("column"),
						Sequence([Keyword("("),  Expression("expression"), Keyword(")")])
					]),
				Keyword(",")),
				Keyword(")"),
				Optional(
					Sequence([
						Keyword("WITH"),
						Keyword("("),
						Sequence([
							OneOrMore(
								Choice(0, [Expression("option")]),
								Keyword(",")
							),
						]),
						Keyword(")"),
					]),
					"skip"
				),
			]),
		])
	])
}

function GenerateDropIndex(options = {}) {
	return Diagram([
		Sequence([
			Keyword("DROP INDEX"),
			Optional(Sequence([Keyword("IF EXISTS")]), "skip"),
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

