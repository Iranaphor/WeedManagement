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