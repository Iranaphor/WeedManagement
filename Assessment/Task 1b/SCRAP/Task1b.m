clc, %clf, close all
%{
Task 1b:
    Implement a software application to solve a Medical Diagnosis problem
    similar to the Burglary problem explained during the lectures. 

    The program should have as input the dataset shown in the link below, 
    and the Bayes Network structure shown in the figure below – which uses 
    the following random variables:

        LC: Lung Cancer
        SM: Smoking     
        YF: Yellow_Fingers 
        AN: Anxiety 
        PP: Peer_Pressure 
        GE: Genetics 
        AD: Attention_Disorder 
        BE: Born_an_Even_Day 
        CA: Car_Accident 
        FA: Fatigue 
        AL: Allergy 
        CO: Coughing
 
    Your program should first learn its parameters from data and then use
    inference to calculate the probability distribution of Smoking given
    Coughing and Fatigue:

P( S | C=True, F=True)

Please indicate in your report the methods used for implementing parameter
learning and probabilistic inference.

Data=LUCAS0 Train: http://www.causality.inf.ethz.ch/data/LUCAS.html 
---------------------------------------------------------------------------
%}
input_LUCAS0 = {   % Root Nodes
            'AN', 'Anxiety', [], [0.02, 0.8224];
            'PP', 'Peer_Pressure', [], [0.02, 0.6799];
            'BE', 'Born_an_Even_Day', [], [0.02, 0.5374];
            'GE', 'Genetics', [], [0.02, 0.3950];
            'AL', 'Allergy', [], [0.02, 0.2525];
            % Layer 1 Nodes
            'SM', 'Smoking', ['AN';'PP'], [0.02 0.1100];
            'AD', 'Attention_Disorder', ['GE'], [0.215, 0.8224];
            % Layer 2 Nodes
            'YF', 'Yellow_Fingers', ['SM'], [0.215, 0.6799];
            'LC', 'Lung Cancer', ['SM';'GE'], [0.215, 0.5374];
            % Layer 3 Nodes
            'CO', 'Coughing', ['AL';'LC'], [0.215, 0.3950];
            % Layer 4 Nodes
            'FA', 'Fatigue', ['CO';'LC'], [0.215, 0.2525];
            % Layer 5 Nodes
            'CA', 'Car_Accident', ['FA';'AD'], [0.215, 0.1100]; %TODO: SWAP THESE LABELS
        }; %#ok<NBRAK>


input_burglary = {   'BU','Burglary',[.001],[];
            'EA','Earthquake',[.002],[];
            'AL','Alarm',[.95,.94,.29,.001],['BU';'EA'];
            'JC','John',[.90,.05],['AL'];
            'MC','Mary',[.7,.01],['AL'];
        };

generate_network2(input_burglary)
function [] = generate_network2(input, display)
    
    display

    net=[];
    for i=1:length(input)
        net = [net, NODE('ID', input(i,1), 'Name', input(i,2), ...
                         'CPT', input(i,3), 'Parents', input(i,4))];
    end
    
    a=INFERENCE(net, 1, 'BU', [1,1], ['JC';'MC'], 'enumeration')

end
function [] = generate_network(input)
    
    % Generate Network 
    net=[];
    for i=1:length(input)
        net = [net, NODE('ID', input(i,1), 'Name', input(i,2), ...
                         'Parents', input(i,3), 'Position', input(i,4))];
    end
    
    
    % Load CPT Data
    headings = ['SM'; 'YF'; 'AN'; 'PP'; 'GE'; 'AD'; 'BE'; 'CA'; 'FA'; 'AL'; 'CO'; 'LC'];
    [net, headings, data] = generateCPT('lucas0_train.csv', net, headings);
    
    
    % Display Graph / CPT Nodes
    plotNetwork(net, data);
    
    
    % Inference
    % P( SM | CO=True, FA=True)
    %INFERENCE(bn, X, X_label, e, e_labels, type)
    INFERENCE(net, 'SM', [1,1], ['CO';'FA'], 'enumeration')
    
end

%% CPT Functions
function [net, headings, data] = generateCPT(filepath, net, headings)
    data = csvread(filepath,1);
    
    for i=1:length(net)
        
        %We must first identify the column we are looking at
        
        id = find(string(headings) == string(net(i).ID), 1);
        
        switch size(net(i).Parents,1)
            case 0 %P(X = x) = count(x)+1 /count(X)+|X|
%                 disp("CASE 0");
                pt = (counter(data, id, 1)+1)/(length(data)+2);
                net(i).CPT = pt;
                
            case 1
                clc
%                 disp("CASE 1");
                pid = find(string(headings) == string(net(i).Parents(1,:)), 1);
                %pid = getparent(headings, net, i, 1);
                
                ptt = CPT(data, [id, pid], [1,1]);
                ptf = CPT(data, [id, pid], [1,0]);
                net(i).CPT = [ptt, ptf];
                
            case 2
%                 disp("CASE 2");
                pid_1 = find(string(headings) == string(net(i).Parents(1,:)), 1);
                pid_2 = find(string(headings) == string(net(i).Parents(2,:)), 1);
                pttt = CPT(data, [id, pid_1, pid_2], [1,1,1]);
                pttf = CPT(data, [id, pid_1, pid_2], [1,1,0]);
                ptft = CPT(data, [id, pid_1, pid_2], [1,0,1]);
                ptff = CPT(data, [id, pid_1, pid_2], [1,0,0]);
                net(i).CPT = [pttt, pttf, ptft, ptff];
        end
    end
end
function [ret] = CPT(data, rows, sequence) %CPT(data, [1,3,7], [1,0,1])

    c1 = counter(data, rows, sequence);
    c2 = counter(data, rows(2:end), sequence(2:end));
    ret = (c1+1)/(c2+2); %TODO: eheck whether domainsize should be 2^length(sequence)

end
function [ret] = counter(data, rows, sequence)

    data2 = data(:, rows);
    ret = sum(ismember(data2, sequence, 'rows'));
    
end
    
    
%% UI Functions
function plotNetwork(net, data)
    networkDiag = zeros(length(net));
    labels = [];
    for i=1:length(net)
        labels = [labels, strrep(string(net(i).Name), '_',' ')];
        switch size(net(i).Parents,1)
            
            case 1
%                 disp("CASE 1");
                pid = string(net(i).Parents(1,:));
                
                for nid=1:length(net)
%                     disp(pid + " | " + net(nid).ID)
                    if net(nid).ID==pid
                        networkDiag(nid,i)=1;
                        break; 
                    end
                end
                
                labels(i) = labels(i);
                
            case 2
%                 disp("CASE 2");
                pid_1 = string(net(i).Parents(1,:));
                pid_2 = string(net(i).Parents(2,:));
                
                for nid=1:length(net)
%                     disp(pid_1 + " | " + net(nid).ID)
                    if net(nid).ID==pid_1
                        networkDiag(nid,i)=1;
                        break; 
                    end
                end
                
                for nid=1:length(net)
%                     disp(pid_2 + " | " + net(nid).ID)
                    if net(nid).ID==pid_2
                        networkDiag(nid,i)=1;
                        break; 
                    end
                end
                
        end
    end
    
    G=digraph(networkDiag);
    subplot(1,3,[2,3])
    G.Nodes.Name = string(labels)';
    plot(G, 'layout', 'auto'); %axis off;
    
    j=0;
    for i=1:length(net)
        if size(net(i).Parents,1) ~= 0
            j = j + 1; 
        end
    end
    
    
    
    for i=1:length(net)
        plottable([net(i).Position, 0.5 0.1243], net, i)
    end
    
end
function [] = plottable(pltpos, net, i)
    
    parentsCount = size(net(i).Parents,1);
    PC = net(i).CPT';
    
    if parentsCount==0
        id = net(i).ID;
        T = table(PC,'VariableNames', {['P(',id,')']});
    elseif parentsCount==1
        id = net(i).ID;
        p1 = net(i).Parents(1,:);
        PT = {p1, ['P(',id,'|',p1,')']};
        PA = ['T';'F'];
        T = table(PA,PC,'VariableNames', PT); %#ok<NASGU>
    elseif parentsCount==2
        id = net(i).ID;
        p1 = net(i).Parents(1,:);
        p2 = net(i).Parents(2,:);
        PT = {p1, p2, ['P(',id,'|',p1,',',p2,')']};
        PA = ['T';'T';'F';'F'];
        PB = ['T';'F';'T';'F'];
        T = table(PA,PB,PC,'VariableNames', PT); %#ok<NASGU>
    end
    
    % Get the table in string form.
    TString = evalc('disp(T)');

    % Use TeX Markup for bold formatting and underscores.
    TString = strrep(TString,'<strong>','\bf');
    TString = strrep(TString,'</strong>','\rm');
    TString = strrep(TString,'_','\_');
    newlines = find(TString'+0==10);
    %TString(newlines(length(newlines)))=[];
    TString(newlines(length(newlines)-1:end))=[];
    TString(newlines(1):newlines(2))=[];
    

    % Get a fixed-width font.
    FixedWidth = get(0,'FixedWidthFontName');

    % Output the table using the annotation command.
    annotation(gcf,'Textbox','String',TString,...
                    'FontName', FixedWidth, 'FontSize', 10,...
                    'Units','Normalized','Position',pltpos, 'EdgeColor', 'none');
    
end





