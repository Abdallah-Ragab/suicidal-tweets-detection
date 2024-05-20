// function submitUsername() {
//     const username = document.getElementById('username').value;
//     if (username.trim() === "") {
//         alert("Please enter a username");
//         return;
//     }

//     // Show loading screen
//     document.getElementById('input-screen').classList.add('hidden');
//     document.getElementById('loading-screen').classList.remove('hidden');

//     // Make a GET request to /task endpoint
//     fetch(`localhost:8000/task?username=${username}`)
//         .then(response => response.json())
//         .then(data => {
//             const taskId = data.task_id;
//             checkTaskStatus(taskId);
//         })
//         .catch(error => {
//             console.error("Error:", error);
//             alert("An error occurred. Please try again.");
//         });
// }

// function checkTaskStatus(taskId) {
//     fetch(`localhost:8000/check?task_id=${taskId}`)
//         .then(response => response.json())
//         .then(data => {
//             const statusMessage = data.status.message;
//             document.getElementById('status-message').innerText = statusMessage;

//             if (data.status.code === 6 || data.status.code === 7) {
//                 // Task is done, show result screen
//                 document.getElementById('loading-screen').classList.add('hidden');
//                 document.getElementById('result-message').innerText = statusMessage;
//                 document.getElementById('result-screen').classList.remove('hidden');
//             } else {
//                 // Poll again after a delay
//                 setTimeout(() => checkTaskStatus(taskId), 1000);
//             }
//         })
//         .catch(error => {
//             console.error("Error:", error);
//             alert("An error occurred. Please try again.");
//         });
// }

window.gdata = {};

function submitUsername() {
    const username = document.getElementById('username').value;
    if (username.trim() === "") {
        alert("Please enter a username");
        return;
    }

    // Show loading screen
    document.getElementById('input-screen').classList.add('hidden');
    document.getElementById('loading-screen').classList.remove('hidden');

    // Make a GET request to /task endpoint
    fetch(`http://localhost:8000/task?username=${username}`)
        .then(response => response.json())
        .then(data => {
            const taskId = data.task_id;
            checkTaskStatus(taskId);
            console.log(data);
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
}

function checkTaskStatus(taskId) {
    fetch(`http://localhost:8000/check?task_id=${taskId}`)
        .then(response => response.json())
        .then(data => {
            const statusMessage = data.status.message;
            document.getElementById('status-message').innerText = statusMessage;
            window.gdata = data;
            if (data.status.code === 6 || data.status.code === 7) {
                // Task is done, show result screen
                document.getElementById('loading-screen').classList.add('hidden');
                document.getElementById('result-message').innerText = data.message;
                document.getElementById('result-list').innerText = data.ps_tweets.tweets;
                document.getElementById('result-screen').classList.remove('hidden');
            } else {
                // Poll again after a delay
                setTimeout(() => checkTaskStatus(taskId), 1000);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
}
