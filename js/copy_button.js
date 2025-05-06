$(document).ready(function() {
    var codeBlocks = [].concat(...document.querySelectorAll('pre.highlight'), ...document.querySelectorAll('figure.highlight'));

    codeBlocks.forEach(function (codeBlock) {
        if (!$(codeBlock).parents().hasClass('language-console')) {
            var copyButton = document.createElement('button');
            copyButton.className = 'copy';
            copyButton.type = 'button';
            copyButton.ariaLabel = 'Copy code to clipboard';
            copyButton.innerHTML = '<span class="copy"></span>';
            codeBlock.append(copyButton);
        }
    });
    
    $('main').on('click', 'button.copy', function() {
        var elem = $(this);
        var codeElem = $(this).parent().find('code')[0];

        function extractTextWithLinebreaks(node) { // <br> to \n 
            var text = '';
            node.childNodes.forEach(function(child) {
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

        var text = extractTextWithLinebreaks(codeElem).trim();
        window.navigator.clipboard.writeText(text);
        elem.html('<span class="copied"></span>');

        setTimeout(function () {
            elem.html('<span class="copy"></span>');
        }, 3500);
    });
    
});
