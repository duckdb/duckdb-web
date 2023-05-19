
function GenerateUpdate(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("UPDATE"),
			GenerateQualifiedTableName(),
			Optional(
				Sequence([
					Optional(Keyword('AS')),
					Expression('table-alias')
				])
			),
			Sequence([
				Keyword("SET"),
				OneOrMore(
					Sequence([
						Expression("column-name"),
						Keyword("="),
						Choice(0, [
							Expression(),
							Expression("subquery")
						]),
					]), Keyword(",")
				)
			]),
			Optional(Expandable("from-node",options,"from-node",GenerateFromClause)),
			Optional(Sequence([
				Keyword("WHERE"),
				Expression()
			]))
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateUpdate(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

