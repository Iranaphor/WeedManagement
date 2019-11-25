%{
2. TASK ON MARKOV MODELS For the following task, select and critically
appraise the most relevant technique(s) to solve the problem, justify your
choice and explain in the report the different steps taken to develop the
requested software. This will be used by the marker to check
inconsistencies or unclear points about the software. 

The source code must
be included as plain text (no images) in an appendix at the end of the
report. 

Task:
    Heater = <ON, OFF>
    Temperature = <Hot, Warm, Cold>;

        P(StateX |  StateX) = 0.7
        P(StateX | ¬StateX) = 0.3

        State ON/OFF:
            P(Hot|ON) = 0.4
            P(Warm|ON) = 0.4
            P(Cold|ON) = 0.2
    
            P(Hot|OFF) = 0.1
            P(Warm|OFF) = 0.45
            P(Cold|OFF) = 0.45

a) Implement and explain in the report a software application that, given 
in input any sequence of the above temperatures (i.e. the sequence can have 
any length), returns the probability of observing such sequence. 
Without any prior information, you can assume the initial states of the 
system to be equiprobable.

b) In the report, explain how you formalized the problem, with the aid of 
diagrams and tables, and describe step-by-step the operations and the 
numerical results of your software to compute the probability of observing 
the sequence Cold-Warm-Hot-Warm-Cold.

%}

clc
[liklihood, hidden_var_seq] = Calculate_Liklihood(["COLD","WARM","HOT","WARM","COLD"]);

disp("Liklihood of observing sequence e(1:t): " + liklihood)
disp("Sequence: "), disp(hidden_var_seq);

function [seq_liklihood,L] = Calculate_Liklihood(SEQUENCE)
    %% Convert [HOT, WARM, COLD] to usable sequence of [1,2,3]
    u = ones(length(SEQUENCE),1);
    SEQ_ID = ["HOT","WARM","COLD"];
    for i=1:length(SEQ_ID)
        u(SEQUENCE == SEQ_ID(i))=i;
    end
 
    %% Define Emission/Sensor Model
    P_TEMP_ON = [.4,.4,.2];
    P_TEMP_OFF = [.1,.45,.45];
    P_T_S = [P_TEMP_ON;P_TEMP_OFF];
    T_T_S = table(P_T_S(:,1), P_T_S(:,2), P_T_S(:,3),...
                  'VariableNames', SEQ_ID, 'RowNames', ["ON","OFF"]);
    disp(T_T_S);
    
    %% Define Transition Model
    P_NO_CHANGE = eye(2)*.7;
    P_STATECHANGE = (~eye(2))*.3;
    P_O_O = P_NO_CHANGE + P_STATECHANGE;
    T_O_O = table(P_O_O(:,1), P_O_O(:,2),...
                  'VariableNames', ["ON","OFF"], 'RowNames', ["ON","OFF"]);
    disp(T_O_O);
    
    %% Repeat through Timestep
    w = nan(2,length(u)+1);
    w(:,1)=[0.5;0.5];
    L = w;
    for t=2:length(w)
        
        %Calculate Hidden Variable Probabilities (INDEPENDENT HIDDEN STATES)
        A = P_T_S(1,u(t-1)) * (P_O_O(1, 1)*w(1,t-1) +  P_O_O(1,2)*w(2,t-1));
        B = P_T_S(2,u(t-1)) * (P_O_O(2, 1)*w(1,t-1) +  P_O_O(2,2)*w(2,t-1));
        AB = A+B; A = A*(1/AB); B = B*(1/AB); %Normalize
        w(:,t)=[A;B];
        
        %Calculate Hidden Variable Probabilities (LIKLIHOOD)
        a = (P_O_O(1, 1)*L(1,t-1));
        a2 =(P_O_O(1,2)*L(2,t-1))
        AL = P_T_S(1,u(t-1)) * (P_O_O(1, 1)*L(1,t-1) + P_O_O(1,2)*L(2,t-1));
        b =(P_O_O(2, 1)*L(1,t-1) + P_O_O(2,2)*L(2,t-1));
        BL = P_T_S(2,u(t-1)) * (P_O_O(2, 1)*L(1,t-1) + P_O_O(2,2)*L(2,t-1));
        L(:,t)=[AL;BL];
        
        
    end
    
    %% Liklihood Result
    seq_liklihood = sum(L(:,end));
    disp(w) 
    
 end

%%
    %{
        %Probability Calculation Breakdown
    
        a1 = P(u(i) | w(t)=1) * [ P(w(t)=1|w(t-1)=1) * P(w(t-1)=1) + P(w(t)=1|w(t-1)=0) * P(w(t-1)=0) ]
        a2 = P(u(i) | w(t)=0) * [ P(w(t)=0|w(t-1)=1) * P(w(t-1)=1) + P(w(t)=0|w(t-1)=0) * P(w(t-1)=0) ]
        
        a1 * 0.9          * [0.7 *          0.5 + 0.3 *          0.5 ]     = a1* 0.9 * 0.5= 0.818
        a1 * 0.2          * [0.3 *          0.5 + 0.7 *          0.5 ]     = a1* 0.2 * 0.5= 0.182
        
        a2 * P(u2=T|w2=R) * [P(w2=R|w1=R) * 0.818 + P(w2=R|w1=S) * 0.182 ]
        a2 * P(u2=T|w2=S) * [P(w2=S|w1=R) * 0.818 + P(w2=S|w1=S) * 0.182 ]
        
        a2 * 0.9          * [0.7 *          0.818 + 0.3          * 0.182 ] = a2*0.9*0.627=0.883
        a2 * 0.2          * [0.3 *          0.818 + 0.7          * 0.182 ] = a2*0.2*0.373=0.117
    %}

