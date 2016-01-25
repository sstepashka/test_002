#!/usr/bin/env python
# -*- coding: utf-8 -*-

class EvalException(Exception):
    def __init__(self):
        super(EvalException, self).__init__()


def is_operation_token(token):
    return token in ['+', '-', '*', '/']

def is_const_token(token):
    return token.isdigit()

class Cell(object):
    def __init__(self):
        super(Cell, self).__init__()

    def eval(self, sheet):
        pass

class EmptyCell(Cell):
    def eval(self, sheet):
        return '\"\"'

class ErrorCell(object):
    def __init__(self, error):
        super(ErrorCell, self).__init__()
        self.error = error

    def eval(self, sheet):
        return self.error
        
class ConstCell(Cell):
    def __init__(self, value):
        super(ConstCell, self).__init__()
        self.value = value

    def eval(self, sheet):
        return str(self.value)

class StringCell(Cell):
    def __init__(self, string):
        super(StringCell, self).__init__()
        self.string = string

    def eval(self, sheet):
        return self.string

# for calculation value of expression used default python eval function
# This can be replaced for convert to "reverse polish notation"

# eval method recursively call reference values, 
# should be replace for stack or another algorithm for large tables

# for optiomization can be used cache of evaluated value
     
class ExpressionCell(Cell):
    def __init__(self, expression):
        super(ExpressionCell, self).__init__()
        self.expression = expression

    def _value_for_token(self, token, sheet):
        if is_operation_token(token) or is_const_token(token):
            return str(token)
        else:
            cell = sheet.get(token.lower(), None)
            if cell is None:
                raise EvalException()
            else:
                if isinstance(cell, ConstCell) or isinstance(cell, ExpressionCell):
                    return cell.eval(sheet)
                else:
                    raise EvalException()

    def get_references(self):
        return [token for token in self.expression if not (is_operation_token(token) or is_const_token(token))]

    def eval(self, sheet):
        try:
            valid_tokens = map(lambda x: self._value_for_token(x, sheet), self.expression)
            return str(eval(''.join(valid_tokens)))
        except Exception:
            return "#EVAL"









