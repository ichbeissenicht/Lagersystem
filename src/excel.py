import pandas as pd
import json
import os
from datetime import date
import lagerLib as lib

def convertToExcel():
    with open(r"C:\Users\juliu\Desktop\library.json", "r", encoding="utf-8") as f: #r"L:\AENE\ne-pm\01_EPC\60_labor\60_Lagerhaltung\Musterlager\library.json"
        daten = json.load(f)
    rows = []
    for uuid, item in daten.items():
        wafer_liste = item.get("wafer", [])
        if not wafer_liste:
            continue
        wafer_str = "\n".join(f"{w['Name']}: {w['Menge']}" for w in wafer_liste)
        sperr_flag = "x" if item.get("sperr_vermerk") else ""
        if any(uuid in liste for liste in lib.storageData.values()):
            imlager = "Ja"
        else:
            imlager = "Nein"
        gesamtstueckzahl = sum(item["Menge"] for item in lib.readUuid(uuid)["wafer"] if isinstance(item["Menge"], int))
        row = {
            "Typ": item.get("typ"),
            "Charge": item.get("charge"),
            "Wafer/Rolle": wafer_str,
            "Lager/Station": imlager,
            "Verpackungsart": item.get("verpackung"),
            "Reserviert für": item.get("reserviert"),
            "Sperrvermerk": sperr_flag,
            "Gesamtstückzahl": str(gesamtstueckzahl),
            "Durchmesser": item.get("durchmesser"),
            "Notiz": item.get("vermerk")

        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df = df.sort_values(by="Typ", key=lambda x: x.str.lower())
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    datum = date.today().isoformat()
    filename = f"Bestandsliste_{datum}.xlsx"
    filepath = os.path.join(downloads_path, filename)
    with pd.ExcelWriter(filepath, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Bestand")

        workbook = writer.book
        worksheet = writer.sheets["Bestand"]

        wrap_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            col_width = max(15, min(max_len, 50))
            if col == "Sperrvermerk-Nummer":
                col_width = max(col_width, 30)

            cell_format = wrap_format if col == "Wafer" else None
            worksheet.set_column(idx, idx, col_width, cell_format)


