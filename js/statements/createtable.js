
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
		]),
		Sequence([
			Keyword("FOREIGN"),
			Keyword("KEY"),
			Keyword("("),
			OneOrMore(Expression("column-name"), ","),
			Keyword(")"),
			Keyword("REFERENCES"),
			Expression("foreign-table"),
			Keyword("("),
			OneOrMore(Expression("column-name"), ","),
			Keyword(")")
		])
	]), ",", "skip")]
}

function GenerateGeneratedColumnDefinition(options) {
	return [
		Sequence([
			Sequence([
				GenerateOptionalType(),
				GenerateGeneratedColumnSyntax(),
			]),
			Sequence([
				Keyword("("),
				Expression("expr"),
				Keyword(")"),
				GenerateOptionalGeneratedType(),
			])
		])
	];
}

function GenerateOptionalType(options) {
	return Optional(Sequence([
		Expression("type-name"),
	]), "skip");
}

function GenerateGeneratedColumnSyntax(options) {
	return Sequence([
		Optional(Sequence([
			Keyword("GENERATED"),
			Keyword("ALWAYS"),
		]), "skip"),
		Keyword("AS")
	]);
}

function GenerateOptionalGeneratedType(options) {
	return Optional(Choice(0, [Keyword("VIRTUAL"), Keyword("STORED")]), "skip");
}

function GenerateCreateTable(options = {}) {
	return Diagram([
		AutomaticStack([
			Sequence([
				Keyword("CREATE"),
				GenerateOrReplace(),
				GenerateTemporary(),
				Keyword("TABLE")
			]),
			Sequence([
				GenerateIfNotExists(),
				GenerateQualifiedTableName()
			]),
			Choice(1, [
				AutomaticStack([
					Sequence([
						Keyword("("),
						OneOrMore(Sequence([
							Expression("column-name"),
							Choice(0, [
								Sequence([
									Expression("type-name"),
									Expandable("column-constraints", options, "column-constraints", GenerateColumnConstraints)
								]),
								Expandable("generated-column", options, "generated-column", GenerateGeneratedColumnDefinition),
							])
						]), ","),
						Expandable("table-constraints", options, "table-constraints", GenerateTableConstraints),
						Keyword(")")
					])
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

