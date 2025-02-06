
function GenerateCreateMacro(options = {}) {
	return Diagram([
		AutomaticStack([
			Keyword("CREATE"),
			GenerateOrReplace(),
			GenerateTemporary(),
			Choice(0, [
				Keyword("MACRO"),
				Keyword("FUNCTION"),
				]
			),
			Optional(Sequence([
				Expression("schema-name"),
				Keyword(".")
			]), "skip"),
			Expression("macro-name"),
			OneOrMore(Sequence([
				Keyword("("),
				ZeroOrMore(Sequence([
					Expression("param-name"),
					], "skip")
				),
				ZeroOrMore(Sequence([
					Expression("param-name"),
					Keyword(":="),
					Expression("default-value")
					], "skip")
				),
				Keyword(")"),
				Keyword("AS"),
				Optional("TABLE"),
				Expression("expr")
			]), ",")
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateCreateMacro(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

