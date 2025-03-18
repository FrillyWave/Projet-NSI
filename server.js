const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const cors = require('cors'); // Middleware CORS

const app = express();
const PORT = 3001;

app.use(cors());
app.use(bodyParser.json());

// Endpoint pour ajouter un joueur
app.post('/add-player', (req, res) => {
    const newPlayer = req.body;

    // Vérifie les données de base
    if (!newPlayer.name || !newPlayer.password) {
        return res.status(400).send('Erreur : Nom et mot de passe requis.');
    }

    const filePath = path.join(__dirname, 'Data', 'users.json');

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Erreur de lecture du fichier :', err);
            return res.status(500).send('Erreur interne du serveur.');
        }

        const players = JSON.parse(data || '[]');

        // Vérifie si le joueur existe déjà
        if (players.some(player => player.name === newPlayer.name)) {
            return res.status(400).send(`Erreur : Le joueur "${newPlayer.name}" existe déjà.`);
        }

        players.push(newPlayer);

        fs.writeFile(filePath, JSON.stringify(players, null, 2), (err) => {
            if (err) {
                console.error('Erreur d\'écriture du fichier :', err);
                return res.status(500).send('Erreur interne du serveur.');
            }

            res.send('Profil ajouté avec succès!');
        });
    });
});

// Endpoint pour supprimer un joueur
app.post('/delete-player', (req, res) => {
    const { name, password } = req.body;

    if (!name || !password) {
        return res.status(400).send({ success: false, message: 'Nom et mot de passe requis.' });
    }

    const filePath = path.join(__dirname, 'data', 'players.json');

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Erreur de lecture du fichier :', err);
            return res.status(500).send({ success: false, message: 'Erreur interne du serveur.' });
        }

        let players = JSON.parse(data || '[]');

        const playerIndex = players.findIndex(player => player.name === name && player.password === password);

        if (playerIndex === -1) {
            return res.status(404).send({ success: false, message: 'Profil introuvable ou mot de passe incorrect.' });
        }

        players.splice(playerIndex, 1);

        fs.writeFile(filePath, JSON.stringify(players, null, 2), (err) => {
            if (err) {
                console.error('Erreur d\'écriture du fichier :', err);
                return res.status(500).send({ success: false, message: 'Erreur interne du serveur.' });
            }

            res.send({ success: true, message: 'Profil supprimé avec succès.' });
        });
    });
});

app.post('/update-progress', (req, res) => {
    const { name, currentPage } = req.body;

    if (!name || !currentPage) {
        return res.status(400).send('Nom et page actuelle requis');
    }

    const filePath = path.join(__dirname, 'player.json');

    // Charger le fichier JSON
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) return res.status(500).send('Erreur lecture fichier JSON');

        const players = JSON.parse(data);

        // Trouver et mettre à jour le joueur
        const player = players.find(p => p.name === name);
        if (!player) return res.status(404).send('Joueur non trouvé');

        player.currentPage = currentPage;

        // Sauvegarder le fichier mis à jour
        fs.writeFile(filePath, JSON.stringify(players, null, 2), (err) => {
            if (err) return res.status(500).send('Erreur écriture fichier JSON');
            res.send('Progression mise à jour');
        });
    });
});

app.listen(PORT, () => {
    console.log(`Serveur en cours d'exécution sur http://localhost:${PORT}`);
});
