function [a] = FindAlignment(im_plant, varargin)

    plotter = false;
    iter = 1;
    for i=1:2:size(varargin,2)
        switch (varargin(i))
            case "Plot"
                plotter = varargin(i+1);
            case "Iteration"
                iter = varargin(i+1);
        end
    end
    
    h = gcf;
    figure(30);
    
    a = nan(1,180/iter);
    for i=1:iter:180   
        figure(30);
        rot = imrotate(im_plant,i,'bilinear','crop');
        data = sum(rot');
        [~, pks] = findpeaks(smoothdata(data));
        a(((i-mod(i,iter))/iter)) = size(pks,2);
        
        if (plotter)
            subplot(5,1,1:4); plot(smoothdata(data));
            title("Rotation(" + i + ") Peaks(" + size(pks,2) + ") Minimum(" + min(a) + ")");
            subplot(5,5,21:24); plot(smoothdata(a));
            subplot(5,5,25); imagesc(rot);
            pause(0.001);
        end
    end
    figure(h.Number);
end