clear; clc; close all; 

%% LUCAS0 Problem
input_LUCAS0 = {   
%             Root Nodes
            'AN', 'Anxiety', [];
            'PP', 'Peer_Pressure', [];
            'BE', 'Born_an_Even_Day', [];
            'GE', 'Genetics', [];
            'AL', 'Allergy', [];
%             Layer 1 Nodes
            'SM', 'Smoking', ['AN';'PP'];
            'AD', 'Attention_Disorder', ['GE'];
%             Layer 2 Nodes
            'YF', 'Yellow_Fingers', ['SM'];
            'LC', 'Lung_cancer', ['SM';'GE'];
%             Layer 3 Nodes
            'CO', 'Coughing', ['AL';'LC'];
%             Layer 4 Nodes
            'FA', 'Fatigue', ['CO';'LC'];
%             Layer 5 Nodes
            'CA', 'Car_Accident', ['AD';'FA'];
        }; %#ok<NBRAK>


tom = BAYESIAN_NETWORK(input_LUCAS0);
tom.LOAD_CPT('lucas0_train.csv');
tom.plotNetwork([2,6]);

tic, disp(tom.INFER('SM', [1,1], ['CO';'FA'], 'enumeration')), toc
tic, disp(tom.INFER('SM', [1,1], ['CO';'FA'], 'rejection', 100)), toc
tic, disp(tom.INFER('SM', [1,1], ['CO';'FA'], 'likelihood', 100)), toc

%% Burglary Problem
% figure
% input_burglary = {  'BU','Burglary',[],[.001];
%                     'EA','Earthquake',[],[.002];
%                     'AL','Alarm',['BU';'EA'],[.95,.94,.29,.001];
%                     'JC','John',['AL'],[.90,.05];
%                     'MC','Mary',['AL'],[.7,.01]}; %#ok<NBRAK>
%    
%                 
% tim = BAYESIAN_NETWORK(input_burglary);
% tim.plotNetwork([1,5]);
% tim.INFER('BU', [1,1], ['JC';'MC'], 'enumeration')
