
function GenerateCreateSequence(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("CREATE"),
			GenerateOrReplace(),
			GenerateTemporary(options),
			Sequence([
				Keyword("SEQUENCE"),
				Expression("sequence-name")
			]),
			Optional(Sequence([
				Keyword("INCREMENT"),
				Optional(Keyword("BY"), "skip"),
				Expression("increment")
			]), "skip"),
			Choice(0, [
				new Skip(),
				Keyword("NO MINVALUE"),
				Sequence([Keyword("MINVALUE"), Expression("minvalue")])
			]),
			Choice(0, [
				new Skip(),
				Keyword("NO MAXVALUE"),
				Sequence([Keyword("MAXVALUE"), Expression("maxvalue")])
			]),
			Optional(Sequence([
				Keyword("START"),
				Optional(Keyword("WITH"), "skip"),
				Expression("start")
			]), "skip"),
			Optional(Sequence([
				Optional(Keyword("NO"), "skip"),
				Keyword("CYCLE")
			]), "skip")
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

