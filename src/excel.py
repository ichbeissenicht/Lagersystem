import pandas as pd
import json
import os
from datetime import date

def convertToExcel():

    with open(r"L:\AENE\ne-pm\01_EPC\60_labor\60_Lagerhaltung\Musterlager\library.json", "r", encoding="utf-8") as f:
        daten = json.load(f)
    rows = []
    for uuid, item in daten.items():
        wafer_liste = item.get("wafer", [])
        if not wafer_liste:
            continue
        wafer_str = "\n".join(f"{w['Name']}: {w['Menge']}" for w in wafer_liste)
        sperr_flag = "x" if item.get("sperr_vermerk") else ""

        row = {
            "Typ": item.get("typ"),
            "Charge": item.get("charge"),
            "Verpackung": item.get("verpackung"),
            "Durchmesser": item.get("durchmesser"),
            "Sperrvermerk": sperr_flag,
            "Sperrvermerk-Nummer": item.get("sperr_vermerk_nummer"),
            "Reserviert": item.get("reserviert"),
            "Vermerk": item.get("vermerk"),
            "Wafer": wafer_str
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


