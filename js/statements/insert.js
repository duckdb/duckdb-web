
function GenerateInsert(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("INSERT"),
			Choice(0, [
				new Skip(),
				Keyword("OR REPLACE"),
				Keyword("OR IGNORE"),
			]),
			Keyword("INTO"),
			GenerateQualifiedTableName(),
			Optional(
				Sequence([
					Keyword("AS"),
					GenerateQualifiedTableName()
				]),
				"skip"
			),
			GenerateOptionalColumnList(),
			Choice(0, [
				Sequence(GenerateValues(options)),
				Expression("select-node"),
				Sequence([
					Keyword("DEFAULT"),
					Keyword("VALUES")
				])
			]),
			Optional(
				Expandable("on-conflict-clause", options, "on-confict-clause", GenerateOnConflict),
				"skip"
			),
			Optional( 
				Expandable("returning-clause", options, "returning-clause", GenerateReturning),
				"skip"
			)
		])
	])
}

function GenerateOnConflict(options) {
	return [
		Sequence([
			Keyword("ON CONFLICT"),
			// (c1, c2) WHERE <expr>
			Optional(
				Sequence([
					Keyword("("),
					OneOrMore(
						Expression("column-name"),
						Keyword(",")
					),
					Keyword(")"),
					Optional(
						Sequence([
							Keyword("WHERE"),
							Expression()
						]),
						"skip"
					)
				]),
				"skip"
			),
			Choice(0, [
				Sequence([
					Keyword("DO UPDATE"),
					Keyword("SET"),
					OneOrMore(
						Sequence([
							Expression("column-name"),
							Keyword("="),
							Expression(),
						]), Keyword(",")
					),
					Optional(Sequence([
						Keyword("WHERE"),
						Expression()
					]), "skip")
				]),
				Sequence([
					Keyword("DO NOTHING")
				])
			])
		])
	]
}

function GenerateReturning(options) {
	return [
		Sequence([
			Keyword("RETURNING"),
			Optional(Keyword("*"), "skip"),
			Choice(0, [
				new Skip(),
				OneOrMore(
					Sequence([Expression(), Optional(Sequence([Optional(Keyword("AS")), Expression("alias")]), "skip")]),
					","
				),
			]),
		])
	]
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateInsert(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

