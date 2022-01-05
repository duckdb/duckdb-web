function GenerateAggregateOrderBy(options = {}) {
	return [
		Keyword("ORDER"),
		Keyword("BY"),
		GenerateOrderTerms()
	]
}

function GenerateFilterClause(options = {}) {
	return [
		Keyword("FILTER"),
		Keyword("("),
		Keyword("WHERE"),
		Expression('filter_expr'),
		Keyword(")")
	]
}

function GenerateAggregate(options = {}) {
	return Diagram([
		AutomaticStack([
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
			Keyword(")"),
			Optional(Expandable("filter-clause",options,"filter-clause",GenerateFilterClause)),
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

