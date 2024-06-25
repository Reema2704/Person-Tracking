// Submit the form on button click
document.getElementById("loginForm").onsubmit = function(event) {
    event.preventDefault();
    
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    
    // Send a POST request to the login API endpoint
    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Login successful") {
            // Redirect to a success page or perform other actions
            window.location.href = "/success";
        } else {
            // Display error message in the snackbar
            var snackbar = document.getElementById("snackbar");
            snackbar.innerText = "Invalid username or password";
            snackbar.classList.add("show");
            
            // Hide snackbar after 3 seconds
            setTimeout(function() {
                snackbar.classList.remove("show");
            }, 3000);
        }
    })
    .catch(error => console.error(error));
};


