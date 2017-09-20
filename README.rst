dfvalidate Module Repository
========================
This module can be used to validate pandas data frames
===========
**Basic usage:**
    df = pd.DataFrame({'foo':[1,2,3], 'bar':["one","two","three"]}
    checker = sheetcheck.SheetChecker()
    checker.add_column('foo', col_type=int, required=True)
    checker.add_column('bar', col_type=str)
    checked_df, errors = checker.check_sheet(df)

**Advanced usage:**
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
    checked_sheet, errors = checker.check_sheet(df)
