%{
    tom = new BAYESIAN_NETWORK(structure)
    tom.generate_CPT(dataset)
    tom.plot_data()
    tom.infer('SM', true, ['CO';'FA'], [true; true], 'enumeration')

%}



classdef netty < handle
    properties
        net
    end
    methods
        function b = netty()
            
            b.net = 1;
            
        end
        
        function [] = loader(f)
            disp("loader")
            netty.loader2();
        end
    end
    
    methods(Static)
        function [] = loader2()
            disp("loader2")
            b.net = 1;
        end
    end
end