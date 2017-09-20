# -*- coding: utf-8 -*-
import pandas as pd
from collections import defaultdict
from numpy import nan
from datetime import datetime
import re


class Column(object):

    """
    :param name: name of column header, e.g. 'foo'
    :param default: The value inserted if a value is absent from the
        col and values are not required.
    :param bool required: Whether or not cell may be NaN.
    :param col_type: The type to which the cell values should be
        converted.
    :param list options: A list of the allowable values.
    :param int lenght: lenght of the cell value i.e. len(value).
    :param float min_val: cell value must be >= min_val.
    :param float max_val: cell value must be <= max_val.
    :param date_format: checks or formats cells to provided strftime.
    :param regex: cell value must match regular expression.

    """

    def __init__(self, name, required=False, col_type=None, default=None,
                 options=None, lenght=None, max_val=None, min_val=None,
                 date_format=None, regex=None, replace=None):
        self.name = name
        self.required = required
        self.type = col_type
        self.default = default
        self.options = options
        self.lenght = lenght
        self.max_val = max_val
        self.min_val = min_val
        self.date_format = date_format
        self.regex = regex
        self.replace = replace

        if self.type is not None and not isinstance(self.type, type):
            raise TypeError("col_type must be instance of %s." % type)

        if self.default is not None and type(self.default) != self.type and self.type is not None:
            #raise TypeError("default type must be of type col_type (%s)." % self.type)
            print("Column %s's default value is not of type col_type (%s)." % (self.name, self.type))

        if self.options is not None and type(self.options) != list:
            raise TypeError("Options must be a list of values")

    def parse(self, col):
        """Validates column values from the df, converting according to
        the columns's type.
        """

        col_name = col.name
        col_errors = {}
        errors = defaultdict(list)

        validated_col = col.copy()

        validated_col = validated_col.astype(object)

        for i, cell in col.items():
            i = str(i) # for json

            # required
            if self.required and pd.isnull(cell):
                errors[i].append("Value is required")
                continue

            # replace
            if self.replace is not None and cell in self.replace:
                cell = self.replace[cell]

            # type
            if self.type is not None and pd.notnull(cell):
                try:
                    cell = self.type(cell)
                except:
                    errors[i].append("Value (%s) not of type %s" % (cell, self.type))
            if self.date_format is not None and pd.notnull(cell):
                try:
                    # assume in datetime
                    cell = cell.strftime(self.date_format)
                except:
                    # try converting from string
                    try:
                        datetime.strptime(cell, self.date_format)
                        # already in format
                    except:
                        errors[i].append("Incorrect date format (%s)" % self.date_format)


            if self.regex is not None and pd.notnull(cell):
                if not re.search(self.regex, str(cell)):
                    # lat ^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$
                    # long ^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$
                    errors[i].append("Value (%s) did not match regex" % cell)

            # options
            if self.options is not None and cell not in self.options and pd.notnull(cell):
                errors[i].append("Value (%s) is not one of the options" % cell)



            # lenght
            if pd.notnull(cell) and self.lenght is not None and len(str(cell)) != self.lenght:
                errors[i].append("Value is not the correct lenght (%s)" % self.lenght)

            if pd.notnull(cell) and type(cell) == int or type(cell) == float:

                if self.min_val is not None and cell < self.min_val:
                    errors[i].append("Value (%s) < min_val (%s)" % (cell, self.min_val))

                if self.max_val is not None and cell > self.max_val:
                    errors[i].append("Value (%s) > max_val (%s)" % (cell, self.max_val))

            validated_col.loc[int(i)] = cell

        if errors:
            col_errors[col_name] = errors

        if self.default is not None and not self.required:
            validated_col.fillna(self.default, inplace=True)

        return validated_col, errors


class Validator(object):
    """Validate the foramt and values of pandas df cells"""

    def __init__(self, column_class=Column):
        self.cols = []
        self.column_class = column_class

    def add_column(self, *args, **kwargs):
        """Adds an column to be parsed.
        Accepts either a single instance of Column or arguments to be passed
        into :class:`Column`'s constructor.
        See :class:`Column`'s constructor for documentation on the
        available options.
        """

        if len(args) == 1 and isinstance(args[0], self.column_class):
            self.cols.append(args[0])
        else:
            self.cols.append(self.column_class(*args, **kwargs))

        return self

    def validate(self, data_frame):
        """
        Validates pandas data frame against columns.
        """
        errors = {}
        data_frame = data_frame.fillna(value=nan)

        col_names = [col.name for col in self.cols]
        Extra_cols = []
        for header in list(data_frame):
            if header in col_names:
                continue
            Extra_cols.append(header)
        if Extra_cols:
            errors["Extra_cols"] = Extra_cols

        Missing_cols = [col.name for col in self.cols if col.name not in list(data_frame)]
        if Missing_cols:
            errors["Missing_cols"] = Missing_cols

        Col_errors = {}
        for col in self.cols:
            if col.name in Missing_cols:
                continue
            validated_col, col_errors = col.parse(data_frame[col.name])

            if col_errors:
                Col_errors[col.name] = col_errors

            if validated_col is not None:
                # only update col if the errors wernt breaking

                data_frame[col.name] = validated_col
        if Col_errors:
            errors['Col_errors'] = Col_errors
        return data_frame, errors
