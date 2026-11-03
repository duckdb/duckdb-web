function GenerateUse(options = {}) {
    return Diagram([
        AutomaticStack([
            Keyword("USE"),
            Choice(0, [
                Sequence([
                    Expression("database-name"),
                    Optional(Sequence([Keyword("."), Expression("schema-name")]), "skip")
                ]),
                Expression("schema-name")
            ])
        ])
    ])
}

function Initialize(options = {}) {
    document.getElementById("rrdiagram1").classList.add("limit-width");
    document.getElementById("rrdiagram1").innerHTML = GenerateUse(options).toString();
}

function Refresh(node_name, set_node) {
    options[node_name] = set_node;
    Initialize(options);
}

options = {}
Initialize()
