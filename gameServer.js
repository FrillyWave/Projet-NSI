const express = require('express')
const { spawn } = require('child_process')
const path = require('path')
const app = express()

const port = 4000 

const scriptPath = path.join(__dirname, "Backend", "projet_Python.py")

app.get("/api/run-python", (req, res) => {
    const pythonProcess = spawn("python3", [scriptPath]);

    let output = "";
    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    pythonProcess.on("close", (code) => {
        console.log(`Processus Python terminé avec le code ${code}`);
        res.json({ output });
    });
    
    pythonProcess.stderr.on("data", (data) => {
        console.error(`Erreur Python : ${data}`);
    });
    
});

app.listen(port, () => {
    console.log(`Jeu serveur Express en écoute sur http://localhost:${port}`);
});
