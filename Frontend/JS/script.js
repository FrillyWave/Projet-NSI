function handleSubmit(event) {
event.preventDefault(); // Empêche la soumission du formulaire

    // Récupérer les valeurs du formulaire
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Ajouter ici la logique de vérification des données (par exemple, vérification côté serveur)

    // Si les données sont valides, rediriger vers la page main.html
    if (username && password) {
        window.location.href = "../Frontend/main.html"; // Redirection vers main.html
    } else {
        document.getElementById('errorMessage').textContent = "Nom d'utilisateur ou mot de passe incorrect.";
        document.getElementById('errorMessage').style.display = "block";
}
}

