

function GenerateCreateType(options = {}) {
	return Diagram([
		AutomaticStack([
			Sequence([
				Keyword("CREATE"),
				Keyword("TYPE"),
				Expression("type-name"),
				Keyword("AS"),
			]),
            Choice(0, [
                Expression("existing-type-name"), 
                Sequence([
                    Keyword("ENUM"),
                    Keyword("("),
                    OneOrMore(Expression("'enum-value'"), ","),
                    Keyword(")")
                ]),
                Sequence([
                    Keyword("STRUCT"),
                    Keyword("("),
                    OneOrMore(
                        Sequence([
                            Expression("field-name"),
                            Expression("existing-type-name"),
                        ]),
                        ","
                    ),
                    Keyword(")")
                ]),
                Sequence([
                    Keyword("UNION"),
                    Keyword("("),
                    OneOrMore(
                        Sequence([
                            Expression("field-name"),
                            Expression("existing-type-name"),
                        ]),
                        ","
                    ),
                    Keyword(")")
                ])
            ])
		])
	])
}

function Initialize(options = {}) {
	document.getElementById("rrdiagram").classList.add("limit-width");
	document.getElementById("rrdiagram").innerHTML = GenerateCreateType(options).toString();
}

function Refresh(node_name, set_node) {
	options[node_name] = set_node;
	Initialize(options);
}

options = {}
Initialize()

