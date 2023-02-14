<?php

/**
 * IPPcode23 parser
 *
 * @author Josef Kuchař <xkucha28@stud.fit.vutbr.cz>
 */

// Show errors on stderr
ini_set('display_errors', 'stderr');

/**
 * Arg types
 */
enum Arg {
    case Variable;
    case Symbol;
    case Label;
    case Type;
}

/**
 * Useful regular expressions
 * Value is in match group
 */
class Re {
    /** Variable Regex */
    public const VAR_RE = "/^([GLT]F@[_\-$\&%\*!\?a-zA-Z][_\-$\&%\*!\?a-zA-Z0-9]*)$/";
    /** Label Regex */
    public const LABEL_RE = "/^([_\-$\&%\*!\?a-zA-Z][_\-$\&%\*!\?a-zA-Z0-9]*)$/";
    /** Bool Regex */
    public const BOOL_RE = "/^bool@(true|false)$/";
    /** Nil Regex */
    public const NIL_RE = "/^nil@(nil)$/";
    /** Int Regex - created from PHP documentation https://www.php.net/manual/en/language.types.integer.php */
    public const INT_RE = "/^int@([+-]?(?:[1-9][0-9]*(_[0-9]+)*|0)|(?:0[xX][0-9a-fA-F]+(_[0-9a-fA-F]+)*)|(?:0[oO]?[0-7]+(_[0-7]+)*))$/";
    /** String Regex */
    public const STRING_RE = "/^string@((?:(?:\\\\\d{3})|[^\\\\])*)$/";
    /** Type Regex */
    public const TYPE_RE = "/^(int|string|bool)$/";
    /** Comment Regex */
    public const COMMENT_RE = "/#.*/";
    /** Space Regex */
    public const SPACE_RE = "/\s+/";
}

/**
 * Exit status codes
 */
enum StatusCode: int {
    case Ok = 0;
    case MissingHeader = 21;
    case InvalidInstruction = 22;
    case LexicalSyntaxError = 23;

    public function get(): int {
        return $this->value;
    }
}

/**
 * Exit with message and status code
 */
function exit_msg(string $msg, StatusCode $code) {
    fwrite(STDERR, "$msg\n");
    exit($code->get());
}

/**
 * All instructions and their arguments
 */
const INSTRUCTIONS = [
    'MOVE' => [Arg::Variable, Arg::Symbol],
    'CREATEFRAME' => [],
    'PUSHFRAME' => [],
    'POPFRAME' => [],
    'DEFVAR' => [Arg::Variable],
    'CALL' => [Arg::Label],
    'RETURN' => [],
    'PUSHS' => [Arg::Symbol],
    'POPS' => [Arg::Variable],
    'ADD' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'SUB' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'MUL' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'IDIV' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'LT' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'GT' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'EQ' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'AND' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'OR' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'NOT' => [Arg::Variable, Arg::Symbol],
    'INT2CHAR' => [Arg::Variable, Arg::Symbol],
    'STRI2INT' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'READ' => [Arg::Variable, Arg::Type],
    'WRITE' => [Arg::Symbol],
    'CONCAT' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'STRLEN' => [Arg::Variable, Arg::Symbol],
    'GETCHAR' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'SETCHAR' => [Arg::Variable, Arg::Symbol, Arg::Symbol],
    'TYPE' => [Arg::Variable, Arg::Symbol],
    'LABEL' => [Arg::Label],
    'JUMP' => [Arg::Label],
    'JUMPIFEQ' => [Arg::Label, Arg::Symbol, Arg::Symbol],
    'JUMPIFNEQ' => [Arg::Label, Arg::Symbol, Arg::Symbol],
    'EXIT' => [Arg::Symbol],
    'DPRINT' => [Arg::Symbol],
    'BREAK' => []
];

// Parse args with getopt
$args = getopt('', ['help']);

// Output help message and exit
if (isset($args['help'])) {
    echo "Accepts IPPcode23 on standard input and outputs XML representation on standard output\n\n";
    echo "usage: parse.php [--help] < SOURCE\n\n";
    echo "options:\n";
    echo "\t--help\tshow this help message and exit\n";
    exit(StatusCode::Ok->get());
}

// Load whole stdin into string
$input = file_get_contents('php://stdin', 'r');
// Split by newlines, supports both LF and CR-LF line endings
$input = preg_split("/\r\n|\n/", $input);
// Transform to array of arrays
$input = array_map(function ($line) {
    // Remove comments
    $line = preg_replace(Re::COMMENT_RE, '', $line);
    // Remove leading and trailing whitespace
    $line = trim($line);
    // Split to parts by whitespace
    return preg_split(Re::SPACE_RE, $line);
}, $input);
// Remove empty lines
$input = array_filter($input, fn ($line) => $line[0] !== "");
// Reindex array
$input = array_values($input);

// Initiate XML generation
$output = new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8"?><program language="IPPcode23"/>');

// Check header
if (count($input) === 0 || strtolower($input[0][0]) !== '.ippcode23') {
    exit_msg("Invalid header", StatusCode::MissingHeader);
}
unset($input[0]);

// Iterate over all lines
foreach ($input as $key => $line) {
    // Convert to upper case
    $line[0] = strtoupper($line[0]);

    // Check if instruction exists
    if (!array_key_exists($line[0], INSTRUCTIONS)) {
        exit_msg("Invalid instruction: $line[0]", StatusCode::InvalidInstruction);
    }

    // Check if instruction has correct number of arguments
    if (count($line) - 1 !== count(INSTRUCTIONS[$line[0]])) {
        exit_msg("Invalid number of arguments", StatusCode::LexicalSyntaxError);
    }

    // Craft XML
    $instructionEl = $output->addChild('instruction');
    $instructionEl->addAttribute('order', $key);
    $instructionEl->addAttribute('opcode', $line[0]);

    $instruction = INSTRUCTIONS[$line[0]];
    // So we don't have to deal with 0 index
    unset($line[0]);

    // Check and generate arguments
    foreach ($line as $key => $arg) {
        $argumentEl = $instructionEl->addChild("arg$key");
        // Find and check argument type with regex
        switch ($instruction[$key - 1]) {
            case Arg::Variable:
                if (!preg_match(Re::VAR_RE, $arg, $matches)) {
                    exit_msg("Invalid variable: $arg", StatusCode::LexicalSyntaxError);
                }
                $argumentEl->addAttribute('type', 'var');
                break;
            case Arg::Symbol:
                if (preg_match(Re::VAR_RE, $arg, $matches)) {
                    $argumentEl->addAttribute('type', 'var');
                } elseif (preg_match(Re::BOOL_RE, $arg, $matches)) {
                    $argumentEl->addAttribute('type', 'bool');
                } elseif (preg_match(Re::NIL_RE, $arg, $matches)) {
                    $argumentEl->addAttribute('type', 'nil');
                } elseif (preg_match(Re::INT_RE, $arg, $matches)) {
                    $argumentEl->addAttribute('type', 'int');
                } elseif (preg_match(Re::STRING_RE, $arg, $matches)) {
                    $argumentEl->addAttribute('type', 'string');
                } else {
                    exit_msg("Invalid symbol: $arg", StatusCode::LexicalSyntaxError);
                }
                break;
            case Arg::Label:
                if (!preg_match(Re::LABEL_RE, $arg, $matches)) {
                    exit_msg("Invalid label: $arg", StatusCode::LexicalSyntaxError);
                }
                $argumentEl->addAttribute('type', 'label');
                break;
            case Arg::Type:
                if (preg_match(Re::TYPE_RE, $arg, $matches)) {
                    $argumentEl->addAttribute('type', 'type');
                } else {
                    exit_msg("Invalid type: $arg", StatusCode::LexicalSyntaxError);
                }
                break;
        }
        // First match group is our value
        $argumentEl[0] = $matches[1];
    }
}

// Output final XML
echo $output->asXML();
