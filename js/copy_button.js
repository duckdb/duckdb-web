$(document).ready(function() {
    var codeBlocks = [].concat(...document.querySelectorAll('pre.highlight'), ...document.querySelectorAll('figure.highlight'));

    codeBlocks.forEach(function (codeBlock) {
        var copyButton = document.createElement('button');
        copyButton.className = 'copy';
        copyButton.type = 'button';
        copyButton.ariaLabel = 'Copy code to clipboard';
        copyButton.innerHTML = '<span class="copy"></span>';

        codeBlock.append(copyButton);

        copyButton.addEventListener('click', function () {
            var code = codeBlock.querySelector('code').innerText.trim();
            window.navigator.clipboard.writeText(code);

            copyButton.innerHTML = '<span class="copied"></span>';
            var fourSeconds = 3000;

            setTimeout(function () {
            copyButton.innerHTML = '<span class="copy"></span>';
            }, fourSeconds);
        });
    });
});
