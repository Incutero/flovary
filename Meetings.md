# Meeting Notes

## Meeting 3
- kai's version is a regex parser to identify functions
  * can't handle imported functions since it walks through and finds all function names first to ID
- shum's version isn't done, uses AST to identify function calls
  * long term probably want to use this since it's OO
  * confusing to use, frustrating
  * need more time to explore how AST walks through code
- next meeting is work session

## Meeting 2
- everybody write own implementation of basic walk-through
  * figure out what we each like/don't like about certain data structures
  * see what parts of code are important/not important to visualize
- parse file given start function
- textual output only
- what about conflicting function names?
- how to handle imported functions?
- we're not a compiler -- python being JIT


## Meeting 1
- identify codebases to test on 6.02 6.036 6.006 ?
- python files first
- produce data structure that represents functions -> calls
- each node is function
   * filename
   * class if has one
   * return type
   * params / signature
   * line #
- start nodes -> public functions
- recursion has own arrow
