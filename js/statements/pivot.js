
function GeneratePivot(options) {
	return Diagram([
		AutomaticStack([
			Choice(0, [
				Keyword("PIVOT"),
				Keyword("PIVOT_WIDER")
			]),
			Choice(0, [
				Expression("table-name"),
				Expression("view-name"),
				Expression("table-function-name"),
				Sequence([
					Keyword('('),
					Expression("select-node"),
					Keyword(')'),
				])
			]),
			Optional(
				Sequence([
					Keyword("ON"),
					OneOrMore(
						Sequence([
							Expression("pivot-column"),
							Optional(
								Sequence([
									Keyword("IN"),
									Keyword("("),
									Expression("in-list"),
									Keyword(")"),
								]),
								"skip")
						]), ",")
				]),
				"skip"),
			Optional(
				Sequence([
					Keyword("USING"),
					OneOrMore(
						Sequence([
							Expression("aggregate-expr"),
							Optional(Sequence([Optional(Keyword("AS")), Expression("alias")])),
						]), ","),
				]),
				"skip"),
			Optional(
				Sequence([
					Keyword("GROUP BY"),
					OneOrMore(Expression("group-by-expr"), ","),
				]),
				"skip"),
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GeneratePivot(options).toString();

}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

