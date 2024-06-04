document.getElementById('check-notifications-btn').addEventListener('click', function() {
    fetch('/check_notifications/')
        .then(response => response.json())
        .then(data => {
            let notificationsDiv = document.getElementById('notifications');
            notificationsDiv.innerHTML = ''; 
            data.forEach(notification => {
                let card = document.createElement('div');
                card.className = 'card mb-3';
                
                let cardBody = document.createElement('div');
                cardBody.className = 'card-body';
                
                let cardText = document.createElement('p');
                cardText.className = 'card-text';
                
                var date = new Date(notification.created_at);
                var formattedDate = date.toISOString().replace('T', ' ').split('.')[0];
                
                cardText.textContent = notification.message + ' at ' + formattedDate;
                
                cardBody.appendChild(cardText);
                card.appendChild(cardBody);
                notificationsDiv.appendChild(card);
            });
        })
        .catch(error => console.error('Error:', error));
});