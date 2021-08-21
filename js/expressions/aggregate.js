function GenerateAggregateOrderBy(options = {}) {
	return [
		Keyword("ORDER"),
		Keyword("BY"),
		GenerateOrderTerms()
	]
}

function GenerateAggregate(options = {}) {
	return Diagram([
		Sequence([
			Expression("aggregate-name"),
			Keyword("("),
			Choice(0, [
				Sequence([
					Optional(Keyword("DISTINCT"), "skip"),
					OneOrMore(Sequence([
						Expression()
					]), Keyword(",")),
					Optional(Expandable("order-by", options, "order-by", GenerateAggregateOrderBy))
				]),
				new Skip()
			]),
			Keyword(")")
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateAggregate(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

