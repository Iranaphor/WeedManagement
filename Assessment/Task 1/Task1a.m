%{
Task 1A
 
Using the most appropriate AI methods and a suitable programming
language, implement a software application to solve the Rare Disease and
test problem explained during the lectures.

INPUTS:
    P( d ) : 
        prior probability of having a disease 

    P( t | d ) : 
        probability that the test is positive given the person has the 
        disease 

    P( 氟 | 查) :
        probability that the test is negative given the person does not 
        have the disease
 
WHERE:
    d: the person has the disease 
    t: the test is positive
 
TASK:
    After the values for the previous probabilities are set the program
    should calculate the rest of necessary probabilities and calculate the
    probability of having the disease given the test was positive:

OUTPUT:
    P( d | t )
    
 
You should be able to easily change the initial probability values and
run the program to get the new result.
---------------------------------------------------------------------------
%}


%{ 
Input: 
    P(d), P(t|d), P(氟|查)

Task:
    The product rule:
    P(t|d)P(d) = P(d|t)P(t)
    
    Rearranged:
    P(t|d)P(d)/P(t) = P(d|t)

Output: 
    P(d|t)
%}

a=rare_disease(1/10000, 0.99, 0.95);
function p_d_g_t = rare_disease(p_d, p_t_g_d, p_nt_g_nd)
    disp(" Input: P(d)="+p_d+", P(t|d)="+p_t_g_d+", P(氟|查)="+p_nt_g_nd);
    digits(20);
    
%   p_d;                           %P(d)
    p_nd = 1-p_d;                  %P(查)
    
%   p_t_g_d;                       %P(t|d)
%   p_nt_g_d = 1-p_t_g_d;          %P(氟|d)
    
    p_t_g_nd = 1-p_nt_g_nd;        %P(t|查)
%   p_nt_g_nd;                     %P(氟|查)
    
    p_t = (p_t_g_d*p_d) + (p_t_g_nd*p_nd);    %P(t)
%   p_nt = 1-p_t;                             %P(氟)
    
    p_d_g_t = vpa((p_t_g_d*p_d)/p_t,15);  %P(d|t)
    symbolicOutput = vpa(p_d_g_t,15);
    
    disp("Output: P(d|t)= " + char(symbolicOutput));
    
end



