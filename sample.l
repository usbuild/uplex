%#
hello world
%#

input = '123if'

%%

->[ ]
print 'SPACE',

->;
print 'LINEBREAK',
-><|>|>=|<=|=
print 'Compare',

->\{|\}|\[|\]|\(|\)
print 'BRACKET',

->int|float|double|char|struct
print 'TYPENAME',

->if|else|switch|case|for|while
print 'KEYWORD',

->\+|-|\*|/
print 'Operand',

->\d+
print 'DIGIT',

->[a-zA-Z_]\w*
print 'id',

->.
print 'Unknown',


%%
