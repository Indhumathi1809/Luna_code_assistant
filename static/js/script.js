document.getElementById('createRepoModal').addEventListener('click', function() {
    document.getElementById('createRepoModalOverlay').style.display = 'block';
});

document.getElementById('createRepoModalOverlay').addEventListener('click', function(event) {
    if (event.target === this) {
        this.style.display = 'none';
    }
});

document.getElementById('createRepoCloseModal').addEventListener('click', function() {
    document.getElementById('createRepoModalOverlay').style.display = 'none';
});

document.getElementById('createRepoForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const repoName = document.getElementById('createRepoName').value;
    const repoDescription = document.getElementById('createRepoDescription').value;
    const visibility = document.querySelector('input[name="createVisibility"]:checked').value;
    
    const token = 'your_token'; // Replace with your GitHub personal access token
    
    fetch('https://api.github.com/user/repos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'token ' + token
        },
        body: JSON.stringify({
            name: repoName,
            description: repoDescription,
            visibility: visibility,
            auto_init: true
        })
    })
    .then(response => {
        if (response.ok) {
            alert('Repository created successfully!');
            document.getElementById('createRepoModalOverlay').style.display = 'none';
        } else {
            response.json().then(data => {
                alert('Error: ' + data.message);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while creating the repository. Please try again.');
    });
});

document.getElementById('listRepoModal').addEventListener('click', function() {
    document.getElementById('listRepoModalOverlay').style.display = 'block';
    fetchRepositories();
});

document.getElementById('listRepoModalOverlay').addEventListener('click', function(event) {
    if (event.target === this) {
        this.style.display = 'none';
    }
});

document.getElementById('listRepoCloseModal').addEventListener('click', function() {
    document.getElementById('listRepoModalOverlay').style.display = 'none';
});

function fetchRepositories() {
    const token = 'YOUR_TOKEN'; // Replace with your GitHub personal access token
    
    fetch('https://api.github.com/user/repos', {
        headers: {
            'Authorization': 'token ' + token
        }
    })
    .then(response => response.json())
    .then(data => {
        const repoList = document.getElementById('repoList');
        repoList.innerHTML = '';
        data.forEach(repo => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<span class="repo-name">${repo.name}</span>: ${repo.description}`;
            repoList.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while fetching the repositories. Please try again.');
    });
}

document.getElementById('createFileModal').addEventListener('click', function() {
    document.getElementById('createFileModalOverlay').style.display = 'block';
});

document.getElementById('createFileModalOverlay').addEventListener('click', function(event) {
    if (event.target === this) {
        this.style.display = 'none';
    }
});

document.getElementById('createFileCloseModal').addEventListener('click', function() {
    document.getElementById('createFileModalOverlay').style.display = 'none';
});

document.getElementById('createFileForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const repoName = document.getElementById('repoName').value;
    const filePath = document.getElementById('filePath').value;
    const fileContent = document.getElementById('fileContent').value;

    const token = 'YOUR_TOKEN'; // Replace with your GitHub personal access token
    
    fetch(`https://api.github.com/repos/${repoName}/contents/${filePath}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'token ' + token
        },
        body: JSON.stringify({
            message: 'Create new file',
            content: btoa(fileContent), // Encoding content to base64
        })
    })
    .then(response => {
        if (response.ok) {
            alert('File created successfully!');
            document.getElementById('createFileModalOverlay').style.display = 'none';
        } else {
            response.json().then(data => {
                alert('Error: ' + data.message);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while creating the file. Please try again.');
    });
});





document.getElementById('uploadFileModal').addEventListener('click', function() {
    document.getElementById('uploadFileModalOverlay').style.display = 'block';
});

document.getElementById('uploadFileModalOverlay').addEventListener('click', function(event) {
    if (event.target === this) {
        this.style.display = 'none';
    }
});

document.getElementById('uploadFileCloseModal').addEventListener('click', function() {
    document.getElementById('uploadFileModalOverlay').style.display = 'none';
});

document.getElementById('uploadFileForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const repoName = document.getElementById('uploadRepoName').value;
    const filePath = document.getElementById('uploadFilePath').value;
    const fileToUpload = document.getElementById('fileToUpload').files[0];

    const reader = new FileReader();
    reader.onload = function() {
        const fileContent = reader.result.split(',')[1]; // Extracting base64-encoded content
        const token = 'your_token'; // Replace with your GitHub personal access token
        
        fetch(`https://api.github.com/repos/${repoName}/contents/${filePath}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + token
            },
            body: JSON.stringify({
                message: 'Upload new file',
                content: fileContent, // Sending base64-encoded content directly
                encoding: 'base64' // Indicating that the content is base64-encoded
            })
        })
        .then(response => {
            if (response.ok) {
                alert('File uploaded successfully!');
                document.getElementById('uploadFileModalOverlay').style.display = 'none';
            } else {
                response.json().then(data => {
                    alert('Error: ' + data.message);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while uploading the file. Please try again.');
        });
    };
    reader.readAsDataURL(fileToUpload); // Reading the selected file as a data URL
});


// Commit Changes Modal
document.getElementById('commitChangesModal').addEventListener('click', function() {
document.getElementById('commitChangesModalOverlay').style.display = 'block';
});

document.getElementById('commitChangesCloseModal').addEventListener('click', function() {
document.getElementById('commitChangesModalOverlay').style.display = 'none';
});

document.getElementById('commitChangesForm').addEventListener('submit', function(event) {
event.preventDefault();

const repoName = document.getElementById('commitRepoName').value;
const fileName = document.getElementById('commitFileName').value;
const commitMessage = document.getElementById('commitMessage').value;

const token = 'YOUR_TOKEN'; // Replace with your GitHub personal access token

fetch(`https://api.github.com/repos/${repoName}/contents/${fileName}`, {
method: 'PUT',
headers: {
    'Content-Type': 'application/json',
    'Authorization': 'token ' + token
},
body: JSON.stringify({
    message: commitMessage,
    content: btoa('Your file content here') // Encode file content to base64
})
})
.then(response => {
if (response.ok) {
    alert('File committed successfully!');
    document.getElementById('commitChangesModalOverlay').style.display = 'none';
} else {
    response.json().then(data => {
        alert('Error: ' + data.message);
    });
}
})
.catch(error => {
console.error('Error:', error);
alert('An error occurred while committing changes. Please try again.');
});
});


// Push Button
document.getElementById('pushButton').addEventListener('click', function() {
document.getElementById('pushModalOverlay').style.display = 'block';
});

// Close Push Modal
document.getElementById('pushCloseModal').addEventListener('click', function() {
document.getElementById('pushModalOverlay').style.display = 'none';
});

// Push Form Submission
document.getElementById('pushForm').addEventListener('submit', function(event) {
event.preventDefault();

const repoName = document.getElementById('pushRepoName').value;

// Implement push functionality
fetch('/push', {
method: 'POST',
headers: {
    'Content-Type': 'application/json'
},
body: JSON.stringify({ repoName: repoName })
})
.then(response => {
if (response.ok) {
    alert('Pushed changes successfully!');
    document.getElementById('pushModalOverlay').style.display = 'none';
} else {
    throw new Error('Failed to push changes');
}
})
.catch(error => {
console.error('Error:', error);
alert('An error occurred while pushing changes.');
});
});

// Pull Button
document.getElementById('pullButton').addEventListener('click', function() {
document.getElementById('pullModalOverlay').style.display = 'block';
});

// Close Pull Modal
document.getElementById('pullCloseModal').addEventListener('click', function() {
document.getElementById('pullModalOverlay').style.display = 'none';
});

// Pull Form Submission
document.getElementById('pullForm').addEventListener('submit', function(event) {
event.preventDefault();

const repoName = document.getElementById('pullRepoName').value;

// Implement pull functionality
fetch('/pull', {
method: 'POST',
headers: {
    'Content-Type': 'application/json'
},
body: JSON.stringify({ repoName: repoName })
})
.then(response => {
if (response.ok) {
    alert('Pulled changes successfully!');
    document.getElementById('pullModalOverlay').style.display = 'none';
} else {
    throw new Error('Failed to pull changes');
}
})
.catch(error => {
console.error('Error:', error);
alert('An error occurred while pulling changes.');
});
});
// Clone Button
document.getElementById('cloneButton').addEventListener('click', function() {
    document.getElementById('cloneModalOverlay').style.display = 'block';
});

// Close Clone Modal
document.getElementById('cloneCloseModal').addEventListener('click', function() {
    document.getElementById('cloneModalOverlay').style.display = 'none';
});

// Clone Form Submission
document.getElementById('cloneForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const repoUrl = document.getElementById('cloneRepoUrl').value;
    
    // Implement clone functionality
    fetch('/clone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ repoUrl: repoUrl })
    })
    .then(response => {
        if (response.ok) {
            alert('Cloned repository successfully!');
            document.getElementById('cloneModalOverlay').style.display = 'none';
        } else {
            throw new Error('Failed to clone repository');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while cloning repository.');
    });
});