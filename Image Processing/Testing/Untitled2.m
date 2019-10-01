GREENMAX = 84;


I=imread(d(8).name);
subplot(3,3,1), imagesc(I); axis image; title('BASE')

G = I(:,:,2);
subplot(3,3,4), imagesc(I); axis image; title('GREEN ONLY')

G(G<=GREENMAX)=0; 
G(G~=0)=1;
subplot(3,3,5), imagesc(G); axis image; title('Binary')


BW = bwlabel(G);
subplot(3,3,6), imagesc(BW); axis image; title('Label')



Q = medfilt2(I(:,:,2));
subplot(3,3,7), imagesc(Q); axis image; title('MED FILTERED')

Q(Q<=GREENMAX)=0; 
Q(Q~=0)=1;
subplot(3,3,8), imagesc(Q); axis image; title('Filtered Binary')


BW = bwlabel(Q);
subplot(3,3,9), imagesc(BW); axis image; title('Filtered Label')





smooth = imerode(I(:,:,2), strel('disk',3));
subplot(3,3,2), imagesc(smooth); axis image, title('imOpen');


subplot(3,3,3), imagesc(smooth(:,:,2)); axis image, title('imOpen G');