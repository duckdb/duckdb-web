(function() {
    function setDarkMode() {
        document.documentElement.classList.add("darkmode");
        document.documentElement.classList.add('disable-transitions');
        document.documentElement.style.backgroundColor = '#0d0d0d';
        document.documentElement.style.colorScheme = 'dark';
    }

    function setLightMode() {
        document.documentElement.classList.remove("darkmode");
        document.documentElement.style.backgroundColor = '';
        document.documentElement.style.colorScheme = '';
    }

    try {
        var userColorSchemePref = localStorage.getItem("mode");
        if (userColorSchemePref !== null) {
            if (userColorSchemePref === 'dark') {
                setDarkMode();
            } else {
                setLightMode();
            }
            return;
        }
    } catch (e) {}

    // Fallback to system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        setDarkMode();
    } else {
        setLightMode();
    }
})();
