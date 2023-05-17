
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
							Choice(0, [
								Expression("pivot-column"),
								Expression("pivot-expr"),
							]),
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

function GenerateSQLStandardPivot(options) {
	return Diagram([
		AutomaticStack([
			Keyword("FROM"),
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
			Choice(0, [
				Keyword("PIVOT")
			]),
			Keyword("("),
			OneOrMore(
				Sequence([
					Expression("aggregate-expr"),
					Optional(Sequence([Optional(Keyword("AS")), Expression("alias")])),
				]), ","),
			Keyword("FOR"),
			Sequence([
				OneOrMore(
					Sequence([
						Expression("pivot-column"),
						Sequence([
							Keyword("IN"),
							Keyword("("),
							Expression("in-list"),
							Keyword(")"),
						])
					]), " ")
			]),
			Optional(
				Sequence([
					Keyword("GROUP BY"),
					OneOrMore(Expression("group-by-expr"), ","),
				]),
				"skip"),
			Keyword(")"),
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GeneratePivot(options).toString();

	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateSQLStandardPivot(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

