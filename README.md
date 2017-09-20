# dfvalidate Module Repository

This module can be used to validate pandas data frames

## Installation

#### From GitHub

```sh
pipenv install git+https://github.com/wytamma/dfvalidate.git#egg=dfvalidate

```

## Usage

### Basic:
```python
import dfvalidate
import pandas as pd
import json

df = pd.DataFrame({'foo':[1, 2, "three"], 'bar':["one", None, "three"]})
validator = dfvalidate.Validator()
validator.add_column('foo', col_type=int)
validator.add_column('bar', col_type=str, required=True)
validated_df, errors = validator.validate(df)

print(json.dumps(errors['Col_errors'], indent=2))

{
  "foo": {
    "2": [
      "Value (three) not of type <class 'int'>"
    ]
  },
  "bar": {
    "1": [
      "Value is required"
    ]
  }
}
```

### Advanced:
```python
df = pd.ExcelFile('Turtle_Data.xlsx').parse('Sheet1')
validator = dfvalidate.Validator()
validator.add_column('Tag Number', col_type=int, lenght=5)
validator.add_column('Species', col_type=str, options=["Wollumbinia latisternum", "Emydura macquarii krefftii"])
validator.add_column('Sex', col_type=str, options=["Male", "Female"], replace={"M":"Male", "F":"Female"})
validator.add_column('Age Class', required=True, col_type=str, options=["Adult", "Sub Adult", "Juvenile"])
validator.add_column('CCL', col_type=float, min_val=1, max_val=50)  # CCL = Curved Carapace Lenght
validator.add_column('Number of leeches', col_type=int, default=0)
validator.add_column('Date', required=True, date_format="%d/%m/%Y")
validator.add_column('Latitude', regex="^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$")
validator.add_column('Longitude', regex="^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$")
validated_df, errors = validator.validate(df)
```

### Super advanced nek level usage:

Load df and build validator

```python
import pandas as pd
import dfvalidate

df = pd.ExcelFile('Turtle_Data.xlsx').parse('Sheet1')

validator = dfvalidate.Validator()
validator.add_column('Tag Number', col_type=int, lenght=5)
validator.add_column('Species', col_type=str, options=["Wollumbinia latisternum", "Emydura macquarii krefftii"])
validator.add_column('Sex', col_type=str, options=["Male", "Female"], replace={"M":"Male", "F":"Female"})
validator.add_column('Age Class', required=True, col_type=str, options=["Adult", "Sub Adult", "Juvenile"])
validator.add_column('CCL', col_type=float, min_val=1, max_val=50)  # CCL = Curved Carapace Lenght
validator.add_column('Number of leeches', col_type=int, default=0)
validator.add_column('Date', required=True, date_format="%d/%m/%Y")
validator.add_column('Latitude', regex="^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$")
validator.add_column('Longitude', regex="^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$")
validated_df, errors = validator.validate(df)
```

Use openpyxl to save errors as comments and highlight cells.

```python
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.comments import Comment
from openpyxl.styles import PatternFill

sheet_title = "validated"

wb = openpyxl.load_workbook('Turtle_Data.xlsx')

if sheet_title in wb.sheetnames:
    ws = wb[sheet_title]
    wb.remove_sheet(ws)

ws = wb.create_sheet(title=sheet_title)

for r in dataframe_to_rows(validated_df, index=False, header=True):
    ws.append(r)

def create_col_numbers(validated_df):
    headers = list(validated_df.columns)
    col_numbers = {}
    for i, header in enumerate(headers):
        col_numbers[header] = i + 1
    return col_numbers

col_numbers = create_col_numbers(validated_df)

redFill = PatternFill(
    start_color='e74c3c',
    end_color='e74c3c',
    fill_type='solid'
)

for col in errors['Col_errors']:
    for error in errors['Col_errors'][col]:
        row = int(error) + 2 # +2 for 0 start and header
        column = col_numbers[col]
        comment = Comment(", ".join(errors['Col_errors'][col][error]), "xlValidator")
        cell = ws.cell(row=row, column=column)
        cell.comment = comment
        cell.fill = redFill

wb.save(file_name)
```
