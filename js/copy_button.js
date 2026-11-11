(function () {
    var codeBlocks = document.querySelectorAll('pre.highlight, figure.highlight');

    codeBlocks.forEach(function (codeBlock) {
        if (codeBlock.closest('.language-console') || codeBlock.querySelector(':scope > button.copy')) {
            return;
        }
        var copyButton = document.createElement('button');
        copyButton.className = 'copy';
        copyButton.type = 'button';
        copyButton.setAttribute('aria-label', 'Copy code to clipboard');
        copyButton.innerHTML = '<span class="copy"></span>';
        codeBlock.append(copyButton);
    });

    function extractTextWithLinebreaks(node) { // <br> to \n
        var text = '';
        node.childNodes.forEach(function (child) {
            if (child.nodeType === Node.TEXT_NODE) {
                text += child.textContent;
            } else if (child.nodeName === 'BR') {
                text += '\n';
            } else {
                text += extractTextWithLinebreaks(child);
            }
        });
        return text;
    }

    document.addEventListener('click', function (event) {
        var button = event.target.closest('main button.copy');
        if (!button) {
            return;
        }
        var codeElem = button.parentElement.querySelector('code');
        if (!codeElem) {
            return;
        }
        window.navigator.clipboard.writeText(extractTextWithLinebreaks(codeElem).trim());
        button.innerHTML = '<span class="copied"></span>';

        setTimeout(function () {
            button.innerHTML = '<span class="copy"></span>';
        }, 3500);
    });
})();
