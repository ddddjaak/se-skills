# Spreadsheet Processing Guide for SE Documents

Techniques for extracting structured data from Excel (.xlsx/.xls) and CSV/TSV files
commonly used in SE workflows: BOMs, pin lists, register maps, electrical specs,
test matrices.

## Quick Reference

| Task | Best Tool | Notes |
|------|-----------|-------|
| Read .xlsx data (fast, all sheets) | `pandas.read_excel()` | `sheet_name=None` to read all sheets |
| Read .xlsx with formatting/merged cells | `openpyxl.load_workbook()` | `data_only=True` for calculated values |
| Read .csv | `pandas.read_csv()` or `csv` module | Specify `dtype=str` to avoid inference |
| Read .tsv | `pandas.read_csv(sep='\t')` | Tab-separated |
| Detect empty rows | `openpyxl` row iteration | Check `all(c is None for c in row)` |
| Skip header rows | `pandas.read_excel(skiprows=N)` | Use when first N rows are metadata |

## Common SE Spreadsheet Types

### BOM (Bill of Materials)

```
Typical columns: Item, Qty, Part Number, Description, Value, Footprint, Voltage Rating, Manufacturer, MPN
```

Key extraction concerns:
- Merged cells in "Item" column (grouped by subsystem)
- Alternate parts (multiple MPNs per line)
- DNI (Do Not Install) components → flag as conditional
- Thermal/voltage derating notes in separate cells

### Pin List

```
Typical columns: Pin#, Name, Type (I/O/Power/GND), Function, Alt Function, Voltage Domain, Drive Strength, Notes
```

Key extraction concerns:
- Power pins grouped by domain (VDD_CORE, VDD_IO, VDDA, etc.)
- NC (No Connect) pins → flag for PCB layout
- Pin mux table with multiple alt functions per pin (often in wide tables)

### Register Map

```
Typical columns: Offset, Register Name, Bit[7:0], Default, Access (R/W/RO), Description
```

Key extraction concerns:
- Bit-level sub-tables within a register description
- Reset values may be in hex (0x00) or binary
- Access types: RO, RW, R/W1C, WO, etc. → important for driver design

### Electrical Specifications

```
Typical columns: Parameter, Symbol, Min, Typ, Max, Unit, Conditions, Notes
```

Key extraction concerns:
- "Typ" values ≠ worst-case (design to Min/Max)
- Conditions column may reference temperature/voltage corners
- Units may vary within same sheet (mV, V, μA, mA)

### Test Matrix

```
Typical columns: Test ID, Requirement Ref, Test Description, Input, Expected Output, Pass/Fail, HW Rev, FW Version
```

Key extraction concerns:
- Requirement traceability (REQ-XXX IDs)
- HW/FW version columns → version gate for test applicability

## Reading Strategies

### Strategy 1: pandas (preferred for clean data)

```python
import pandas as pd

# Read all sheets
sheets = pd.read_excel("BOM.xlsx", sheet_name=None, dtype=str)

# Read specific sheet, skip metadata rows
df = pd.read_excel("PinList.xlsx", sheet_name="Pins", skiprows=3, dtype=str)

# Read CSV with semicolon separator (common in European exports)
df = pd.read_csv("export.csv", sep=";", dtype=str, encoding="utf-8-sig")
```

### Strategy 2: openpyxl (for complex formatting)

```python
from openpyxl import load_workbook

wb = load_workbook("datasheet.xlsx", data_only=True)
sheet = wb["Electrical Specs"]

# Iterate rows (1-indexed)
for row in sheet.iter_rows(min_row=2, values_only=True):
    param, sym, min_val, typ_val, max_val, unit = row[:6]
    # ...
```

### Strategy 3: CSV module (for minimal dependencies)

```python
import csv

with open("data.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        # process row
```

## Handling Edge Cases

### Merged Cells

openpyxl preserves merged cell info. pandas fills with NaN/empty.
Strategy: forward-fill empty cells in key columns:

```python
# Forward-fill the 'Subsystem' column (merged cells)
df['Subsystem'] = df['Subsystem'].fillna(method='ffill')
```

### Multi-line Cells

Cells containing newlines (`\n`) in pin function descriptions.
Strategy: replace with "; " separator when converting to Markdown.

### Formula Cells

Cells starting with `=` in openpyxl (without `data_only=True`).
Strategy: always use `data_only=True` to get calculated values, or skip formula cells.

### Date Inference

pandas automatically converts date-like strings to datetime.
Strategy: use `dtype=str` to prevent this, or use `parse_dates=['col']` explicitly.

### Encoding Issues

Common encodings for internationally-used spreadsheets:
- `utf-8` (default)
- `utf-8-sig` (handles BOM)
- `gbk` / `gb2312` (Chinese-sourced files)
- `latin-1` / `cp1252` (Western European)

## Output Structure

```
docs/inputs-preprocessed/<source-name>/
├── sheets/
│   ├── sheet-01-Pin_List.md       ← Each sheet as a Markdown table
│   ├── sheet-02-Electrical.md
│   └── sheet-03-Mechanical.md
└── manifest.json                  ← Sheet metadata + issues
```

### manifest.json schema

```json
{
  "source": "BOM.xlsx",
  "total_sheets": 3,
  "sheets_exported": 3,
  "total_rows": 156,
  "total_cells": 1248,
  "sheets": [
    {
      "name": "Main BOM",
      "index": 1,
      "rows": 120,
      "cols": 8,
      "has_header": true,
      "markdown_path": "sheets/sheet-01-Main_BOM.md"
    }
  ],
  "issues": [
    "Sheet 'Alternates': merged cells in column A may lose group info"
  ]
}
```

## Integration with requirements-decompose

After preprocessing, the Markdown table files feed directly into Step 2 (CLASSIFY):

| Sheet Content | Maps to Requirement Type | Example |
|--------------|------------------------|---------|
| Pin list | Interface (IF-XXX) | "Pin 42 = GPIO_12, I/O, 3.3V domain" |
| BOM | Constraint (CON-XXX) | "C37 = 10μF, X7R, 16V, 0805" |
| Register map | Functional (REQ-XXX) | "Offset 0x10: Control Register, Bit 2 = Enable ADC" |
| Electrical spec | Performance (REQ-XXX) | "V_IH(min) = 0.7 × VDDIO = 2.31V" |
| Test matrix | Verification | "TC-042 confirms REQ-018 (SPI boot timeout)" |
