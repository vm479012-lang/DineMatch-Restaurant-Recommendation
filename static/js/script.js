document.addEventListener('DOMContentLoaded', () => {
    // Quick chips interaction
    const chips = document.querySelectorAll('.chip');
    const cuisineSelect = document.getElementById('cuisine');
    
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            const val = chip.getAttribute('data-value');
            if (cuisineSelect) {
                // Find and select the option
                for (let i = 0; i < cuisineSelect.options.length; i++) {
                    if (cuisineSelect.options[i].value === val) {
                        cuisineSelect.selectedIndex = i;
                        break;
                    }
                }
            }
            // Update active state
            chips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
        });
    });

    // Form submission animation
    const form = document.getElementById('recommendation-form');
    const submitBtn = document.getElementById('submit-btn');
    
    if (form && submitBtn) {
        form.addEventListener('submit', () => {
            submitBtn.classList.add('loading');
        });
    }

    // Sort interaction (client-side only for visual effect)
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            const grid = document.querySelector('.results-grid');
            const cards = Array.from(grid.children);
            
            cards.sort((a, b) => {
                const valA = sortSelect.value === 'rating' 
                    ? parseFloat(a.querySelector('.rating-badge').textContent.replace('⭐ ', ''))
                    : sortSelect.value === 'votes'
                    ? parseInt(a.querySelector('.card-meta div:nth-child(2)').textContent.trim().split(' ')[0])
                    : parseFloat(a.querySelector('.match-overlay').textContent.replace('🎯 ', '').replace('%', ''));
                    
                const valB = sortSelect.value === 'rating' 
                    ? parseFloat(b.querySelector('.rating-badge').textContent.replace('⭐ ', ''))
                    : sortSelect.value === 'votes'
                    ? parseInt(b.querySelector('.card-meta div:nth-child(2)').textContent.trim().split(' ')[0])
                    : parseFloat(b.querySelector('.match-overlay').textContent.replace('🎯 ', '').replace('%', ''));

                return valB - valA;
            });
            
            cards.forEach(card => grid.appendChild(card));
        });
    }

    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('nav-active');
        });
    }
});
