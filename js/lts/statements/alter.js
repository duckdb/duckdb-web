
function GenerateAlterColumnOptions(options) {
	return [
		Choice(0, [
			Sequence([
				Optional(Sequence([
					Keyword("SET"),
					Optional(Keyword("DATA"))
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
				Keyword("SET DEFAULT"),
				Expression()
			]),
			Sequence([
				Keyword("DROP DEFAULT")
			]),
			Sequence([
				Keyword("SET NOT NULL"),
			]),
			Sequence([
				Keyword("DROP NOT NULL")
			])
		])
	]
}

function GenerateAlterTable(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("ALTER TABLE"),
			Expression("table-name"),
			Choice(0, [
				Sequence([
					Keyword("ADD"),
					Choice(0, [
						Sequence([
							Optional("COLUMN"),
							GenerateIfNotExists(),
							Expression("column-name"),
							Expression("type-name"),
							Expandable("column-constraints", options, "column-constraints", GenerateColumnConstraints)
						]),
						Sequence([
							Keyword("PRIMARY KEY"),
							Keyword("("),
							OneOrMore(Expression("column-name"), ","),
							Keyword(")")
						])
					])
				]),
				Sequence([
					Keyword("DROP"),
					Optional("COLUMN"),
					GenerateIfExists(),
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
					Keyword("RENAME TO"),
					Expression("new-name")
				])
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateAlterTable(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

