%#
hello world
%#

input = 'hello%2%31.211'

%%
->[\n]
print 'newline',

->[0-9]+
print 'integer',

->[0-9]*\.[0-9]+
print 'float',

->[a-zA-Z][a-zA-Z0-9]*
print 'alpha',

->[\+\-\*\/\%]
print 'operator',

->.
print yytext,

%%

print "Hello"