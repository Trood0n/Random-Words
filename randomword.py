import tkinter as tk
import os
from datetime import datetime
import requests

# URL de téléchargement de la liste de mots
WORD_LIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
LOCAL_FILE_PATH = 'words-EN.txt'

# API de Random.org pour obtenir un vrai nombre aléatoire
def get_random_number(min_val, max_val):
    url = f"https://www.random.org/integers/?num=1&min={min_val}&max={max_val}&col=1&base=10&format=plain&rnd=new"
    response = requests.get(url)
    response.raise_for_status()  # Vérifie les erreurs
    return int(response.text.strip())

# Fonction pour télécharger la liste de mots depuis GitHub
def download_word_list():
    response = requests.get(WORD_LIST_URL)
    if response.status_code == 200:
        with open(LOCAL_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("La liste de mots a été téléchargée.")
    else:
        print("Erreur lors du téléchargement de la liste de mots.")

# Fonction pour obtenir un mot aléatoire depuis le fichier
def get_random_word():
    # Vérifie si le fichier existe, sinon le télécharge
    if not os.path.exists(LOCAL_FILE_PATH):
        download_word_list()
    
    # Lire le fichier et renvoyer un mot aléatoire
    with open(LOCAL_FILE_PATH, 'r', encoding='utf-8') as f:
        words = f.read().splitlines()

    # Utiliser Random.org pour obtenir un vrai nombre aléatoire
    random_index = get_random_number(0, len(words) - 1)
    return words[random_index]

# Création de la fenêtre
def create_window():
    print("Création de la fenêtre...")
    window = tk.Tk()
    window.title("Générateur de mots")
    window.config(bg="white")

    # Date ajd
    date_label = tk.Label(window, text=datetime.now().strftime("%d/%m/%Y"), font=("Arial", 14), bg="white")
    date_label.pack(pady=10)

    # Création d'un widget Text
    text_widget = tk.Text(window, font=("Arial", 18), bg="white", wrap=tk.WORD, bd=0, height=10, width=50)
    text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Fonction pour ajouter un mot à l'affichage
    def on_key_press(event):
        if event.keysym == 'space' or event.keysym == 'Return':
            new_word = get_random_word()
            current_text = text_widget.get("1.0", tk.END)
            updated_text = current_text.strip() + " " + new_word
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, updated_text)

    # Lier la fonction de pression de touche
    window.bind("<KeyPress>", on_key_press)

    # Afficher la fenêtre
    print("Affichage de la fenêtre...")
    window.mainloop()

if __name__ == "__main__":
    create_window()
