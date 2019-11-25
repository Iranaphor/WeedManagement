
%{
    TODO: Add Description for inputs for class
%}

classdef BAYESIAN_NETWORK < handle
    properties
        net
        bnid
        bnnames
    end
    methods
        
        %Default Consutructor
        function bn = BAYESIAN_NETWORK(network_structure)
            
            %Create nodes
            bn.net=[];
            bn.bnid = network_structure(:,1);
            bn.bnnames = network_structure(:,2);
            
            for i=1:length(network_structure)
                bn.net = [bn.net, NODE('ID', network_structure(i,1), ...
                                       'Name', network_structure(i,2), ...
                                       'Parents', network_structure(i,3))];
            end
        
            %Add CPT Data if available
            if size(network_structure,2)>3
                for i=1:length(network_structure)
                    bn.net(i).CPT = cell2mat(network_structure(i,4));
                end
            end
            
        end
        
        %Populate CPT from Data
        function LOAD_CPT(bn, filepath)
            
            % Load CPT Data
            Tbl = readtable(filepath);
            names = Tbl.Properties.VariableNames;
            data = csvread(filepath,1);
            
            %Format dataset headings
            labels = [];
            for i = 1:length(names')
                labels = [labels; bn.net(strcmp(names(i), bn.bnnames)).ID];
            end
            
            %For each node in network
            for i=1:length(bn.net)
                
                %Identify node's column of data
                id = find(string(labels) == string(bn.net(i).ID), 1);
                
                %Switch based on number of parents
                switch size(bn.net(i).Parents,1)
                    case 0
                        %For 0 Parents, perform: 
                        %   P(X = x) = count(x)+1 /count(X)+|X|
                        pt = (BAYESIAN_NETWORK.counter(data, id, 1)+1)...
                                                        /(length(data)+2);
                        bn.net(i).CPT = pt;
                        
                    case 1
                        %For 1 Parents, perform: 
                        %   P(X| a) = count(X, a)+1 /count( a)+|X|
                        %  &P(X|¬a) = count(X,¬a)+1 /count(¬a)+|X|
                        pid = find(string(labels) == ...
                            string(bn.net(i).Parents(1,:)), 1);
                        
                        ptt = BAYESIAN_NETWORK.CPT(data, [id, pid], [1,1]);
                        ptf = BAYESIAN_NETWORK.CPT(data, [id, pid], [1,0]);
                        bn.net(i).CPT = [ptt, ptf];
                        
                    case 2
                        %For 2 Parents, perform: 
                        %   P(X| a, b) = count(X, a, b)+1 /count( a, b)+|X|
                        %  &P(X| a,¬b) = count(X, a,¬b)+1 /count( a,¬b)+|X|
                        %  &P(X| a, b) = count(X,¬a, b)+1 /count(¬a, b)+|X|
                        %  &P(X|¬a,¬b) = count(X,¬a,¬b)+1 /count(¬a,¬b)+|X|
                        
                        p1 = find(string(labels) == ...
                                        string(bn.net(i).Parents(1,:)), 1);
                        p2 = find(string(labels) == ...
                                        string(bn.net(i).Parents(2,:)), 1);
                        pttt = BAYESIAN_NETWORK.CPT(data, [id,p1,p2], [1,1,1]);
                        pttf = BAYESIAN_NETWORK.CPT(data, [id,p1,p2], [1,1,0]);
                        ptft = BAYESIAN_NETWORK.CPT(data, [id,p1,p2], [1,0,1]);
                        ptff = BAYESIAN_NETWORK.CPT(data, [id,p1,p2], [1,0,0]);
                        bn.net(i).CPT = [pttt, pttf, ptft, ptff];
                end
            end
        end

        %UI Functions
        function plotNetwork(bn, xy)
            
            xc = 0.1;
            if xy(1)~=1
                xc = linspace(0.02,0.215,xy(1)); 
            end
            yc = flip(linspace(0.05,0.85,xy(2)));
            cc = [repelem(xc,length(yc))', repmat(yc,1,length(xc))'];
            
            networkDiag = zeros(length(bn.net));
            labels = [];
            
            %Build the digraph to plot
            for i=1:length(bn.net)
                labels = [labels, strrep(string(bn.net(i).Name), '_',' ')];
                switch size(bn.net(i).Parents,1)
                    case 1
                        pid = string(bn.net(i).Parents(1,:));
                        networkDiag(bn.bnid==pid,i)=1;

                    case 2
                        pid_1 = string(bn.net(i)  .Parents(1,:));
                        pid_2 = string(bn.net(i).Parents(2,:));
                        networkDiag(bn.bnid==pid_1,i)=1;
                        networkDiag(bn.bnid==pid_2,i)=1;
                end
            end

            %Plot Digraph
            subplot(1,3,[2,3])
            plot(digraph(networkDiag,string(labels)'), 'layout', 'auto');
            
            %For each node, plot its CPT
            for i=1:length(bn.net)
                BAYESIAN_NETWORK.plottable([cc(i,:), 0.5 0.1243], bn.net, i)
            end

        end
        
        %Calculate Inferred Probability
        function p = INFER(bn, X_label, e, e_labels, type, sample_count)
            
            switch type
                case 'enumeration'
                    p = INFERENCE.enumeration(bn.net, X_label, e, e_labels);
                case 'elimination'
                    p = INFERENCE.emlimination(bn.net, X_label, e, e_labels);
                case 'rejection'
                    p = INFERENCE.rejection(bn.net, X_label, e, e_labels, sample_count);
                case 'likelihood'
                    p = INFERENCE.likelihood(bn.net, X_label, e, e_labels, sample_count);
                case 'gibbs'
                    p = INFERENCE.gibbs(bn.net, X_label, e, e_labels);
            end
            
        end
        
    end
    methods(Static)
        
        %Perform CPT Calculation of sequence across rows
        function [ret] = CPT(data, rows, sequence)
            c1 = BAYESIAN_NETWORK.counter(data, rows, sequence);
            c2 = BAYESIAN_NETWORK.counter(data, rows(2:end), sequence(2:end));
            ret = (c1+1)/(c2+2);

        end
        %Count total number of occurances of sequence across rows
        function [ret] = counter(data, rows, sequence)

            data2 = data(:, rows);
            ret = sum(ismember(data2, sequence, 'rows'));

        end
        
        %Plot CPT Data and Network Graph (only compatible with LUCAS0 input Data)
        function [] = plottable(pltpos, net, i)
%             try
                parentsCount = size(net(i).Parents,1);
                PC = net(i).CPT';

                %Format table based on total number of parents.
                if parentsCount==0
                    id = net(i).ID;
                    PT = {['P(',id,')']};
                    try
                        T = table(PC,'VariableNames', PT);
                    catch
                        T = table(PC,'VariableNames', matlab.lang.makeValidName(PT));
                    end
                elseif parentsCount==1
                    id = net(i).ID;
                    p1 = net(i).Parents(1,:);
                    PT = ['P(',id,'|',p1,')'];
                    PA = ['T';'F'];
                    try
                        T = table(PA,PC,'VariableNames', {p1, PT});
                    catch
                        T = table(PA,PC,'VariableNames', {p1, matlab.lang.makeValidName(PT)});
                    end

                elseif parentsCount==2
                    id = net(i).ID;
                    p1 = net(i).Parents(1,:);
                    p2 = net(i).Parents(2,:);
                    PT = ['P(',id,'|',p1,',',p2,')'];
                    PA = ['T';'T';'F';'F'];
                    PB = ['T';'F';'T';'F'];
                    try
                        T = table(PA,PB,PC,'VariableNames', {p1, p2, PT});
                    catch
                        T = table(PA,PB,PC,'VariableNames', {p1, p2, matlab.lang.makeValidName(PT)});
                    end
                end
            
                %Format and plot table as annotation
                TString = evalc('disp(T)');
                TString = strrep(TString,'<strong>','\bf');
                TString = strrep(TString,'</strong>','\rm');
                TString = strrep(TString,'_','\_');
                newlines = find(TString'+0==10);
                TString(newlines(length(newlines)-1:end))=[];
                TString(newlines(1):newlines(2))=[];
                FixedWidth = get(0,'FixedWidthFontName');
                annotation(gcf,'Textbox','String',TString,...
                                'FontName', FixedWidth, 'FontSize', 10,...
                                'Units','Normalized','Position',pltpos, 'EdgeColor', 'none');
%             catch e
%                 disp(e)
%                 disp("Matlab Version Incompatible; Plotting available in R2019b or later.")
%             end
        end
        
        
        
    end
end