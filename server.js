const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const fs = require('fs');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const { spawn } = require('child_process');

const app = express();
const PORT = 3002;

// Middleware pour autoriser les requêtes CORS
app.use(cors());

// Middleware pour parser le JSON dans le corps des requêtes
app.use(express.json());

// Serveur pour les fichiers statiques (Frontend)
app.use(express.static(path.join(__dirname, "Frontend/html")));
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "Frontend/html/connexion.html"));
});

// Route pour ajouter un nouvel utilisateur
app.post('/register', async (req, res) => {
    const { username, password } = req.body; // Récupération des informations envoyées par le client
    const filePath = path.join(__dirname, 'Data', 'users.json'); // Définir le chemin du fichier où les utilisateurs sont enregistrés

    // Vérifier si les champs requis sont présents
    if (!username || !password) {
        return res.status(400).json({ error: 'Tous les champs sont requis' });
    }

    console.log("Nouvel utilisateur :", username);

    // Hachage du mot de passe
    const hashedPassword = await bcrypt.hash(password, 10); // Le "10" est le nombre de rounds de salage

    // Lire le fichier JSON où sont stockés les utilisateurs
    fs.readFile(filePath, 'utf8', (err, data) => {
        let users = [];

        // Si le fichier existe et contient des données, on les parse
        if (!err && data) {
            try {
                users = JSON.parse(data);
            } catch (parseErr) {
                console.error('Erreur parsing JSON :', parseErr);
                return res.status(500).json({ error: 'Erreur de lecture des utilisateurs' });
            }
        }

        // Vérifier si l'utilisateur existe déjà
        if (users.some(user => user.username === username)) {
            return res.status(400).json({ error: 'Nom d’utilisateur déjà pris' });
        }

        // Ajouter le nouvel utilisateur à la liste avec le mot de passe haché
        users.push({ username, password: hashedPassword });

        // Sauvegarder le fichier mis à jour
        fs.writeFile(filePath, JSON.stringify(users, null, 2), (writeErr) => {
            if (writeErr) {
                console.error('Erreur d’écriture dans le fichier :', writeErr);
                return res.status(500).json({ error: 'Impossible d’enregistrer l’utilisateur' });
            }
            console.log(`Utilisateur ${username} enregistré avec succès !`);
            res.status(201).json({ message: 'Utilisateur créé avec succès' });
        });
    });
});

// Route pour la connexion d'un utilisateur
app.post('/login', async (req, res) => {
    const { username, password } = req.body; // Récupérer les informations d'identification envoyées

    const filePath = path.join(__dirname, 'Data', 'users.json'); // Le chemin vers le fichier des utilisateurs

    // Lire le fichier JSON pour vérifier les informations de connexion
    fs.readFile(filePath, 'utf8', async (err, data) => {
        if (err) {
            console.error("Erreur de lecture du fichier :", err);
            return res.status(500).send('Erreur interne du serveur');
        }

        const users = JSON.parse(data || '[]'); // Parser les données ou retourner un tableau vide si aucune donnée
        const user = users.find(u => u.username === username); // Trouver l'utilisateur avec le nom d'utilisateur correspondant

        // Si l'utilisateur est trouvé, vérifier le mot de passe
        if (user) {
            const isPasswordValid = await bcrypt.compare(password, user.password); // Comparer le mot de passe fourni avec le haché

            if (isPasswordValid) {
                res.send('Connexion réussie');
            } else {
                res.status(400).send(`Nom d'utilisateur ou mot de passe incorrect`);
            }
        } else {
            // Si l'utilisateur n'est pas trouvé, retourner une erreur
            res.status(400).send(`Nom d'utilisateur ou mot de passe incorrect`);
        }
    });
});

// Définir le chemin vers le script Python
const scriptPath = path.join(__dirname, "Backend", "projet_Python.py");

// Route GET pour initialiser l'échiquier
app.get("/api/init", (req, res) => {
    console.log("Appel à /api/init")
    // Lancer le script Python pour générer l'échiquier
    const pythonProcess = spawn("python3", [scriptPath]);

    let output = "";

    // Capture la sortie du script Python
    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    // Gestion des erreurs du script Python
    pythonProcess.stderr.on("data", (data) => {
        console.error(`Erreur Python : ${data}`);
    });

    // Quand le processus Python se termine
    pythonProcess.on("close", (code) => {
        if (code !== 0) {
            console.error(`Le processus Python a échoué avec le code ${code}`);
            return res.status(500).json({ error: "Erreur lors de l'exécution du script Python." });
        }

        // Retourner l'échiquier généré en JSON
        try {
            const echiquier = JSON.parse(output);
            res.json({ echiquier });
        } catch (error) {
            console.error("Erreur de parsing JSON : ", error);
            res.status(500).json({ error: "Erreur lors du traitement du JSON." });
        }
    });
});

// Route POST pour jouer un coup
app.post("/api/jouer", (req, res) => {
    console.log(">>> /api/jouer appelée avec :", req.body);
    const { coup, echiquier } = req.body;

    // Vérifier si les données sont présentes
    if (!coup || !echiquier) {
        return res.status(400).json({ error: "Les données requises (coup et echiquier) sont manquantes." });
    }

    // Lancer le script Python pour traiter le coup
    const pythonProcess = spawn("python3", [scriptPath, JSON.stringify(echiquier), coup]);

    let output = "";

    // Capture la sortie du script Python
    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    // Gestion des erreurs du script Python
    pythonProcess.stderr.on("data", (data) => {
        console.error(`Erreur Python : ${data}`);
    });

    // Quand le processus Python se termine
    pythonProcess.on("close", (code) => {
        if (code !== 0) {
            console.error(`Le processus Python a échoué avec le code ${code}`);
            return res.status(500).json({ error: "Erreur lors de l'exécution du script Python." });
        }

        // Retourner l'échiquier mis à jour
        try {
            const echiquierMisAJour = JSON.parse(output);
            res.json({ echiquier: echiquierMisAJour });
        } catch (error) {
            console.error("Erreur de parsing JSON : ", error);
            res.status(500).json({ error: "Erreur lors du traitement du JSON." });
        }
    });
});

// Lancer le serveur
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Serveur en cours d'exécution sur http://0.0.0.0:${PORT}`);
});
