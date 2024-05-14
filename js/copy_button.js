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
        var code = $(this).parent().find('code').text().trim();
        
        window.navigator.clipboard.writeText(code);
        
        elem.html('<span class="copied"></span>');
        
        setTimeout(function () {
            elem.html('<span class="copy"></span>');
        }, 3500);
    });
    
});
