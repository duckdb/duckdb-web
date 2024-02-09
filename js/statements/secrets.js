function GenerateCreateSecret(options = {}) {
	return Diagram([
		Stack([
			Sequence([
				Keyword("CREATE"),
				GenerateOrReplace(),
				Optional(Choice(0, [Keyword("PERSISTENT"), Keyword("TEMPORARY")]), "skip"),
				Keyword("SECRET"),
			]),
			Sequence([
				GenerateIfNotExists(),
				Expression("secret_name"),
				Optional(Sequence([Keyword("IN"), Expression("storage_specifier")]), "skip")
			]),
			Sequence([
				Keyword("("),
				Keyword("TYPE"), Expression("secret_type"),
				ZeroOrMore(Sequence([Keyword(","), Keyword("KEY_n"), Expression("VALUE_n")])),
				Keyword(")"),
			]),
		])
	])
}

function GenerateDropSecret(options = {}) {
	return Diagram([
		Stack([
			Sequence([
				Keyword("DROP"),
				Optional(Choice(0, [Keyword("PERSISTENT"), Keyword("TEMPORARY")]), "skip"),
				Keyword("SECRET"),
				Optional(Sequence([Keyword("IF"), Keyword("EXISTS")]), "skip")
			]),
			Sequence([
				Expression("secret_name"),
				Optional(Sequence([Keyword("FROM"), Expression("storage_specifier")]), "skip")
			]),
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram1").classList.add("limit-width");
	document.getElementById("rrdiagram1").innerHTML = GenerateCreateSecret(options).toString();
	document.getElementById("rrdiagram2").classList.add("limit-width");
	document.getElementById("rrdiagram2").innerHTML = GenerateDropSecret(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

