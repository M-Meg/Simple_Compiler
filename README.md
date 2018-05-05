# Simple_Compiler
Simple Compiler implementation using Python.
You can find an Input example in file test.
the output will be assembley code for SIC/XE machine.
you can find a sample output "test_output"


#Impplemented Grammar
<prog>        ::= PROGRAM <prog-name> VAR <id-list> BEGIN <stmt-list> END.
<prog-name>   ::= id
<id-list>     ::= id | <id-list>, id
<stmt-list>   ::= <stmt> | <stmt> ; <stmt-list> 
<stmt>        ::= <assign> | <read> | <write> | <for>
<assign>      ::= id := <exp>
<exp>         ::= <factor> + <factor> | <factor> * factor>
<factor>      ::= id | ( <exp> )
<read>        ::= READ ( <id-list> )
<write>       ::= WRITE ( <id-list> )
<for>         ::= FOR <index-exp> DO <body>
<index-exp>   ::= id := <exp> to <exp>
<body>        ::= <stmt> | BEGIN <stmt-list> END
