%{
#include<iostream>
#include<cstdlib>
#include"yytab.h"
%}
/*正规表达式*/
digit [0-9]
letter [a-zA-Z]
id {letter}[{letter}|{digit}]*
num [1-9]{digit}*
%%
break       {return BREAK; }
case        {return CASE; }
char        {return CHAR;}
const       {return CONST; }
continue    {return CONTINUE; }
default     {return DEFAULT; }
do          {return DO; }
double      {return DOUBLE; }
else        {return ELSE; }
enum        {return ENUM; }
float       {return FLOAT; }
for         {return FOR; }
goto        {return GOTO; }
if          {return IF; }
int         {return INT; }
long        {return LONG; }
return      {return RETURN; }
short       {return SHORT; }
signed      {return SIGNED; }
sizeof      {return SIZEOF; }
static      {return STATIC; }
switch      {return SWITCH; }
typedef     {return TYPEDEF; }
unsigned    {return UNSIGNED; }
void        {return VOID; }
while       {return WHILE; }
{num}       {return NUMBER;}
{id}        {return IDENTIFIER;}
+=		    {return ADD_ASSIGN; }
-=			{return SUB_ASSIGN; }
*=			{return MUL_ASSIGN; }
/=			{return DIV_ASSIGN; }
++			{return INC_OP; }
--			{return DEC_OP; }
->			{return PTR_OP; }
&&			{return AND_OP; }
\|\|		{return OR_OP; }
<=			{return LE_OP; }
>=			{return GE_OP; }
==			{return EQ_OP; }
!=			{return NE_OP; }
;			{return ';'; }
,	        {return ','; }
:			{return ':'; }
=			{return '='; }
.		    {return '.'; }
&			{return '&'; }
!			{return '!'; }
-			{return '-'; }
+			{return '+'; }
/			{return '/'; }
<		    {return '<'; }
>			{return '>'; }
?			{return '?'; }
{		    {return '{'; }
}		    {return '}'; }
\[          {return '['; }
\]          {return ']'; }
\*          {return '*'; }
%%
void main()
{
	char *A[60]={"break","case","char","const","continue","default","do",
	          "double","else","enum","float","for","goto","if","int",
	          "long","return","short","signed","sizeof","static",
	          "switch","typedef","unsigned","void","while","egad","3435","045",
	          "4df","+=","-=","*=","/=","++","--","->","||","<=",">=","==","!=",
			  ";",",",":","=",".","&","!","-","+","/","<",">","?","{","}","[","]","*"};
	for(int i=0;i<60;i++)
	{
		cout<<analysis(A[i],strlen(A[i]))<<endl;
	}

}
