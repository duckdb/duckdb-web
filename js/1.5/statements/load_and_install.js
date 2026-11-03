function GenerateLoad(options = {}) {
    return Diagram([
        AutomaticStack([
            Keyword("LOAD"),            
            Choice(0, [
                Expression("extension-name"),
                Expression("'extension-path'")
            ]),
        ])
    ])
}

function GenerateInstall(options = {}) {
    return Diagram([
        AutomaticStack([
            Optional(Keyword("FORCE"), "skip"),
            Keyword("INSTALL"),
            Expression("extension-name"),
            Optional(
                Sequence([
                    Keyword("FROM"),
                    Choice(0, [
                        Expression("repository"),
                        Expression("'repository-url'")
                    ]),
                ]),
                "skip"
            ),
            Optional(
                Sequence([
                    Keyword("VERSION"),
                    Expression("version-number")
                ]),
                "skip"
            )
        ])
    ])
}

function Initialize(options = {}) {
    document.getElementById("rrdiagram1").classList.add("limit-width");
    document.getElementById("rrdiagram1").innerHTML = GenerateLoad(options).toString();

    document.getElementById("rrdiagram2").classList.add("limit-width");
    document.getElementById("rrdiagram2").innerHTML = GenerateInstall(options).toString();
}

function Refresh(node_name, set_node) {
    options[node_name] = set_node;
    Initialize(options);
}

options = {}
Initialize()
