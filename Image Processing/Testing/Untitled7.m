close all;
x = 1;
d = dir('*.png');
for j=1:size(d,1)
    I=imread(d(j).name); 
    
    subplot(7,7,x), x = x + 1;
    imshow(I), title(j);
    
    %Plot RGB histograms
    for i=1:3
        subplot(7,7,x), x=x+1;
        histogram(I(:,:,i))
        xlim([0,125]);
    end
    
    %Plot HSV Histograms
    I2 = rgb2hsv(I);
    for i=1:3
        subplot(7,7,x), x=x+1;
        histogram(I2(:,:,i))
        xlim([0,1]);
    end
end



F = figure;
GREENMAX = 84;
HUEMAX = 0.14;
st = strel('disk',3);

pb = uicontrol('style','push',...
                 'units','normalized',...
                 'fontsize',14,...
                 'string','Pause',...
                 'callback',{@pb_call, F});

i=0;
while true
    i=i+1;
    if (i>size(d,1)-1)
        i=1;
    end
    
    I=imread(d(i).name);
    subplot(3,4,1); imagesc(I); axis image; title('1');
    set(gca,'XColor', 'none','YColor','none');

    
    I2 = rgb2hsv(I);
    I3 = I2(:,:,1);
    I3(I3 > 0.5) = 0;
    subplot(3,4,2); imagesc(I3); axis image; title('2');
    set(gca,'XColor', 'none','YColor','none');

    I3(I3<0.14)=0;
    subplot(3,4,3); imagesc(I3); axis image; title('3')
    set(gca,'XColor', 'none','YColor','none');
    
    %I3(I3 < 0.333) = 0;
    I3(I3 ~= 0) = 1;
    imero = imerode(I3,st);
    subplot(3,4,4); imagesc(imero); axis image; title('4')
    set(gca,'XColor', 'none','YColor','none');

    
    
    
    
    
    
    
     
    I=imread(d(i).name);
    subplot(3,4,5); imagesc(I); axis image; title('1');
    set(gca,'XColor', 'none','YColor','none');

    G = I(:,:,2);
    subplot(3,4,6); imagesc(G); axis image; title('2');
    set(gca,'XColor', 'none','YColor','none');

    G2 = G;
    G2(G2<=GREENMAX)=0;
    G2(G2~=0)=1;
    subplot(3,4,7); imagesc(G2); axis image; title('3')
    set(gca,'XColor', 'none','YColor','none');

    bwm = bwmorph(G2, 'skel', 2);
    med = medfilt2(bwm);
    sk = bwmorph(med, 'skel', 2);
    fin = medfilt2(sk, [6,6]);
    subplot(3,4,8); imagesc(fin); axis image; title('4')
    set(gca,'XColor', 'none','YColor','none');
    
%     e = G;
% e(e<77)=0
% surfl(G)
% surfl(e)
% surfl(medfilt2(e,[20,20]))
% imagesc(medfilt2(e,[20,20]))
    
    

%     bwm = bwmorph(imerode(I3, st), 'skel', 4);
%     %bwm = imerode(I3, st);
%     subplot(3,4,4); imagesc(bwm); axis image; title('4')
%     set(gca,'XColor', 'none','YColor','none');
%     
%     med = medfilt2(bwm);
%     subplot(3,4,5); imagesc(med); axis image; title('5')
%     set(gca,'XColor', 'none','YColor','none');
%     
%     sk = bwmorph(med, 'skel', 2);
%     subplot(3,4,6); imagesc(sk); axis image; title('6')
%     set(gca,'XColor', 'none','YColor','none');
%     
%     fin = medfilt2(sk, [6,6]);
%     subplot(3,4,7); imagesc(fin); axis image; title('7')
%     set(gca,'XColor', 'none','YColor','none');
%     
%     rec = imreconstruct(fin, logical(G));
%     subplot(3,4,8); imagesc(rec); axis image; title('8')
%     set(gca,'XColor', 'none','YColor','none');
%     
%     fil = imfill(rec, 'holes');
%     subplot(3,4,9); imagesc(fil); axis image; title('9')
%     set(gca,'XColor', 'none','YColor','none');
%     
%     ime = imerode(fil,st);
%     subplot(3,4,10); imagesc(ime); axis image; title('10')
%     set(gca,'XColor', 'none','YColor','none');
    
    

    rec2 = imreconstruct(fin, logical(imero));
    subplot(3,4,9); imagesc(rec2); axis image; title('rec')
    set(gca,'XColor', 'none','YColor','none');


    
    
    
    
    TOTAL_WAIT_TIME = 2;
    TOTAL_LOOPS = 15;
    for k=1:TOTAL_LOOPS
        ax = subplot(6,8,48);
        pb.Position(1) = ax.Position(1);
        pb.Position(3) = ax.Position(3);
        
        
        
        pie([(TOTAL_LOOPS+1)-k,k]); 
        delete(ax.Children(1:size(ax.Children,1)-1))
        ax.Children(size(ax.Children,1)).FaceColor = [(k/TOTAL_LOOPS),1-(k/TOTAL_LOOPS),0];
        pause(TOTAL_WAIT_TIME/TOTAL_LOOPS)
        
        while F.Name == "paused"
            pause(0.1);
        end
        
    end
    
    
    
end



function pb_call(varargin)
    F = varargin{3};
    b = gcbo;
    if F.Name == "paused"
        F.Name = "running";
        b.String="Pause";
    else
        F.Name = "paused";
        b.String="Run";
    end
end













































