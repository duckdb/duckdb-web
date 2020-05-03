
function GenerateAlterColumnOptions(options) {
	return [
		Choice(0, [
			Sequence([
				Optional(Sequence([
					Keyword("SET"),
					Keyword("DATA")
				])),
				Keyword("TYPE"),
				Expression("data-type"),
				Optional(
					Sequence([
						Keyword("COLLATE"),
						Expression("collation-name"),
					])
				),
				Optional(
					Sequence([
						Keyword("USING"),
						Expression(),
					])
				)
			]),
			Sequence([
				Keyword("SET"),
				Keyword("DEFAULT"),
				Expression()
			]),
			Sequence([
				Keyword("DROP"),
				Keyword("DEFAULT")
			])
		])
	]
}

function GenerateCreateSequence(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("ALTER"),
			Keyword("TABLE"),
			Expression("table-name"),
			Choice(0, [
				Sequence([
					Keyword("ADD"),
					Optional("COLUMN"),
					Expression("column-name"),
					Expression("type-name"),
					Expandable("column-constraints", options, "column-constraints", GenerateColumnConstraints)
				]),
				Sequence([
					Keyword("DROP"),
					Optional("COLUMN"),
					Optional(Sequence([
						Keyword("IF"),
						Keyword("EXISTS")
					]), "skip"),
					Expression("column-name")
				]),
				Sequence([
					Keyword("ALTER"),
					Optional("COLUMN"),
					Expression("column-name"),
					Expandable("alter-column-options", options, "alter-column-options", GenerateAlterColumnOptions)
				]),
				Sequence([
					Keyword("RENAME"),
					Optional("COLUMN"),
					Expression("column"),
					Keyword("TO"),
					Expression("new-column")
				]),
				Sequence([
					Keyword("RENAME"),
					Keyword("TO"),
					Expression("new-name")
				])
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateCreateSequence(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

