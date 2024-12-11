#!/usr/bin/env python3
import os
import csv
import click
import pandas as pd
from pathlib import Path

class TranslationManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.ensure_directories()

    def ensure_directories(self):
        """S'assure que les répertoires nécessaires existent"""
        for lang in ['english', 'french']:
            (self.base_dir / lang).mkdir(exist_ok=True)

    def get_translation_file(self, from_lang, to_lang):
        """Retourne le chemin du fichier de traduction approprié"""
        if from_lang == 'en':
            return self.base_dir / 'english' / 'american-english_tofr.csv'
        return self.base_dir / 'french' / 'french_toen.csv'

    def get_increment_file(self, lang):
        """Retourne le chemin du fichier d'incrémentation pour la langue donnée"""
        lang_dir = 'english' if lang == 'en' else 'french'
        return self.base_dir / lang_dir / 'word_increment.csv'

    def increment_word_usage(self, word, lang):
        """Incrémente ou initialise le compteur d'utilisation d'un mot"""
        inc_file = self.get_increment_file(lang)
        
        # Créer le fichier s'il n'existe pas
        if not inc_file.exists():
            inc_file.write_text("word,count\n")
            df = pd.DataFrame(columns=['word', 'count'])
        else:
            df = pd.read_csv(inc_file)

        if word in df['word'].values:
            df.loc[df['word'] == word, 'count'] += 1
        else:
            new_row = pd.DataFrame({'word': [word], 'count': [1]})
            df = pd.concat([df, new_row], ignore_index=True)

        df.to_csv(inc_file, index=False)

    def word_exists(self, word, file_path):
        """Vérifie si un mot existe déjà dans le fichier de traduction et retourne aussi la ligne si trouvée"""
        if not file_path.exists():
            return False, None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                parts = [p.strip() for p in line.split(',')]
                if parts and parts[0] == word:
                    return True, (i, line, len(parts) == 1)
        return False, None

    def update_translation(self, word, translations, file_path):
        """Met à jour la traduction d'un mot s'il existe sans traduction"""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            parts = [p.strip() for p in line.split(',')]
            if parts and parts[0] == word and len(parts) == 1:
                lines[i] = f"{word}, {', '.join(translations)}\n"
                break

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    def append_translation(self, word, translations, file_path):
        new_count = 0
        """Ajoute de nouvelles traductions à un mot existant"""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            parts = [p.strip() for p in line.split(',')]
            if parts and parts[0] == word:
                # Garder l'ordre original et ajouter uniquement les nouvelles traductions
                existing_translations = parts[1:] if len(parts) > 1 else []
                # Convertir en list pour préserver l'ordre
                all_translations = existing_translations.copy()
                # Ajouter uniquement les nouvelles traductions
                for trans in translations:
                    if trans not in existing_translations:
                        all_translations.append(trans)
                        new_count += 1
                lines[i] = f"{word}, {', '.join(all_translations)}\n"
                break

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return new_count  # Retourne le nombre de nouvelles traductions ajoutées

    def add_translation(self, word, translations, from_lang, to_lang):
        """Ajoute une nouvelle traduction si le mot n'existe pas déjà"""
        trans_file = self.get_translation_file(from_lang, to_lang)
        
        # Créer le fichier s'il n'existe pas
        if not trans_file.exists():
            trans_file.parent.mkdir(parents=True, exist_ok=True)
            trans_file.write_text("")

        exists, info = self.word_exists(word, trans_file)
        if not exists:
            with open(trans_file, 'a', encoding='utf-8') as f:
                f.write(f"{word}, {', '.join(translations)}\n")
            self.increment_word_usage(word, from_lang)
            return "added"
        elif info is not None and len(info) > 2 and info[2]:  # Le mot existe sans traduction
            self.update_translation(word, translations, trans_file)
            return "updated"
        else:
            # Ajouter les nouvelles traductions au mot existant
            added_count = self.append_translation(word, translations, trans_file)
            return f"appended_{added_count}"

@click.command()
@click.argument('direction')
@click.argument('word')
@click.argument('translations', nargs=-1)
def trans(direction, word, translations):
    """
    Ajoute une traduction dans la base de données.
    
    DIRECTION: Direction de la traduction (enfr ou fren)
    WORD: Le mot à traduire
    TRANSLATIONS: Les traductions du mot (une ou plusieurs)
    """
    if not translations:
        click.echo("Erreur: Veuillez fournir au moins une traduction")
        return

    tm = TranslationManager()
    
    if direction == 'enfr':
        from_lang, to_lang = 'en', 'fr'
    elif direction == 'fren':
        from_lang, to_lang = 'fr', 'en'
    else:
        click.echo("Erreur: Direction invalide. Utilisez 'enfr' ou 'fren'")
        return

    result = tm.add_translation(word, translations, from_lang, to_lang)
    if result == "added":
        click.echo(f"Traduction ajoutée pour '{word}'")
    elif result == "updated":
        click.echo(f"Traduction mise à jour pour '{word}'")
    elif result.startswith("appended_"):
        added_count = int(result.split("_")[1])
        click.echo(f"{added_count} nouvelle(s) traduction(s) ajoutée(s) pour '{word}'")
    else:
        click.echo(f"Le mot '{word}' existe déjà avec des traductions dans la base de données")

if __name__ == '__main__':
    trans()
