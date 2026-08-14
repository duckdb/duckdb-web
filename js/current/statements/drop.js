

function GenerateDrop(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("DROP"),
			Choice(3, [
				Keyword("FUNCTION"),
				Keyword("INDEX"),
				Sequence([
					Keyword("MACRO"),
					Optional(Keyword("TABLE"), "skip")
				]),
				Keyword("SCHEMA"),
				Keyword("SEQUENCE"),
				Keyword("TABLE"),
				Keyword("VIEW"),
				Keyword("TYPE"),
			]),
			GenerateIfExists(),
			GenerateQualifiedTableName(options, "entry-name"),
			Choice(0, [
				new Skip(),
				Keyword("CASCADE"),
				Keyword("RESTRICT")
			])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateDrop(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

