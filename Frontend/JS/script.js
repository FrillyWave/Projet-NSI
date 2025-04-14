document.addEventListener('DOMContentLoaded', () => {
    /**
     * Gestion du formulaire de connexion
     */
    const connexion_form = document.getElementById('connexion_form');
    const errorMessage = document.getElementById('errorMessage'); // Conteneur pour afficher les erreurs

    // Vérifie si le formulaire de connexion existe sur la page
    if (connexion_form) {
        // Écoute l'événement de soumission du formulaire
        connexion_form.addEventListener('submit', function (event) {
            event.preventDefault(); // Empêche le rechargement de la page lors de la soumission
    
            // Récupère les valeurs des champs de formulaire (nom d'utilisateur et mot de passe)
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
    
            // Vérifie si les champs sont vides
            if (!username || !password) {
                alert("Veuillez remplir tous les champs.");
                return;
            }
    
            // Envoie les données au serveur via une requête POST
            fetch('https://projet-nsi-sffl.onrender.com/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
            .then(response => {
                // Si la réponse n'est pas correcte (non OK), on gère l'erreur
                if (!response.ok) {
                    return response.text().then(errorText => { throw new Error(errorText); });
                }
                return response.text();
            })
            .then(data => {
                // Réponse du serveur après la connexion réussie
                console.log('Réponse du serveur :', data);
                // Enregistre le profil de l'utilisateur dans le localStorage
                localStorage.setItem('userProfile', JSON.stringify({ username }));
                // Redirige l'utilisateur vers la page principale
                window.location.href = '../html/main.html';
            })
            .catch(error => {
                // Si une erreur survient lors de la requête, on l'affiche
                console.error('Erreur lors de la connexion :', error);
                errorMessage.style.display = 'block';
                errorMessage.textContent = error.message;
            });
        });
    }
})

    

document.addEventListener('DOMContentLoaded', () => {
    const signUpForm = document.getElementById('sign_up-form');
    const errorMessage = document.getElementById('errorMessage'); // Conteneur pour afficher les erreurs

    // Vérifie si le formulaire d'inscription existe sur la page
    if (signUpForm) {
        signUpForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Empêche le rechargement de la page lors de la soumission
    
            // Récupère les valeurs des champs du formulaire (nom d'utilisateur, mot de passe et validation du mot de passe)
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            const validPassword = document.getElementById('valid-password').value.trim();
    
            // Vérifie si les champs sont vides
            if (!username || !password || !validPassword) {
                alert("Veuillez remplir tous les champs.");
                return;
            }

            // Vérifie si les mots de passe correspondent
            if (password !== validPassword) {
                alert("Les mots de passe ne correspondent pas.");
                return;
            }

            console.log("Envoi des données au serveur...");

            try {
                // Envoie les données d'inscription au serveur
                const response = await fetch('https://projet-nsi-sffl.onrender.com/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                console.log("Réponse reçue du serveur :", response);

                // Si la réponse n'est pas OK, on gère l'erreur
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(errorText);
                }

                const data = await response.json();
                console.log("Inscription réussie :", data);

                // Enregistre l'utilisateur en localStorage pour qu'il reste connecté
                localStorage.setItem('userProfile', JSON.stringify({ username }));

                // Redirection vers la page principale
                console.log("Redirection vers main.html...");
                window.location.href = '../html/main.html';

            } catch (error) {
                // Si une erreur survient lors de l'inscription, on l'affiche
                console.error('Erreur lors de l’inscription :', error);
                errorMessage.style.display = 'block';
                errorMessage.textContent = error.message;
            }
        });
    }
});

/**
 * Fonction pour quitter une fenêtre ou rediriger vers une autre page
 */
function refresh() {
    let openedWindow

    openedWindow = window.open("../html/main.html");
    openedWindow = window.close("../html/main.html");
}

function valider() {
    let depart = document.getElementById("origine").value.toLowerCase();
    let arrivee = document.getElementById("destination").value.toLowerCase();

    // Expression régulière pour valider les cases d'échecs (ex: e2, h7)
    const regexCase = /^[a-h][1-8]$/;

    // Vérification que les deux cases sont valides
    if (!regexCase.test(depart) || !regexCase.test(arrivee)) {
        document.getElementById("output").textContent = "❌ Case invalide. Exemple attendu : E2 vers E4";
        return;
    }

    // Récupération de l'échiquier depuis le localStorage
    const echiquier = JSON.parse(localStorage.getItem("echiquier"));
    // Création du coup
    const coup = depart + arrivee;

    fetch("https://projet-nsi-sffl.onrender.com/api/jouer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ coup, echiquier }) // Envoi de l'échiquier avec le coup
    })
    .then(response => response.json())
    .then(data => {
        console.log("Échiquier après coup :", data.echiquier);
        localStorage.setItem("echiquier", JSON.stringify(data.echiquier)); // Mise à jour du localStorage
        document.getElementById("output").textContent = "Coup joué !";
    })
    .catch(error => {
        console.error("Erreur lors du coup :", error);
        document.getElementById("output").textContent = "Erreur lors de l'envoi du coup.";
    });
}

// Fonction pour afficher l'échiquier dans la console
function afficherEchiquierConsole(echiquier) {
    for (let i = 0; i < 8; i++) {
        console.log(echiquier[i].join(' ')); // Affiche chaque ligne de l'échiquier
    }
}

// Fonction pour démarrer la partie et récupérer l'échiquier
function lancerPartie() {
    fetch("https://projet-nsi-sffl.onrender.com/api/init")
        .then(response => response.json())
        .then(data => {
            // Récupérer l'échiquier initial
            const echiquier = data.echiquier;
            
            // Stocker l'échiquier dans localStorage pour une utilisation future
            localStorage.setItem("echiquier", JSON.stringify(echiquier));

            console.log("Échiquier initialisé :", echiquier);
            document.getElementById("output").textContent = "Échiquier initialisé !";
        })
        .catch(error => {
            console.error("Erreur lors de l'initialisation :", error);
            document.getElementById("output").textContent = "Erreur lors de l'initialisation.";
        });
}


