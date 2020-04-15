function GenerateValues(options) {
	return [
		Keyword("VALUES"),
		OneOrMore(
			Sequence([
				Keyword("("),
				OneOrMore(Expression(), ","),
				Keyword(")")
			]), Keyword(","))
	]
}

function GenerateDistinctClause(options) {
	return [
		Choice(0, [
			new Skip(),
			Sequence([
				Keyword("DISTINCT"),
				Optional(Sequence([
					Keyword("("),
					OneOrMore(Expression(), ","),
					Keyword(")"),
				]) , "skip")
			]),
			Keyword("ALL")
		])
	]
}

function GenerateDistinctClause(options) {
	return [
		Choice(0, [
			new Skip(),
			Sequence([
				Keyword("DISTINCT"),
				Optional(Sequence([
					Keyword("("),
					OneOrMore(Expression(), ","),
					Keyword(")"),
				]) , "skip")
			]),
			Keyword("ALL")
		])
	]
}

function GenerateJoinClause(options) {
	return [
		Expression("table-or-subquery"),
		OneOrMore(Sequence([
				Sequence([
					Optional(Keyword("NATURAL"), "skip"),
					Choice(0,[
						Keyword("INNER"),
						Sequence([Choice(0, [Keyword("LEFT"), Keyword("RIGHT"), Keyword("FULL")]), Optional(Keyword("OUTER"), "skip")]),
						Keyword("CROSS")
					]),
					Keyword("JOIN")
				]),
				Expression("table-or-subquery"),
				Choice(0, [
					Sequence([
						Keyword("ON"),
						Expression()
					]),
					Sequence([
						Keyword("USING"),
						Keyword("("),
						OneOrMore(Expression("column-name"), ","),
						Keyword(")")
					])
				])
			]))
	]
}

function GenerateTableReference(options) {
	return [
		Sequence([
			Optional(Sequence([Expression("schema-name"), Keyword(".")]), "skip"),
			Expression("table-name"),
		])
	]
}

function GenerateTableFunction(options) {
	return [
		Sequence([
			Optional(Sequence([Expression("schema-name"), Keyword(".")]), "skip"),
			Expression("table-function-name"),
			Keyword("("),
			ZeroOrMore(Expression(), ","),
			Keyword(")"),
		])
	]
}

function GenerateSubquery(options) {
	return [
		Sequence([
			Sequence([
				Keyword("("),
				Expression("select-node"),
				Keyword(")"),
			])
		])
	]
}

function GenerateTableOrSubquery(options) {
	return [
		Choice(0, [
			Sequence([
				Choice(0,[
					Expandable("table-reference", options, "table-reference", GenerateTableReference),
					Expandable("table-function", options, "table-function", GenerateTableFunction),
					Expandable("subquery", options, "subquery", GenerateSubquery)
				]),
				Optional(Sequence([Keyword("AS"), Expression("table-alias")]), "skip")
			]),
			Expandable("join-clause", options, "join-clause", GenerateJoinClause)
		])
	]
}

function GenerateCommonTableExpression(options) {
	return [
		Expression("table-name"),
		Optional(Sequence([
			Keyword("("),
			OneOrMore(Expression("column-name"), Keyword(",")),
			Keyword(")")
		]), "skip"),
		Keyword("AS"),
		Keyword("("),
		Expression("select-node"),
		Keyword(")")
	]
}

function GenerateOrderBy(options) {
	return [
		Keyword("ORDER"),
		Keyword("BY"),
		OneOrMore(Sequence([
			Expression(),
			Choice(0, [
				new Skip(),
				Keyword("ASC"),
				Keyword("DESC")
			])
		]), ",")
	]
}

function GenerateSelectNode(options) {
	return [Stack([
		Sequence([
			Keyword("SELECT"),
			Expandable("distinct-clause", options, "distinct-clause", GenerateDistinctClause),
			OneOrMore(Choice(0, [
				Sequence([Expression(), Optional(Sequence([Keyword("AS"), Expression("alias")]), "skip")]),
				Sequence([
					Optional(Sequence([Expression("table-name"), Keyword(".")]), "skip"),
					Keyword("*")
				])
			]), ",")
		]),
		Sequence([
			Optional(Sequence([
				Keyword("FROM"),
				OneOrMore(Expandable("table-or-subquery", options, "table-or-subquery-1", GenerateTableOrSubquery), Keyword(","))
			])),
			Optional(
				Sequence([
					Keyword("WHERE"),
					Expression()
				])
			)
		]),
		Sequence([
			Optional(Sequence([
				Keyword("GROUP"),
				Keyword("BY"),
				OneOrMore(Expression(), ","),
			])),
			Optional(Sequence([
				Keyword("HAVING"),
				Expression()
			]))
		]),
		Optional(
			Sequence([Sequence([
					Keyword("WINDOW"),
					Expression("window-name"),
					Keyword("AS"),
					Expression("window-definition")
				])
			]), "skip"),
		Sequence([
			Optional(Sequence(GenerateOrderBy(options)))
		]),
		Optional(Sequence([
			Keyword("LIMIT"),
			Expression(),
			Optional(Sequence([
				Keyword("OFFSET"),
				Expression()
			]), "skip")
		]))
	])]
}

function GenerateSetOperation(options) {
	return [
		Choice(0, [
			Keyword("UNION"),
			Keyword("UNION ALL"),
			Keyword("INTERSECT"),
			Keyword("EXCEPT")
		])
	]
}

function GenerateSelect(options = {}) {
	return Diagram([
		Stack([
			Optional(
				Sequence([
					Keyword("WITH"),
					Optional(Keyword("RECURSIVE"), "skip"),
					OneOrMore(
						Expandable("common-table-expr", options, "common-table-expr", GenerateCommonTableExpression), ",")
				]), "skip"),
			OneOrMore(Choice(0, [
				Expandable("select-node", options, "select-node", GenerateSelectNode),
				Expandable("values-list", options, "values", GenerateValues)
			]), Expandable("set-operation", options, "set-operation", GenerateSetOperation))
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").innerHTML = GenerateSelect(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

