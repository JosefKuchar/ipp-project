<?php

require_once 'Re.php';
require_once 'StatusCode.php';

/**
 * Argument types
 */
enum Argument
{
    case Variable;
    case Symbol;
    case Label;
    case Type;
}

/**
 * All instructions and their arguments
 */
const INSTRUCTIONS = [
    'MOVE' => [Argument::Variable, Argument::Symbol],
    'CREATEFRAME' => [],
    'PUSHFRAME' => [],
    'POPFRAME' => [],
    'DEFVAR' => [Argument::Variable],
    'CALL' => [Argument::Label],
    'RETURN' => [],
    'PUSHS' => [Argument::Symbol],
    'POPS' => [Argument::Variable],
    'ADD' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'SUB' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'MUL' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'IDIV' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'LT' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'GT' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'EQ' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'AND' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'OR' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'NOT' => [Argument::Variable, Argument::Symbol],
    'INT2CHAR' => [Argument::Variable, Argument::Symbol],
    'STRI2INT' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'READ' => [Argument::Variable, Argument::Type],
    'WRITE' => [Argument::Symbol],
    'CONCAT' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'STRLEN' => [Argument::Variable, Argument::Symbol],
    'GETCHAR' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'SETCHAR' => [Argument::Variable, Argument::Symbol, Argument::Symbol],
    'TYPE' => [Argument::Variable, Argument::Symbol],
    'LABEL' => [Argument::Label],
    'JUMP' => [Argument::Label],
    'JUMPIFEQ' => [Argument::Label, Argument::Symbol, Argument::Symbol],
    'JUMPIFNEQ' => [Argument::Label, Argument::Symbol, Argument::Symbol],
    'EXIT' => [Argument::Symbol],
    'DPRINT' => [Argument::Symbol],
    'BREAK' => []
];

$options = [
    'help',
    'stats:',
    'loc',
    'comments',
    'labels',
    'jumps',
    'fwjumps',
    'backjumps',
    'badjumps',
    'frequent',
    'print:',
    'eol',
];

$args = getopt('', $options);

if (isset($args['help'])) {
    //TODO: You can't combine with other params

    //TODO: Help text
    echo "TODO\n";
    exit(StatusCode::Ok->get());
}

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
    $line = preg_split(Re::SPACE_RE, $line);
    return $line;
}, $input);
// Remove empty lines
$input = array_filter($input, function ($line) {
    return $line[0] !== "";
});
// Reindex array
$input = array_values($input);

$output = new SimpleXMLElement('<program language="IPPcode23"></program>');

foreach ($input as $key => $line) {
    // Check header
    if ($key === 0) {
        if ($line[0] !== '.IPPcode23' && $line[0] !== '.IPPcode22') { // TODO: Remove 22 once examples are fixed
            exit(StatusCode::MissingHeader->get());
        }
        continue;
    }
    // Convert to upper case
    $line[0] = strtoupper($line[0]);

    // Check if instruction exists
    if (!array_key_exists($line[0], INSTRUCTIONS)) {
        fwrite(STDERR, "Invalid instruction: $line[0]\n");
        exit(StatusCode::InvalidInstruction->get());
    }

    // Check if instruction has correct number of arguments
    if (count($line) - 1 !== count(INSTRUCTIONS[$line[0]])) {
        fwrite(STDERR, "Invalid number of arguments for instruction: $line[0]\n");
        exit(StatusCode::LexicalSyntaxError->get());
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
        $argumentEl[0] = $arg;

        switch ($instruction[$key - 1]) {
            case Argument::Variable:
                if (!preg_match(Re::VAR_RE, $arg, $matches)) {
                    fwrite(STDERR, "Invalid variable: $arg\n");
                    exit(StatusCode::LexicalSyntaxError->get());
                }
                $argumentEl->addAttribute('type', 'var');
                break;
            case Argument::Symbol:
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
                    fwrite(STDERR, "Invalid symbol: $arg\n");
                    exit(StatusCode::LexicalSyntaxError->get());
                }
                break;
            case Argument::Label:
                if (!preg_match(Re::LABEL_RE, $arg, $matches)) {
                    fwrite(STDERR, "Invalid label: $arg\n");
                    exit(StatusCode::LexicalSyntaxError->get());
                }
                $argumentEl->addAttribute('type', 'label');
                break;
            case Argument::Type:
                if (preg_match(Re::TYPE_RE, $arg, $matches)) {
                    $argumentEl->addAttribute('type', 'type');
                } else {
                    fwrite(STDERR, "Invalid type: $arg\n");
                    exit(StatusCode::LexicalSyntaxError->get());
                }
                break;
        }
        // First match group is our value
        $argumentEl[0] = $matches[1];
    }
}

echo $output->asXML();
