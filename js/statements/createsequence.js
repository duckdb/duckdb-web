
function GenerateCreateSequence(options = {}) {
	return Diagram([
		Stack([
			Sequence([
				Keyword("CREATE"),
				Optional(Choice(0, [Keyword("TEMPORARY"), Keyword("TEMP")]), "skip"),
				Keyword("SEQUENCE"),
				Expression("sequence-name")
			]),
			Sequence([
				Optional(Sequence([
					Keyword("INCREMENT"),
					Optional(Keyword("BY"), "skip"),
					Expression()
				]), "skip"),
				Choice(0, [
					new Skip(),
					Sequence([Keyword("NO"), Keyword("MINVALUE")]),
					Sequence([Keyword("MINVALUE"), Expression()])
				])
			]),
			Sequence([
				Choice(0, [
					new Skip(),
					Sequence([Keyword("NO"), Keyword("MAXVALUE")]),
					Sequence([Keyword("MAXVALUE"), Expression()])
				]),
				Optional(Sequence([
					Keyword("START"),
					Optional(Keyword("WITH"), "skip"),
					Expression()
				]), "skip"),
				Optional(Sequence([
					Optional(Keyword("NO"), "skip"),
					Keyword("CYCLE")
				]), "skip")
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").innerHTML = GenerateCreateSequence(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

