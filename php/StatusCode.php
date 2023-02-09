<?php

/**
 * Exit status codes
 */
enum StatusCode: int
{
    case Ok = 0;
    case MissingParam = 10;
    case InputError = 11;
    case OutputError = 12;
    case MissingHeader = 21;
    case InvalidInstruction = 22;
    case LexicalSyntaxError = 23;
    case InternalError = 99;

    public function get(): int
    {
        return $this->value;
    }
}
