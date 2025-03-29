// Initialize Socket.IO
const socket = io();

// Listen for progress updates
socket.on('progress_update', function(data) {
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        progressBar.style.width = data.progress + '%';
        progressBar.setAttribute('aria-valuenow', data.progress);
        progressBar.textContent = data.progress + '%';
    }
});

// Listen for hard update start
socket.on('hard_update_start', function() {
    $('#uploadForm input, #uploadForm button').attr('disabled', true);
    $('#hardUpdateModal').modal('show');
});

// Listen for hard update end
socket.on('hard_update_end', function() {
    $('#uploadForm input, #uploadForm button').attr('disabled', false);
    $('#hardUpdateModal').modal('hide');
});

// Update the file input label with the selected file name
document.querySelector('.custom-file-input').addEventListener('change', function (e) {
    var fileName = document.getElementById("customFile").files[0].name;
    var nextSibling = e.target.nextElementSibling
    nextSibling.innerText = fileName
});

// Handle image click to show modal
document.querySelectorAll('.clickable-image').forEach(function (img) {
    img.addEventListener('click', function () {
        var src = img.getAttribute('data-src');
        document.getElementById('modalImage').setAttribute('src', src);
    });
});

// Handle form submission for upload
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    var fileInput = document.getElementById('customFile');
    if (fileInput.files.length === 0) {
        event.preventDefault();
        showErrorModal('No file selected. Please choose a file to upload.');
    }
});

// Handle form submission for database update
document.getElementById('updateForm').addEventListener('submit', function(event) {
    event.preventDefault();
    fetch('/update_database', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);  // Display a success message
            } else if (data.error) {
                showErrorModal(data.error);
            }
        })
        .catch(error => {
            showErrorModal('An error occurred while updating the database.');
        });
});

// Handle form submission for hard update
document.getElementById('hardUpdateForm').addEventListener('submit', function(event) {
    event.preventDefault();
    $('#hardUpdateModal').modal('show');  // Show hard update modal
    fetch('/hard_update_database', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);  // Display a success message
                $('#hardUpdateModal').modal('hide');  // Hide hard update modal
            } else if (data.error) {
                showErrorModal(data.error);
            }
        })
        .catch(error => {
            showErrorModal('An error occurred while updating the database.');
        });
});

// Handle form submission for downloading selected images
document.getElementById('downloadForm').addEventListener('submit', function(event) {
    var selectedImages = document.querySelectorAll('input[name="selected_images"]:checked');
    if (selectedImages.length === 0) {
        event.preventDefault();
        showErrorModal('No images selected. Please choose images to download.');
    }
});

function showErrorModal(message) {
    document.getElementById('errorMessage').innerText = message;
    $('#errorModal').modal('show');
}

// Show hidden button with ALT+H
document.addEventListener('keydown', function(event) {
    if (event.altKey && event.key === 'h') {
        event.preventDefault();
        var hardUpdateForm = document.getElementById('hardUpdateForm');
        if (hardUpdateForm) {
            if (hardUpdateForm.style.display === 'none') {
                hardUpdateForm.style.display = 'block';
            } else {
                hardUpdateForm.style.display = 'none';
            }
        }
    }
});
