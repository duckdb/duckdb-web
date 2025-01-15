function GenerateWindowOrderBy(options = {}) {
	return [
		Keyword("ORDER"),
		Keyword("BY"),
		GenerateOrderTerms()
	]
}

function GenerateWindowFunction(options = {}) {
	return Diagram([
		AutomaticStack([
			Expression("function-name"),
			Keyword("("),
			Sequence([
				Optional(Keyword("DISTINCT"), "skip"),
				ZeroOrMore(Sequence([
					Expression()
				]), Keyword(",")),
				Optional(Expandable("order-by", options, "order-by", GenerateWindowOrderBy))
			]),
			Keyword(")"),
			Keyword("OVER"),
			Choice(1, [
				Sequence(GenerateWindowSpec(options)),
				Expression("window-name")
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateWindowFunction(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

