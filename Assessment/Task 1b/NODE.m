classdef NODE < handle
    properties
        ID
        Name
        CPT
        Parents
        Position
        State
    end
    methods
        function node = NODE(varargin)
            for i =1:2:length(varargin)
                
                a=varargin(i+1);
                b=a{:};
                if size(b{:},1) == 0; continue; end
                
                %Apply Named arguments to Object
                switch cell2mat(varargin(i))
                    case 'ID'
                        node.ID = char(b);
                    case 'Name'
                        node.Name = char(b);
                    case 'CPT'
                        node.CPT = cell2mat(b);
                    case 'Parents'
                        node.Parents = char(b);
                    case 'Position'
                        node.Position = cell2mat(b);
                end
            end
            
        end
        
    end
end