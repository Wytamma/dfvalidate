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
validated_sheet, errors = validator.validate(df)

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
validated_sheet, errors = validator.validate(df)
```
