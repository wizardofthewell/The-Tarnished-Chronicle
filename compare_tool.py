import json

def find_defeated_boss():
    """
    Načte dva JSON soubory (před a po), porovná statusy bossů
    a najde ID toho, který byl poražen (změna z False na True).
    Soubory jsou očekávány v kódování UTF-16.
    """
    try:
        with open('vystup_PRED.json', 'r', encoding='utf-16') as f:
            pred_data = json.load(f)

        with open('vystup_PO.json', 'r', encoding='utf-16') as f:
            po_data = json.load(f)

        pred_statuses = pred_data.get("boss_statuses", {})
        po_statuses = po_data.get("boss_statuses", {})

        if not pred_statuses or not po_statuses:
            print("Chyba: 'boss_statuses' nebyly nalezeny v jednom nebo obou souborech.")
            return

        found_id = None
        for event_id, is_defeated_po in po_statuses.items():
            # Získáme stav z PRED, výchozí hodnota je None, pokud by klíč neexistoval
            is_defeated_pred = pred_statuses.get(event_id)
            
            # Hledáme změnu z False na True
            if is_defeated_po and is_defeated_pred is False:
                found_id = event_id
                break
        
        if found_id:
            print(f"Nalezeno ID poraženého bosse: {found_id}")
        else:
            print("Nenalezen žádný boss, který by byl poražen (změna z false na true).")

    except FileNotFoundError as e:
        print(f"Chyba: Soubor nebyl nalezen - {e.filename}")
    except json.JSONDecodeError as e:
        print(f"Chyba: Nepodařilo se dekódovat JSON. Soubor může být poškozený nebo ve špatném formátu. Chyba: {e}")
    except Exception as e:
        print(f"Došlo k neočekávané chybě: {e}")

if __name__ == "__main__":
    find_defeated_boss()