# Hat Trick

An assignment-based esolang implementing a version of call/cc.

## Table Of Contents

* [Introduction](https://github.com/wompking/hattrick/blob/main/README.md#introduction)
* [Syntax](https://github.com/wompking/hattrick/blob/main/README.md#syntax)
* [Expressions and Operators](https://github.com/wompking/hattrick/blob/main/README.md#expressions-and-operators)
* [Hat Pairs](https://github.com/wompking/hattrick/blob/main/README.md#hat-pairs)

## Introduction
Hat Trick is an assignment-based esolang implementing a version of call/cc. It's both easier *and* harder to code things in Hat Trick than in [Tailor](https://github.com/wompking/tailorlang), given that Hat Trick doesn't really have loops. We'll get back to that later. File extensions for Hat Trick programs are `.htrck`, and Hat Trick comments begin with `#`. Hat Trick, unlike Tailor, is not forgiving.

## Syntax
Every line of a Hat Trick program is of a specific format:

```
<expression> => <variable name>
OR
=> [<variable name A>|<variable name B>]
```

The first type of line moves values around, and the second type makes [hat pairs](https://github.com/wompking/hattrick/blob/main/README.md#hat-pairs). Hat Trick has **four data types**, being the number, the string, the boolean, and null:
```
Number: 10
Number: -10
Number: 10.5
Number: .5

String: "beans are cool!"
String: 'hello world'
NOT a string: "oops'
NOT a string: 'oops', i did it again'
String: 'yay,\' fixed now'

Boolean: True
Boolean: False

Null:
#yes there's literally just nothing there
```

These can be stored inside variables, which are created when written to. Two standard variables are `stdin` and `stdout`, which should be self-explanatory.

Lines of code in Hat Trick that follow the first format are for computing/copying things. A very simple cat progam would be:

`stdin => stdout`

because the first half of the line is evaluated, taking input from the user, and then the value is pushed to the second half of the line, outputting the value.

## Expressions and Operators

The first half of an "assignment" command in Hat Trick is the expression; it takes in variable names and values, and evaluates it based on RPN arithmetic. For example:

`3 2 + => stdout`

would print `5` to console. Writing

`"Returning with: " stdin "" coerce + => stdout`

would print `Returning with: ` and then whatever you input the program.

The following is a table of operators in Hat Trick. Any operator will error if called on null.

| Operator | Arity | Function |
|----------|-------|----------|
| `+` | 2 | Performs addition between numbers, concatenation between strings, and logical `A OR B` between booleans. |
| `-` | 2 | Performs subtraction between numbers, is undefined for strings, and logical `A OR NOT B` between booleans. |
| `*` | 2 | Performs multiplication between numbers, is undefined for strings, and logical `A AND B` between booleans. Additionally, `string number *` returns `string` repeated `number` times, like in Python. |
| `/` | 2 | Performs divison between numbers, and is undefined otherwise. If hitting `0/0` or `val/0` respectively (where `val` is nonzero), the outputs will be `"INDETERMINATE"` and `"UNDEFINED"` respectively. |
| `abs` | 1 | Absolute value of numbers. Undefined otherwise. |
| `%` | 2 | Performs modulus between numbers, and is undefined otherwise. |
| `^` | 2 | Performs exponentiation between numbers, is undefined for strings, and logical `A XOR B` between booleans. |
| `?` | 3 | `A if C else B`. The last argument *must* be a boolean, and otherwise is unrestricted. |
| `<`, `>`, `<=`, `>=` | 2 | Performs magnitude comparison. Outputs a boolean, takes in numbers, undefined otherwise. |
| `==`, `!=` | 2 | Checks for equality and inequality; for more details, use the Python definition. |
| `!` | 1 | Logical `NOT` on booleans. Undefined otherwise. |
| `coerce` | 2 | Coerces the type of `A` to the type of `B`; this includes evaluating numbers, checking if a value is truthy/falsy, and getting string representations. |
| `find` | 2 | Python `A.find(B)` for strings, undefined otherwise. |
| `slice` | 3 | Python `C[A:B]` for strings, undefined otherwise. |

## Hat Pairs
Hat pairs are the defining feature of Hat Trick; they allow for time travel and loops. The syntax to create a hat pair is:

```
=> [<entrance hat name>|<exit hat name>]
```

When a value is read from the exit hat, the Hat Trick interpreter stores its internal state at that moment. When a value is then written to the entrance hat, the interpreter checks if the value most recently retrieved from the exit hat was the same as the value written to the entrance hat. If so, execution continues as normal. If not, the program rewinds back to the time the exit hat was read from, changes the value read from the exit hat to whatever was put in the entrance hat, and continues from there. For example:

```
=> [ent|ext]
2 => ext
ext => stdout
3 => ent
```

would print `2`, and then `3`.

Writing to the exit of a hat pair works as expected; the value inside the exit simply changes. When a value is read from the exit hat without anything being put into the entrance hat, null is produced.

