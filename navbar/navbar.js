/**
 * Dynamic navbar script that ensures correct navigation regardless of page depth
 * This script calculates the relative paths to the site root and updates links accordingly
 */
document.addEventListener('DOMContentLoaded', function() {
    // Calculate the path depth based on current location
    const currentPath = window.location.pathname;
    const pathSegments = currentPath.split('/').filter(segment => segment !== '');
    
    // Calculate path back to root
    let rootPath = './';
    if (pathSegments.length > 0) {
        rootPath = '../'.repeat(pathSegments.length);
    }
    
    console.log('Current path:', currentPath);
    console.log('Path segments:', pathSegments);
    console.log('Calculated root path:', rootPath);
    
    // Update the home link to always go to the site root
    const homeLink = document.querySelector('.navbar .brand');
    if (homeLink) {
        homeLink.href = rootPath;
        console.log('Updated home link to:', homeLink.href);
    }
    
    // Get all main navigation links (excluding external links)
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
            console.log(`Updated link "${link.textContent}" from ${originalHref} to ${link.href}`);
        }
    });
    
    // Special handling for the CV link which is a file, not a directory
    const cvLink = document.querySelector('.navbar nav ul li a[href*="cv.pdf"]');
    if (cvLink) {
        cvLink.href = rootPath + 'files/cv.pdf';
        console.log('Updated CV link to:', cvLink.href);
    }
}); 