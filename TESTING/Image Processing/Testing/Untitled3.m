GREENMAX = 84;
st = strel('disk',3);

i=0;
while true
    i=i+1;
    if (i>5) 
        i=1;
    end
    
    I=imread(d(i+3).name);
    subplot(2,2,1), imagesc(I); axis image; title('BASE')

    G = I(:,:,2);
    subplot(2,2,2), imagesc(G); axis image; title('GREEN ONLY');

    G(G<=GREENMAX)=0;
    G(G~=0)=1;
    subplot(2,2,3), imagesc(G); axis image; title('Binary')


    bwm = bwmorph(G, 'skel', 2);
    med = medfilt2(bwm);
    sk = bwmorph(med, 'skel', 2);
    fin = medfilt2(sk, [6,6]);
    rec = imreconstruct(fin, logical(G));
    fil = imfill(rec, 'holes');
    subplot(2,2,4), imagesc(imerode(fil,st)); axis image
    
    pause(2)
end