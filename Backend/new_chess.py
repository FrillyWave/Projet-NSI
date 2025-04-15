import chess
import requests 
import json 

def Main():
    url = "https://projet-nsi-sffl.onrender.com"
    board = chess.Board()
    requests.post(url, json = board.fen())
    while not(board.is_checkmate()) and not(board.is_stalemate()) and not(board.is_insufficient_material()):
        reponse = requests.get(url)
        board = chess.Board([0])
        board.push(reponse[1])
        requests.post(url, json = board.fen())
        
