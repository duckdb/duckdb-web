
function GenerateAttachOptions(options) {
	return [
		Keyword('('),
		Sequence([
			OneOrMore(Choice(0, [
				Sequence([Keyword("READ_ONLY"), Choice(0, [new Skip(), Keyword("TRUE"), Keyword("FALSE")])]),
				Sequence([Keyword("TYPE"), Choice(0, [Keyword("sqlite")])])
			]), ",", "skip")
		]),
		Keyword(')'),
	]
}

function GenerateAttach(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("ATTACH"),
			Optional(Keyword("DATABASE"), "skip"),
			Expression("database-path"),
			Optional(Sequence([
				Keyword("AS"),
				Expression("database-alias")
			])),
			Expandable("attach-options", options, "attach-options", GenerateAttachOptions)
		])
	])
}

function GenerateDetach(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("DETACH"),
			Optional(Sequence([
				Keyword("DATABASE"),
				Optional(Sequence([Keyword("IF"), Keyword("EXISTS")]), "skip"),
			]), "skip"),
			Expression("database")
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateAttach(options).toString();

	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateDetach(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

