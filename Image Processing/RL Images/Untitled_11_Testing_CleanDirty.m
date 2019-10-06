figure;
I = Messy;

subplot(4,1,1)
imshow(I)
    
%Plot RGB histograms
x = [3,5,7];
for i=1:3
    subplot(4,2,x(i))
    histogram(I(:,:,i))
end

%Plot HSV Histograms
I2 = rgb2hsv(I);
for i=1:3
    subplot(4,2,x(i)+1)
    histogram(I2(:,:,i))
end