document.addEventListener('DOMContentLoaded', () => {
    
    // Mobile menu toggle
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('show');
        });
    }

    // Dynamic Top Spacing to prevent navbar overlap
    const navbar = document.querySelector('.navbar');
    const resultsPage = document.querySelector('.results-page');
    const homePage = document.querySelector('.home-page');
    
    if (navbar) {
        const updateNavbarHeight = () => {
            const h = navbar.offsetHeight;
            // Provide 32px visual space below the navbar
            if (resultsPage) resultsPage.style.paddingTop = `${h + 32}px`;
            if (homePage) homePage.style.paddingTop = `${h + 32}px`;
        };
        updateNavbarHeight();
        window.addEventListener('resize', updateNavbarHeight);
    }

    // Quick Preference Chips
    const chips = document.querySelectorAll('.chip');
    const cuisineSelect = document.getElementById('cuisine');
    
    if (chips.length > 0 && cuisineSelect) {
        chips.forEach(chip => {
            chip.addEventListener('click', () => {
                // Remove active class from all
                chips.forEach(c => c.classList.remove('active'));
                
                const val = chip.getAttribute('data-value');
                
                // Find matching option in select
                let found = false;
                Array.from(cuisineSelect.options).forEach(opt => {
                    if (opt.value.toLowerCase() === val.toLowerCase()) {
                        opt.selected = true;
                        found = true;
                    }
                });
                
                if (found) {
                    chip.classList.add('active');
                } else {
                    // Fallback to Any if not found
                    cuisineSelect.value = 'Any';
                }
            });
        });
    }

    // Form loading state
    const form = document.getElementById('recommendation-form');
    const submitBtn = document.getElementById('submit-btn');
    
    if (form && submitBtn) {
        form.addEventListener('submit', () => {
            submitBtn.classList.add('is-loading');
            submitBtn.querySelector('.btn-text').textContent = 'Finding your perfect restaurants...';
            // Disable button to prevent double submit
            setTimeout(() => { submitBtn.disabled = true; }, 10);
        });
    }

    // Collapsible "Why this matches you"
    const whyBtns = document.querySelectorAll('.why-match-btn');
    whyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const content = btn.nextElementSibling;
            const isOpen = content.classList.contains('open');
            
            // Close all
            document.querySelectorAll('.why-match-content').forEach(c => c.classList.remove('open'));
            document.querySelectorAll('.why-match-btn svg').forEach(s => s.style.transform = 'rotate(0deg)');
            
            if (!isOpen) {
                content.classList.add('open');
                btn.querySelector('svg').style.transform = 'rotate(180deg)';
            }
        });
    });

    // Client-side Sorting
    const sortSelect = document.getElementById('sort-results');
    const resultsContainer = document.querySelector('.results-grid');
    
    if (sortSelect && resultsContainer) {
        sortSelect.addEventListener('change', (e) => {
            const cards = Array.from(resultsContainer.querySelectorAll('.restaurant-card'));
            const sortVal = e.target.value;
            
            cards.sort((a, b) => {
                if (sortVal === 'match') {
                    // Sort by Match Percentage (highest first)
                    const scoreA = parseFloat(a.getAttribute('data-score')) || 0;
                    const scoreB = parseFloat(b.getAttribute('data-score')) || 0;
                    return scoreB - scoreA;
                } else if (sortVal === 'rating') {
                    // Sort by Rating (highest first)
                    const ratA = parseFloat(a.getAttribute('data-rating')) || 0;
                    const ratB = parseFloat(b.getAttribute('data-rating')) || 0;
                    return ratB - ratA;
                } else if (sortVal === 'popular') {
                    // Sort by Votes (highest first)
                    const voteA = parseInt(a.getAttribute('data-votes')) || 0;
                    const voteB = parseInt(b.getAttribute('data-votes')) || 0;
                    return voteB - voteA;
                }
                return 0;
            });
            
            // Re-append in new order
            cards.forEach(card => resultsContainer.appendChild(card));
        });
    }
});
