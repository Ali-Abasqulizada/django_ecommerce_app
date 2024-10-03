function showLoader() {
    document.getElementById('loader').style.display = 'flex';
}

function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}

// Show loader when navigating away from the page
window.addEventListener('beforeunload', function (event) {
    showLoader();
});

// Hide loader when the page has fully loaded or is restored from cache
window.addEventListener('load', hideLoader);

// Handle page restore from cache using the 'pageshow' event
window.addEventListener('pageshow', function (event) {
    if (event.persisted) { // If page is restored from cache (bfcache)
        hideLoader();
    }
});

// Handle link clicks to show loader
document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', function (e) {
        if (!link.href.startsWith('#')) { // Check for non-hash links
            showLoader();
        }
    });
});

// Prevent the loader from showing on back/forward navigation
window.onpopstate = function () {
    hideLoader(); // Explicitly hide the loader when using back/forward buttons
};
