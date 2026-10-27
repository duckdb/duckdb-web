function GeneratePrepare(options = {}) {
    return Diagram([
        AutomaticStack([
            Keyword("PREPARE"),
            Expression("statement-name"),
            Optional(Sequence([
                "(",
                OneOrMore(Expression("parameter-type"), ","),
                ")"
            ]), "skip"),
            Keyword("AS"),
            Expression("statement")
        ])
    ])
}

function GenerateExecute(options = {}) {
    return Diagram([
        AutomaticStack([
            Keyword("EXECUTE"),
            Expression("statement-name"),
            Optional(Sequence([
                "(",
                OneOrMore(Expression("argument"), ","),
                ")"
            ]), "skip")
        ])
    ])
}

function GenerateDeallocate(options = {}) {
    return Diagram([
        AutomaticStack([
            Keyword("DEALLOCATE"),
            Optional(Keyword("PREPARE"), "skip"),
            Expression("statement-name")
        ])
    ])
}

function Initialize(options = {}) {
    document.getElementById("rrdiagram1").classList.add("limit-width");
    document.getElementById("rrdiagram1").innerHTML = GeneratePrepare(options).toString();
    document.getElementById("rrdiagram2").classList.add("limit-width");
    document.getElementById("rrdiagram2").innerHTML = GenerateExecute(options).toString();
    document.getElementById("rrdiagram3").classList.add("limit-width");
    document.getElementById("rrdiagram3").innerHTML = GenerateDeallocate(options).toString();
}

function Refresh(node_name, set_node) {
    options[node_name] = set_node;
    Initialize(options);
}

options = {}
Initialize()
