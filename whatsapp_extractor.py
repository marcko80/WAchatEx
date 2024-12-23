import os
import shutil
import subprocess
from datetime import datetime
import sys
import json

class WhatsAppExtractor:
    def __init__(self):
        """
        Inizializza l'estrattore di conversazioni WhatsApp con le configurazioni di base
        """
        self.backup_path = "/sdcard/WhatsApp/Databases"
        self.media_path = "/sdcard/WhatsApp/Media"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"whatsapp_extraction_{self.timestamp}.log"

    def scrivi_log(self, messaggio, tipo="INFO"):
        """
        Scrive un messaggio nel file di log
        
        Args:
            messaggio (str): Il messaggio da loggare
            tipo (str): Il tipo di messaggio (INFO, ERROR, WARNING)
        """
        with open(self.log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {tipo}: {messaggio}\n")
        print(f"{tipo}: {messaggio}")

    def verifica_adb(self):
        """
        Verifica se ADB è installato e disponibile nel sistema
        
        Returns:
            bool: True se ADB è disponibile, False altrimenti
        """
        try:
            subprocess.run(['adb', 'version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.scrivi_log("ADB non trovato nel sistema. Installare Android Platform Tools.", "ERROR")
            return False

    def verifica_dispositivo_connesso(self):
        """
        Verifica se un dispositivo Android è connesso via ADB
        
        Returns:
            bool: True se un dispositivo è connesso, False altrimenti
        """
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            devices = result.stdout.strip().split('\n')[1:]
            return any(device.strip() for device in devices)
        except subprocess.CalledProcessError:
            return False

    def crea_backup_whatsapp(self, cartella_destinazione):
        """
        Crea un backup delle conversazioni WhatsApp
        
        Args:
            cartella_destinazione (str): Percorso dove salvare il backup
        
        Returns:
            bool: True se il backup è riuscito, False altrimenti
        """
        try:
            # Crea la struttura delle cartelle
            backup_dir = os.path.join(cartella_destinazione, f"WhatsApp_Backup_{self.timestamp}")
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup dei database
            db_dir = os.path.join(backup_dir, "Databases")
            os.makedirs(db_dir, exist_ok=True)
            
            # Esegue il pull del database
            subprocess.run([
                'adb', 'pull', self.backup_path, db_dir
            ], check=True)
            
            # Backup dei media
            media_dir = os.path.join(backup_dir, "Media")
            os.makedirs(media_dir, exist_ok=True)
            
            # Esegue il pull dei media
            subprocess.run([
                'adb', 'pull', self.media_path, media_dir
            ], check=True)
            
            self.scrivi_log(f"Backup completato in: {backup_dir}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.scrivi_log(f"Errore durante il backup: {str(e)}", "ERROR")
            return False
        except Exception as e:
            self.scrivi_log(f"Errore imprevisto: {str(e)}", "ERROR")
            return False

    def estrai_metadati_chat(self, backup_dir):
        """
        Estrae i metadati delle chat dal backup
        
        Args:
            backup_dir (str): Percorso della directory del backup
        """
        try:
            metadata = {
                'timestamp_backup': self.timestamp,
                'chat_folders': [],
                'media_stats': {
                    'images': 0,
                    'videos': 0,
                    'audio': 0,
                    'documents': 0
                }
            }
            
            # Analizza la struttura delle cartelle dei media
            media_dir = os.path.join(backup_dir, "Media")
            for root, dirs, files in os.walk(media_dir):
                folder_name = os.path.basename(root)
                if folder_name in ['WhatsApp Images', 'WhatsApp Video', 'WhatsApp Audio', 'WhatsApp Documents']:
                    metadata['chat_folders'].append({
                        'name': folder_name,
                        'file_count': len(files)
                    })
                    
                    # Aggiorna le statistiche
                    if 'Images' in folder_name:
                        metadata['media_stats']['images'] += len(files)
                    elif 'Video' in folder_name:
                        metadata['media_stats']['videos'] += len(files)
                    elif 'Audio' in folder_name:
                        metadata['media_stats']['audio'] += len(files)
                    elif 'Documents' in folder_name:
                        metadata['media_stats']['documents'] += len(files)
            
            # Salva i metadati in un file JSON
            metadata_file = os.path.join(backup_dir, 'backup_metadata.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=4)
            
            self.scrivi_log(f"Metadati salvati in: {metadata_file}")
            
        except Exception as e:
            self.scrivi_log(f"Errore durante l'estrazione dei metadati: {str(e)}", "ERROR")

    def mostra_guida_setup(self):
        """
        Mostra la guida per la configurazione iniziale
        """
        print("\n=== Guida alla configurazione ===")
        print("1. Connetti il telefono al computer via USB")
        print("2. Abilita il Debug USB sul telefono:")
        print("   - Vai in Impostazioni > Info sul telefono > Numero build")
        print("   - Tocca 7 volte il Numero build per abilitare le opzioni sviluppatore")
        print("   - Vai in Impostazioni > Opzioni sviluppatore")
        print("   - Attiva il Debug USB")
        print("3. Autorizza il computer sul telefono quando richiesto")
        print("4. Assicurati che WhatsApp sia installato e configurato\n")
        input("Premi INVIO quando hai completato questi passaggi...")

    def esegui_estrazione(self):
        """
        Esegue il processo completo di estrazione
        """
        self.scrivi_log("Avvio processo di estrazione WhatsApp")
        
        # Verifica requisiti
        if not self.verifica_adb():
            return
        
        self.mostra_guida_setup()
        
        if not self.verifica_dispositivo_connesso():
            self.scrivi_log("Nessun dispositivo Android connesso", "ERROR")
            return
        
        # Richiedi la cartella di destinazione
        while True:
            cartella_dest = input("\nInserisci il percorso della cartella di destinazione: ").strip()
            if os.path.exists(cartella_dest):
                break
            print("La cartella non esiste. Creala prima di continuare.")
        
        # Esegui il backup
        print("\nAvvio backup WhatsApp...")
        if self.crea_backup_whatsapp(cartella_dest):
            backup_dir = os.path.join(cartella_dest, f"WhatsApp_Backup_{self.timestamp}")
            self.estrai_metadati_chat(backup_dir)
            print("\nEstrazione completata con successo!")
            print(f"I file sono stati salvati in: {backup_dir}")
            print(f"Consulta il file di log '{self.log_file}' per i dettagli dell'operazione")
        else:
            print("\nEstrazione fallita. Controlla il file di log per i dettagli.")

def main():
    """
    Funzione principale del programma
    """
    try:
        extractor = WhatsAppExtractor()
        extractor.esegui_estrazione()
    except KeyboardInterrupt:
        print("\nOperazione interrotta dall'utente.")
    except Exception as e:
        print(f"\nErrore imprevisto: {str(e)}")
        print("Consulta il file di log per i dettagli.")

if __name__ == "__main__":
    main()
