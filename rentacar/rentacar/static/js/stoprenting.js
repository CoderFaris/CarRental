function removeCar(carId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/rentings/${carId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (response.ok) {
            // Remove the car entry from the list
            location.reload();
        } else {
            response.text().then(text => alert('Failed to remove the car. ' + text));
        }
    })
    .catch(error => console.error('Error:', error));
}
