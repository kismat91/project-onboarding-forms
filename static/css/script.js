document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Define an array of allowed credentials
    const allowedCredentials = [
        { username: 'admin', password: 'password123' },
        { username: 'user1', password: 'pass1' },
        { username: 'user2', password: 'pass2' }
    ];

    // Check if the entered credentials match any of the allowed credentials
    const isValidUser = allowedCredentials.some(creds => 
        creds.username === username && creds.password === password
    );
    if (isValidUser) {
        // Redirect to the home page if the login is successful
        document.cookie = 'isLogIn=True; SameSite=Lax; Path=/';
        window.location.href = '/records_form';
    } else {
        // Optionally, inform the user that the login attempt has failed
        alert('Invalid credentials. Please try again.');
    }
});
