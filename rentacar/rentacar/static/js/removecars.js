function removeCar(carId) {

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/cars/${carId}`, {

        method: 'DELETE',
        headers: {

            'X-CSRFToken' : csrfToken,
            'Content-Type' : 'application/json',

        }

    })
    .then(response => {

        if(response.ok) {

            location.reload();

        } else {

            response.text().then(text=>alert('Failed to remove car ' + text));

        }

    })
    .catch(error => console.error('Error: ', error))

}