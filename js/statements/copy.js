
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
		Optional(Sequence([
			Optional(Keyword("WITH"), "skip"),
			OneOrMore(Choice(0, [
				Sequence([Keyword("FORMAT"), Expression("format-type")]),
				Sequence([Keyword("DELIMITER"), Expression("delimiter")]),
				Sequence([Keyword("NULL"), Expression("null-string")]),
				Sequence([Keyword("DATEFORMAT"), Expression("date-format")]),
				Sequence([Keyword("TIMESTAMPFORMAT"), Expression("timestamp-format")]),
				Sequence([Keyword("HEADER"), Choice(0, [new Skip(), Keyword("TRUE"), Keyword("FALSE")])]),
				Sequence([Keyword("ESCAPE"), Expression("escape-string")]),
				Sequence([Keyword("FORCE_QUOTE"), GenerateColumnList()]),
				Sequence([Keyword("FORCE_NOT_NULL"), GenerateColumnList()])
			]), ",", "skip")
		]), "skip")
	]
}

function GenerateCopyFrom(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("COPY"),
			Expression("table-name"),
			GenerateOptionalColumnList(options),
			Sequence([
				Keyword("FROM"),
				Expression("file-name")
			]),
			Expandable("copy-options", options, "copy-from-options", GenerateCopyOptions)
		])
	])
}


function GenerateCopyTo(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("COPY"),
			Choice(0, [
				Sequence([
					Expression("table-name"),
					GenerateOptionalColumnList(options)
				]),
				Sequence([
					Keyword("("),
					Expression("select-node"),
					Keyword(")")
				])
			]),
			Sequence([
				Keyword("TO"),
				Expression("file-name")
			]),
			Expandable("copy-options", options, "copy-to-options", GenerateCopyOptions)
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateCopyFrom(options).toString()
	document.getElementById("rrdiagram2").innerHTML = GenerateCopyTo(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

