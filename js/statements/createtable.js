
function GenerateTableConstraints(options) {
	return [ZeroOrMore(Choice(0, [
		Sequence([
			Choice(0, [
				Sequence([
					Keyword("PRIMARY"),
					Keyword("KEY")
				]),
				Keyword("UNIQUE")
			]),
			Keyword("("),
			OneOrMore(Expression("column-name"), ","),
			Keyword(")")
		]),
		Sequence([
			Keyword("CHECK"),
			Keyword("("),
			Expression(),
			Keyword(")")
		])
	]), ",", "skip")]
}

function GenerateCreateTable(options = {}) {
	return Diagram([
		AutomaticStack([
			Sequence([
				Keyword("CREATE"),
				GenerateTemporary(),
				Keyword("TABLE")
			]),
			Sequence([
				GenerateIfNotExists(),
				GenerateQualifiedTableName()
			]),
			Choice(0, [
				AutomaticStack([
					Keyword("("),
					OneOrMore(Sequence([
						Expression("column-name"),
						Expression("type-name"),
						Expandable("column-constraints", options, "column-constraints", GenerateColumnConstraints)
					]), ","),
					Expandable("table-constraints", options, "table-constraints", GenerateTableConstraints),
					Keyword(")")
				]),
				Sequence([
					Keyword("AS"),
					Expression("select-node")
				])
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateCreateTable(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

