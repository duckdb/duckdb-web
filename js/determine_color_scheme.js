(function() {
    function setDarkMode() {
        document.documentElement.classList.add("darkmode");
        document.documentElement.classList.add('disable-transitions')
    }

    const userColorSchemePref = localStorage.getItem("mode");
    if (userColorSchemePref !== null) {
        // Use user preference
        return userColorSchemePref === 'dark' && setDarkMode();
    }

    // Fallback to system preference
    var systemPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (systemPrefersDark) {
        setDarkMode()
    }
})();
