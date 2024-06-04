document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star-rating input[type="radio"]');
    stars.forEach(star => {
        star.addEventListener('change', function() {
            const score = document.querySelector('input[name="score"]:checked').value;
            
            console.log('Selected score:', score);
        });
    });
});