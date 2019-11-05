clc
clear all
d = dir('*.png');
I=imread(d(4).name);
hsv = rgb2hsv(I);
fil = hsv(:,:,1)>0.2;
fil = imfill(fil, 'holes');
fil = imerode(fil, strel('disk',6));
fil = bwmorph(fil, 'thin', 9);

bwboundaries(fil);
[B,L,n,A] = bwboundaries(fil);
imshow(fil); hold on;
colors=['b' 'g' 'r' 'c' 'm' 'y'];
B2={};
%%
for j=1:length(B)
  if (size(B{j},1) > 100)
      B2{size(B2,2)+1} = B{j};
  end
  
end  
%%
for k=1:length(B2)
  boundary = B2{k};
  cidx = mod(k,length(colors))+1;
  plot(boundary(:,2), boundary(:,1),...
       colors(cidx),'LineWidth',2);

  %randomize text position for better visibility
  rndRow = ceil(length(boundary)/(mod(rand*k,7)+1));
  col = boundary(rndRow,2); row = boundary(rndRow,1);
  h = text(col+1, row-1, num2str(L(row,col)));
  set(h,'Color',colors(cidx),'FontSize',14,'FontWeight','bold');
end

%%
b = B{3};
for i=1:length(b)
    X = [b(i,:);mean(b)];
    pdi(i) = pdist(X,'euclidean');
end