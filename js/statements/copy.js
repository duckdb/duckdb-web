
function GenerateColumnList(options) {
	return Optional(
		Sequence([
			Keyword("("),
			OneOrMore(Expression("column-name"), ","),
			Keyword(")")
		]), "skip"
	)
}

function GenerateCopyOptions(options) {
	return [
		ZeroOrMore(Choice(0, [
			Sequence([Keyword("FORMAT"), Expression("format-type")]),
			Sequence([Keyword("DELIMITER"), Expression("delimiter")]),
			Sequence([Keyword("NULL"), Expression("null-string")]),
			Sequence([Keyword("HEADER"), Choice(0, [Keyword("TRUE"), Keyword("FALSE")])]),
			Sequence([Keyword("ESCAPE"), Expression("escape-string")]),
			Sequence([Keyword("FORCE_QUOTE"), GenerateColumnList()]),
			Sequence([Keyword("FORCE_NOT_NULL"), GenerateColumnList()])
		]), ",", "skip")
	]
}

function GenerateCopyFrom(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("COPY"),
			Expression("table-name"),
			Optional(Sequence([
				Keyword("("),
				OneOrMore(Expression("column-name"), Keyword(",")),
				Keyword(")")
			]), "skip"),
			Keyword("FROM"),
			Expression("file-name"),
			Optional(Keyword("WITH"), "skip"),
			Expandable("copy-options", options, "copy-from-options", GenerateCopyOptions)
		])
	])
}


function GenerateCopyTo(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("COPY"),
			Choice(0, [
				Sequence([Expression("table-name"),
					Optional(Sequence([
						Keyword("("),
						OneOrMore(Expression("column-name"), Keyword(",")),
						Keyword(")")
					]), "skip")
				]),
				Sequence([
					Keyword("("),
					Expression("select-node"),
					Keyword(")")
				])
			]),
			Keyword("TO"),
			Expression("file-name"),
			Optional(Keyword("WITH"), "skip"),
			Expandable("copy-options", options, "copy-to-options", GenerateCopyOptions)
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateCopyFrom(options).toString() + GenerateCopyTo(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

