document.addEventListener('DOMContentLoaded', function () {
    // Show the default content
    showContent('info-content');  // Change this line to set the default content to 'info-content'

    // Add click event listeners to each link
    document.getElementById('cv-link').addEventListener('click', function () {
        showContent('cv-content');
    });

    document.getElementById('german-link').addEventListener('click', function () {
        showContent('german-content');
    });

    document.getElementById('settings-link').addEventListener('click', function () {
        showContent('settings-content');
    });

    document.getElementById('info-link').addEventListener('click', function () {
        showContent('info-content');
    });

    function showContent(contentId) {
        // Hide all content divs
        var contentDivs = document.querySelectorAll('.profile-content');
        contentDivs.forEach(function (div) {
            div.style.display = 'none';
        });

        // Show the selected content
        document.getElementById(contentId).style.display = 'block';
    }
});
