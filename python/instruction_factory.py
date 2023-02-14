"""Instruction module"""
from error import StatusCode, exit_program
import instructions

def InstructionFactory(xml, runner):
    """Instruction factory"""
    classes = {
        "MOVE": instructions.Move,
        "CREATEFRAME": instructions.CreateFrame,
        "PUSHFRAME": instructions.PushFrame,
        "POPFRAME": instructions.PopFrame,
        "DEFVAR": instructions.DefVar,
        "CALL": instructions.Call,
        "RETURN": instructions.Return,
        "PUSHS": instructions.PushS,
        "POPS": instructions.PopS,
        "ADD": instructions.Add,
        "SUB": instructions.Sub,
        "MUL": instructions.Mul,
        "IDIV": instructions.IDiv,
        "LT": instructions.Lt,
        "GT": instructions.Gt,
        "EQ": instructions.Eq,
        "AND": instructions.And,
        "OR": instructions.Or,
        "NOT": instructions.Not,
        "INT2CHAR": instructions.Int2Char,
        "STRI2INT": instructions.Stri2Int,
        "READ": instructions.Read,
        "WRITE": instructions.Write,
        "CONCAT": instructions.Concat,
        "STRLEN": instructions.StrLen,
        "GETCHAR": instructions.GetChar,
        "SETCHAR": instructions.SetChar,
        "TYPE": instructions.Type,
        "LABEL": instructions.Label,
        "JUMP": instructions.Jump,
        "JUMPIFEQ": instructions.JumpIfEq,
        "JUMPIFNEQ": instructions.JumpIfNeq,
        "EXIT": instructions.Exit,
        "DPRINT": instructions.DPrint,
        "BREAK": instructions.Break
    }

    # Check if opcode is valid
    if xml.attrib['opcode'] not in classes:
        exit_program(StatusCode.MALLFORMED, "Invalid opcode")

    # Return corresponding instruction instance
    return classes[xml.attrib['opcode']](xml, runner)