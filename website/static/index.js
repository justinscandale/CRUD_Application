//function to handle button click for deleting note
function deleteNote(noteID) {
    fetch('/delete-note', { 
        method : 'POST',
        body: JSON.stringify({noteID: noteID}),
    }).then((_res) => {
        window.location.href = "/";
    });
}

// Function to handle button click for refreshing data
function handleRefreshButtonClick() {
    fetch("/refresh-data", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            // Log success message
            console.log(data.message);

            // Update HTML or perform other actions if needed
            // For example, you can reload the page
            window.location.reload();
        })
        .catch(error => {
            console.error('Error refreshing data:', error);
        });
}

// Add event listener to the refresh button
const refreshButton = document.getElementById('refreshButton');
refreshButton.addEventListener('click', handleRefreshButtonClick);