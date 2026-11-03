function GenerateVacuum(options = {}) {
    return Diagram([
        AutomaticStack([
            Keyword("VACUUM"),
            Choice(0, [new Skip(), Keyword("ANALYZE")]),
            Choice(0, [new Skip(),
                Sequence([
                    Expression("table-name"),
                    Optional(Sequence([
                            Keyword("("),
                            OneOrMore(Expression("column-name"), ","),
                            Keyword(")")]),
                        "skip")
                ])
            ])
        ])
    ])
}

function Initialize(options = {}) {
    document.getElementById("rrdiagram1").classList.add("limit-width");
    document.getElementById("rrdiagram1").innerHTML = GenerateVacuum(options).toString();
}

function Refresh(node_name, set_node) {
    options[node_name] = set_node;
    Initialize(options);
}

options = {}
Initialize()
