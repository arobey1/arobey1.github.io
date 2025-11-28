/**
 * Dynamically loads the navbar and handles paths
 * This approach inlines the navbar HTML to eliminate the loading lag
 */
document.addEventListener('DOMContentLoaded', function() {
    // Calculate path back to root
    const currentPath = window.location.pathname;
    const pathSegments = currentPath.split('/').filter(segment => segment !== '');
    
    let rootPath = './';
    if (pathSegments.length > 0) {
        rootPath = '../'.repeat(pathSegments.length);
    }
    
    // Get the header element where we'll insert the navbar
    const header = document.querySelector('header');
    
    // Only proceed if header exists
    if (header) {
        // Inline the navbar HTML instead of loading it via fetch
        // This eliminates the network request and resulting lag
        const navbarHTML = `
            <div class="navbar">
                <a href="./" class="brand">Alex Robey</a>
                <nav>
                    <ul>
                        <li><a href="papers/">papers</a></li>
                        <li><a href="research/">research</a></li>
                        <li><a href="writing/">writing</a></li>
                        <li><a href="crosswords/">crosswords</a></li>
                        <li><a href="files/cv.pdf" target="_blank">cv</a></li>
                    </ul>
                </nav>
            </div>
        `;
        
        // Insert the navbar HTML
        header.innerHTML = navbarHTML;
        
        // Now update all the links in the navbar
        updateNavbarLinks(rootPath);
    } else {
        console.error('No header element found to insert navbar');
    }
});

/**
 * Updates all navbar links to point to the correct paths based on current page depth
 */
function updateNavbarLinks(rootPath) {
    // Update the home link
    const homeLink = document.querySelector('.navbar .brand');
    if (homeLink) {
        homeLink.href = rootPath;
    }
    
    // Update all nav links except those with target="_blank" or absolute URLs
    const navLinks = document.querySelectorAll('.navbar nav ul li a');
    navLinks.forEach(link => {
        const originalHref = link.getAttribute('href');
        
        // Skip external links and links with target="_blank"
        if (originalHref && !originalHref.startsWith('http') && 
            !originalHref.startsWith('/') && !link.hasAttribute('target')) {
            
            // Extract the section name (first directory in the path)
            const section = originalHref.split('/')[0];
            
            // Set the correct path to the root-level section
            link.href = rootPath + section + '/';
        }
    });
    
    // Special handling for the CV link which is a file, not a directory
    const cvLink = document.querySelector('.navbar nav ul li a[href*="cv.pdf"]');
    if (cvLink) {
        cvLink.href = rootPath + 'files/cv.pdf';
    }
} 