(function() {
    function setDarkMode() {
        document.documentElement.classList.add("darkmode");
        document.documentElement.classList.add('disable-transitions');
    }

    try {
        var userColorSchemePref = localStorage.getItem("mode");
        if (userColorSchemePref !== null) {
            if (userColorSchemePref === 'dark') {
                setDarkMode();
            }
            return;
        }
    } catch (e) {}

    // Fallback to system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        setDarkMode();
    }
})();
