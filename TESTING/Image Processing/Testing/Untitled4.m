% close all;
d = dir('*.png');
PAUSER = false;
F = figure;

GREENMAX = 84;
st = strel('disk',3);

pb = uicontrol('style','push',...
                 'units','normalized',...
                 'fontsize',14,...
                 'string','Pause',...
                 'callback',{@pb_call, F});

i=0;
while true
    i=i+1;
    if (i>size(d,1))
        i=1;
    end
    
    I=imread(d(i).name);
    subplot(3,4,1); imagesc(I); axis image; title('1');
    set(gca,'XColor', 'none','YColor','none');

    G = I(:,:,2);
    subplot(3,4,2); imagesc(G); axis image; title('2');
    set(gca,'XColor', 'none','YColor','none');

    G(G<=GREENMAX)=0;
    G(G~=0)=1;
    subplot(3,4,3); imagesc(G); axis image; title('3')
    set(gca,'XColor', 'none','YColor','none');


    bwm = bwmorph(G, 'skel', 2);
    subplot(3,4,4); imagesc(bwm); axis image; title('4')
    set(gca,'XColor', 'none','YColor','none');
    
    med = medfilt2(bwm);
    subplot(3,4,5); imagesc(med); axis image; title('5')
    set(gca,'XColor', 'none','YColor','none');
    
    sk = bwmorph(med, 'skel', 2);
    subplot(3,4,6); imagesc(sk); axis image; title('6')
    set(gca,'XColor', 'none','YColor','none');
    
    fin = medfilt2(sk, [6,6]);
    subplot(3,4,7); imagesc(fin); axis image; title('7')
    set(gca,'XColor', 'none','YColor','none');
    
    rec = imreconstruct(fin, logical(G));
    subplot(3,4,8); imagesc(rec); axis image; title('8')
    set(gca,'XColor', 'none','YColor','none');
    
    fil = imfill(rec, 'holes');
    subplot(3,4,9); imagesc(fil); axis image; title('9')
    set(gca,'XColor', 'none','YColor','none');
    
    ime = imerode(fil,st);
    subplot(3,4,10); imagesc(ime); axis image; title('10')
    set(gca,'XColor', 'none','YColor','none');
    
    
    
    
    
    
    
%     sk2 = bwskel(rec);
%     subplot(3,4,11); imagesc(sk2); axis image; title('11')
%     
%     [lbl, num]=bwlabel(sk2);
%     %end2 = ;
%     x=[];
%     x(1)=0;
%     for j=1:num
%         x(j)=sum(sum(bwmorph(lbl==j, 'endpoints')));
%     end
%     subplot(3,4,12); imagesc(lbl); axis image; title(x);
%     
    
    
%     subplot(100,1,100)
%     plot([1,1]);
%     xlim([0,10]);
    TOTAL_WAIT_TIME = 2;
    TOTAL_LOOPS = 180;
    for k=1:TOTAL_LOOPS
        ax = subplot(6,8,48);
        pb.Position(1) = ax.Position(1);
        pb.Position(3) = ax.Position(3);
        
        
        
        pie([(TOTAL_LOOPS+1)-k,k]); 
        delete(ax.Children(1:size(ax.Children,1)-1))
        ax.Children(size(ax.Children,1)).FaceColor = [(k/TOTAL_LOOPS),1-(k/TOTAL_LOOPS),0];
        pause(TOTAL_WAIT_TIME/TOTAL_LOOPS)
        
        while F.Name == "paused"
            pause(0.2);
        end
        
    end
    
    
    
end



function pb_call(varargin)
    "pb_call"
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













































