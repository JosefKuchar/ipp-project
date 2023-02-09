<?php

/**
 * Useful regular expressions
 */
class Re
{
    public const VAR_RE = "/^[GLT]F@[_\-$\&%\*!\?a-zA-Z][_\-$\&%\*!\?a-zA-Z0-9]*$/";
    /** Label Regex */
    public const LABEL_RE = "/^[_\-$\&%\*!\?a-zA-Z][_\-$\&%\*!\?a-zA-Z0-9]*$/";
    /** Bool Regex */
    public const BOOL_RE = "/^bool@(true|false)$/";
    /** Nil Regex */
    public const NIL_RE = "/^nil@nil$/";
    /** Int Regex */
    public const INT_RE = "/^int@[-+]?[0-9]+$/"; // TODO: Octal, hex
    /** String Regex */
    public const STRING_RE = "/^string@.*$/"; // TODO: escape sequences, #, \
    /** Type Regex */
    public const TYPE_RE = "/^(int|string|bool)$/";
    /** Comment Regex */
    public const COMMENT_RE = "/#.*/";
    /** Space Regex */
    public const SPACE_RE = "/\s+/";
}
