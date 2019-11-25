clear; clc; close all;

treeplot(p)
treeplot(p,nodeSpec,edgeSpec)

https://uk.mathworks.com/help/matlab/ref/treeplot.html


%{
clear; 
t = uitree(); 
  
n1 = uitreenode(t, 'Text', 'n1');
n11 = uitreenode(n1, 'Text', 'n11');

n2 = uitreenode(t, 'Text', 'n2');
%}

