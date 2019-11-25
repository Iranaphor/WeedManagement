%{

    TODO: ADD SECTION TO LOOP TO HANDLE WHEN THERE IS NO IMPACT FROM NODE
    ON HEIRARCHY

%}
classdef INFERENCE < handle
    
    methods(Static)
        function p=enumeration(bn, X_label, e, e_labels)

            %{
                define h as the number of hidden variables !(e,X)
                Create Binary Table (2^length(h), length(h))
                For each node in (e|X)
                    Append column with state of evidence
                    Append reference id

                For each value of X
                    For each row in table
                        Take each column
                            Find node ID
                            Find node parents
                            Find values for ID and Parents (in binarytable)

                            Find CPT probability
                            Convert to !X if applicable

                        Multiply the answers
                    Sum the answers
                Normalize the result
            %}

            %Save the input values for the probability distribution
            p.Type = "ENUMERATION";
            p.X = X_label;
            p.e = e_labels;
            p.e_val = e;
            p.Probs = ["True", "False"];
            
            %Repeat for each value of the Query
            for X_val=0:1
                bnid = [];
                for i=1:length(bn); bnid = [bnid; bn(i).ID]; end
                %Generate table of all possible combinations of hidden values
                h = length(bn)-(length(e)+length(X_val));
                L = [e_labels;X_label];
                Lv = [e,X_val];
                nL = bnid(~ismember(string(bnid), string(L)),:); %If ID is not in L
                T_ref = [nL; L];
                T = dec2bin(0:(2^h-1)) - '0';
                T = [T,ones(length(T), length(Lv)).*Lv]; %Append evidence to table
                p.table = T;
                

                %Loop through each sample defined by the table
                summ=0;
                for i=1:size(T,1) %row
                    %Loop thorough each node defined in the sample %% TODO:
                    %CHANGE THIS TO LOOP THROUGH ONLY THE VARIABLES LIKLI
                    %TO CHANGE for j=1:size(nL,2) %col
                   
                    mult = 1; 
                    for j=1:size(T,2) %col
                        %Identify the position in the bayes network
                        id = T_ref(j,:);  %char ID
                        k = find(all((bnid==id)')); %position in bn
                        pid_all = bn(k).Parents;

                        %Based on the number of parents, extract the CPT
                        %value given the parents values within the sample
                        switch size(pid_all,1)
                            case 0
                                %Load CPT value for noparents
                                p0 = T(i,all((T_ref==id)'));
                                cpt_val = bn(k).CPT(1);

                            case 1
                                %Find evidence value in sample
                                p0 = T(i,all((T_ref==id)'));
                                p1 = T(i,all((T_ref==pid_all)'));

                                %Load CPT value for 1 parent
                                a=flip(dec2bin(0:(2^1-1))-'0');
                                cpt_val = bn(k).CPT(a(:,1)==p1);

                            case 2
                                %Find evidence value in sample
                                p0 = T(i,all((T_ref==id)'));
                                p1 = T(i,all((T_ref==pid_all(1,:))'));
                                p2 = T(i,all((T_ref==pid_all(2,:))')); 
                                
                                %Load CPT value for 1 parent
                                a=flip(dec2bin(0:(2^2-1))-'0');
                                cpt_val = bn(k).CPT(a(:,1)==p1 & a(:,2)==p2);
                        end
                        
                        %Convert to reverse value if query is false
                        if (p0 == 0)
                            cpt_val = 1-cpt_val;
                        end
                        
                        %Multiply all CPT values within the sample
                        mult = mult * cpt_val;
                    end
                    %Take the sum of all the sample probabilities
                    summ = summ + mult;
                    mult = 1; %#ok<NASGU>
                end
                %Save the probability
                p.raw_probability(2-X_val) = summ;
            end
            
            %Normalize the probability
            p.probability=p.raw_probability*(1/sum(p.raw_probability));
            
            
        end
        function p=emlimination(bn, X_label, e, e_labels) 
            disp("Function not yet available.")
            p.probability = 1;
        end
        function p=rejection(bn, X_label, e, e_labels, total_samples)
            p.Type = "REJECTION";
            p.X = X_label;
            p.e = e_labels;
            p.e_val = e;
            p.Total_Samples = total_samples;

            total_valid_entries = 0;
            counter = 0;

            %Loop through each sample
            for i=1:total_samples
                sample = [];

                %Loop through each node
                for j=1:length(bn)

                    %Generate random state
                    val = rand();

                    %Extract relevant probability from CPT
                    %If the node has parents
                    if (~isempty(bn(j).Parents))
                        L = bn(j).Parents;

                        %Extract their states
                        par = INFERENCE.find_parents_in_network(bn,j);
                        states = [];
                        for S=1:length(par)
                            bn(par(S));
                            states(S) = bn(par(S)).State;
                        end
                        dist=flip(dec2bin(0:(2^size(L,1)-1))-'0');

                        %Extract the CPT
                        if size(bn(j).Parents,1)>1
                            ct = bn(j).CPT(all([dist == states]'));
                        else
                            ct = bn(j).CPT([dist == states]);
                        end

                    else %If there are no parents
                        %Extract the base CPT
                        ct = bn(j).CPT;
                    end

                    %Assign state to node
                    bn(j).State = (val < ct);

                    %If the evidence does not match the sample
                    ep = find(all([bn(j).ID==e_labels]'));
                    if ((ep>0) & e(ep)~=bn(j).State) %#ok<*AND2>
                        %Discard the sample
                        break
                    end
                    sample(j) = bn(j).State; %#ok<AGROW>
                end

                %If the sample is a valid entry
                if length(sample) == 12
                    %Increment total_counter
                    total_valid_entries = total_valid_entries + 1;

                    %Find query in network
                    j=INFERENCE.find_node(bn,X_label);

                    %If query matches
                    if (bn(j).State == true)
                        %Increment counter
                        counter = counter + 1;
                    end

                    %Display generated sample
                    %disp("sample#"+i+": " + mat2str(sample))
                end

            end

            %Calculate ratio of Query to !Query using the counters
            p.Valid_Samples = total_valid_entries;
            p.Prob(1)="True";
            p.Prob(2)="False";
            p.probability(1) = counter/total_valid_entries;
            p.probability(2) = 1-p.probability(1);



            %Loop through each sample
                %Loop through each node
                    %Generate random state
                    %Extract relevant probability from CPT
                    %If the node has parents
                        %Extract their states
                        %Extract the CPT
                    %If there are no parents
                        %Extract the base CPT
                    %Assign state to node
                    %If the evidence does not match the sample
                        %Discard the sample
                %If the sample is a valid entry
                    %Increment total_counter
                    %Find query in network
                    %If query matches
                        %Increment counter
                    %Display generated sample
            %Calculate ratio of Query to !Query using the counters

        end
        function p=likelihood(bn, X_label, e, e_labels, total_samples)
            p.Type = "LIKELIHOOD";
            p.X = X_label;
            p.e = e_labels;
            p.e_val = e;
            p.Total_Samples = total_samples;
            
            total_counter = 0;
            counter = 0;
            
            %Loop through each sample
            for i=1:total_samples
                %sample = [];
                product_list = [];
                
                %Loop through each node
                for j=1:length(bn)
                    
                    %Generate random state
                    val = rand();
                    
                    %Extract relevant probability from CPT
                    %If the node has parents
                    if (~isempty(bn(j).Parents))
                        L = bn(j).Parents;
                        
                        %Extract their states
                        par = INFERENCE.find_parents_in_network(bn,j);
                        states = [];
                        for S=1:length(par)
                            bn(par(S));
                            states(S) = bn(par(S)).State;
                        end
                        dist=flip(dec2bin(0:(2^size(L,1)-1))-'0');
                        
                        %Extract the CPT
                        if size(bn(j).Parents,1)>1
                            ct = bn(j).CPT(all([dist == states]'));
                        else
                            ct = bn(j).CPT([dist == states]);
                        end
                        
                    else %If there are no parents
                        %Extract the base CPT
                        ct = bn(j).CPT;
                    end
                    
                    
                    %If node is evidence
                    ep = find(all([bn(j).ID==e_labels]'));
                    if (ep>0)
                        %Save CPT value to product_list
                        product_list(end+1)=ct;
                        
                        %Set sample state to evidence value
                        bn(j).State = e(ep);
                        
                    else %Else
                        %Assign state to node
                        bn(j).State = (val < ct);
                    end 
                    
                    %Save value to sample
                    %sample(j) = bn(j).State; %#ok<AGROW>
                end
                
                %Find query in network
                j=INFERENCE.find_node(bn,X_label);
                
                %If query matches
                if (bn(j).State == true)
                    %Increment counter
                    counter = counter + prod(product_list);
                end
                    
                %Increment total_counter
                total_counter = total_counter + prod(product_list);
                
                
                %Display generated sample
                %disp("sample#"+i+": " + mat2str(sample))
                
            end
            
            %Calculate ratio of Query to !Query using sample_weights
            p.Total_Weight = total_counter;
            p.Weight_true = counter;
            p.Prob(1)="True";
            p.Prob(2)="False";
            p.probability(1) = counter/total_counter ;
            p.probability(2) = 1-p.probability(1);
            
            
            
            %Loop through each sample
                %Loop through each node
                    %Generate random state
                    %Extract relevant probability from CPT
                    %If node has parents
                        %Extract their states
                        %Extract the CPT
                    %Else node had no parents
                        %Extract the base CPT
                        
                    %If node is evidence
                        %Save CPT value to product_list (check if sum or product)
                        %Set sample state to evidence value
                    %Else
                        %Assign state to node
                
                %Find query in network
                %If query matches
                    %Add sum of product_list to counter
                %Increment total_counter
                
            %Calculate ratio of Query to !Query using sample_weights
            

        end
        function p=gibbs(bn, X_label, e, e_labels) %#ok<*INUSD>
            disp("Function not yet available.")
            p.probability = 1;
        end
        
        %function to return the location of parent p of node j in the network bn
        function ret = find_parents_in_network(bn,j)
            parents = bn(j).Parents;
            ret = zeros(size(parents,1),1);
            for XX=1:length(bn)
                ret(bn(XX).ID == string(bn(j).Parents))=XX;
            end
        end
        
        %function to return the location of node N in the network bn
        function ret = find_node(bn,N)
            for ret=1:length(bn)
                if (bn(ret).ID == N)
                    return
                end
            end
        end
    end
end















