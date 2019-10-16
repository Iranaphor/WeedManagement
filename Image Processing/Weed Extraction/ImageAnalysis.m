%% Ask Mark: how wide a range does the weed killer spread when sprayed

clear;
clc;

%% Setup
%{
I_1a = imread('Analysis1a.png'); 
I_1b = imread('Analysis1b.png'); I_1_values = [.2, .34];  %https://www.mathworks.com/help/images/ref/hough.html
I_2 = imread('Analysis2.png'); I_2_values = [.2, .34];
I_3 = imread('Analysis3.png'); I_3_values = [.2, .25];

image = "1a";
switch(image)
    case "1a"
        I = I_1a;
        I_values = I_1_values;
    case "1b"
        I = I_1b;
        I_values = I_1_values;
    case "2"
        I = I_2;
        I_values = I_2_values;
    case "3"
        I = I_3;
        I_values = I_3_values;
    otherwise
        I = I_2;
        I_values = I_2_values;
end

I2 = rgb2hsv(I);

% Dirt
dirtMask = ~imbinarize(I2(:,:,1),I_values(1));
dirt = I.*uint8(dirtMask);

% Weed
weed_binary = imbinarize(imbinarize(I2(:,:,1),I_values(2))-dirtMask, 0.1);
weed_erode = imerode(weed_binary, ones(5));
weed_filtered = imreconstruct(weed_erode, weed_binary);
weed_filled = imfill(weed_filtered, 'holes');
weedMask = imdilate(weed_filled, strel('octagon',12));
weed = I.*uint8(weedMask);
%imagesc(imreconstruct(~weedMask, imerode(~weedMask, ones(30))))

% Plant
plantMask = ~(dirtMask+weedMask);
plant = I.*uint8(plantMask);

if (image == "1a" || image == "1b")
    tempMask = plantMask;
    plantMask = weedMask;
    weedMask = tempMask;
    dirt = I.*uint8(dirtMask);
    weed = I.*uint8(weedMask);
end


% Identification
Ib = I;
Ib(:,:,1)=Ib(:,:,1)+uint8(weedMask(:,:,1)*255);
% Plotting
figure(19);
subplot(3,2,1); imagesc(I); axis image; title("Brerakdown Image " + image);
subplot(3,2,2); imagesc(dirtMask); axis image;
subplot(3,2,3); imagesc(weedMask); axis image;
subplot(3,2,4); imagesc(plantMask); axis image;
subplot(3,1,3); imagesc(Ib); axis image;

%figure(20); 
%subplot(2,1,1); imshow(Ib);
%}

%% IMG(3)
figure(2) 
im3 = imread('Analysis3.png');
subplot(321); imshow(im3); title("RGB Image");
im3_hsv = rgb2hsv(im3);
subplot(325); imshow(im3_hsv); title("HSV Image");
im3_r = im3(:,:,1);
im3_g = im3(:,:,2);
im3_b = im3(:,:,3);
im3_h = im3_hsv(:,:,1);
im3_s = im3_hsv(:,:,2);
im3_v = im3_hsv(:,:,3);

% Plant Mask
im3_plant_2 = im3_h;
im3_plant_2(round(im3_plant_2*100)~=24) = 0;
im3_plant_3 = imopen(im3_plant_2,ones(10));
im3_plant_4 = imreconstruct(im3_plant_3,im3_plant_2);
im3_plant_5 = logical(imfill(im3_plant_4));
subplot(324); imagesc(im3_plant_5); axis image; title("plant mask");

% Dirt Mask
im3_dirt_1 = ~imbinarize(im3_h,.2);
subplot(322); imagesc(logical(im3_dirt_1)); axis image; title("dirt mask");

% Weed Mask
im3_weed_1 = (im3_h>im3_s);
subplot(326); imagesc(logical(im3_weed_1)); axis image; title("weed mask");


% Weed Overlay
im3_b2 = im3;
im3_b2(:,:,1) = im3_b2(:,:,1)+uint8(im3_weed_1*100);
im3_b2(:,:,2) = im3_b2(:,:,2)+uint8(im3_plant_5*100);
im3_b2(:,:,3) = im3_b2(:,:,3)+uint8(im3_dirt_1*100);
subplot(323); imagesc(im3_b2); axis image; title("Weed Overlay");



%% IMG(2) 
figure(3)
im2 = imread('Analysis2.png');
subplot(321); imshow(im2); title("RGB Image");

im2_hsv = rgb2hsv(im2);
subplot(325); imshow(im2_hsv); title("HSV Image");
im2_r = im2(:,:,1);
im2_g = im2(:,:,2);
im2_b = im2(:,:,3);
im2_h = im2_hsv(:,:,1);
im2_s = im2_hsv(:,:,2);
im2_v = im2_hsv(:,:,3);


%{
im2_v identify some the leaves of plants
1-im2_v identifies borders well
1-im2_h weeds are darkest parts
-((1-im2_h).*im2_h) can be used to identify dirt
%}

% Dirt Mask
im2_dirt_1 = ((1-im2_h).*im2_h);
im2_dirt_2 = imbinarize(im2_dirt_1, .145);
im2_dirt_3 = ~imfill(im2_dirt_2, 'holes');
subplot(322); imagesc(im2_dirt_3); axis image; title("dirt mask");


% Plant Mask
im2_plant_1 = imopen(~im2_dirt_3, strel('disk',20));
subplot(324); imagesc(im2_plant_1); axis image; title("plant mask");

% Weed Mask
im2_weed_1 = imdilate(im2_plant_1,strel('disk', 25)) + im2_dirt_3; 
im2_weed_2 = ~imbinarize(im2_weed_1, 0);
subplot(326); imagesc(im2_weed_2); axis image; title("weed mask");


% Weed Overlay
im2_b2 = im2;
im2_b2(:,:,1) = im2_b2(:,:,1)+uint8(im2_weed_2*100);
im2_b2(:,:,2) = im2_b2(:,:,2)+uint8(im2_plant_1*100);
im2_b2(:,:,3) = im2_b2(:,:,3)+uint8(im2_dirt_3*100);
subplot(323); imagesc(im2_b2); axis image; title("Weed Overlay");



%% IMG(2) 
figure(4)
im1 = imread('Analysis1a.png');
subplot(321); imshow(im1); title("RGB Image");
im1_hsv = rgb2hsv(im1);
subplot(325); imshow(im1_hsv); title("HSV Image");
im1_r = im1(:,:,1);
im1_g = im1(:,:,2);
im1_b = im1(:,:,3);
im1_h = im1_hsv(:,:,1);
im1_s = im1_hsv(:,:,2);
im1_v = im1_hsv(:,:,3);


% Dirt Mask
im1_dirt_1 = ~imbinarize(im1_h, 0.17);
subplot(322); imagesc(im1_dirt_1); axis image; title("dirt mask");


% Plant Mask
im1_plant_1 = imbinarize(im1_h, 0.37);
im1_plant_2 = (im1_plant_1'.*sum(im1_plant_1,2)')';
im1_plant_3 = im1_plant_2/max(im1_plant_2, [], 'all');
im1_plant_4 = imbinarize(im1_plant_3,0.35);
im1_plant_5 = imdilate(im1_plant_4, ones(15));
subplot(324); imagesc(im1_plant_5); axis image; title("plant mask");

% Weed Mask
im1_weed_1 = (im1_plant_1.*0)+1;
im1_weed_2 = (im1_weed_1'.*sum(im1_plant_1,2)')';
im1_weed_3 = imbinarize(im1_weed_2,0.35*max(im1_weed_2, [], 'all'));
im1_weed_4 = ~(im1_weed_3+im1_dirt_1);
subplot(326); imagesc(im1_weed_4); axis image; title("weed mask");

% Weed Targets
im1_weed_target_1a = imopen(im1_weed_4, strel('disk', 15));
im1_weed_target_2a = imfill(im1_weed_target_1a, 'holes');

im1_weed_target_1b = imfill(im1_weed_4, 'holes');
im1_weed_target_2b = imerode(im1_weed_target_1b, strel('disk', 50));

im1_weed_target_2c = imerode(im1_weed_4, strel('disk', 15));

im1_weed_target_2 = im1_weed_target_2c;


% Weed Overlay
im1_b2 = im1;
im1_b2(:,:,1) = im1_b2(:,:,1)+uint8(im1_weed_4*100);
im1_b2(:,:,1) = im1_b2(:,:,1)+uint8(im1_weed_target_2*255);
im1_b2(:,:,2) = im1_b2(:,:,2)+uint8(im1_plant_5*100);
im1_b2(:,:,3) = im1_b2(:,:,3)+uint8(im1_dirt_1*100);
subplot(323); imagesc(im1_b2); axis image; title("Weed Overlay");

%{
figure(50);
im1_b2 = im1;
im1_b2(:,:,1) = im1_b2(:,:,1)+uint8(im1_weed_4*100);
im1_b2(:,:,2) = im1_b2(:,:,2)+uint8(im1_plant_5*100);
im1_b2(:,:,3) = im1_b2(:,:,3)+uint8(im1_dirt_1*100);

im1_b2a = im1_b2;
im1_b2a(:,:,1) = im1_b2a(:,:,1)+uint8(im1_weed_target_2a*255);
subplot(311); imagesc(im1_b2a); axis image;

im1_b2b = im1_b2;
im1_b2b(:,:,1) = im1_b2b(:,:,1)+uint8(im1_weed_target_2b*255);
subplot(312); imagesc(im1_b2b); axis image;

im1_b2c = im1_b2;
im1_b2c(:,:,1) = im1_b2c(:,:,1)+uint8(im1_weed_target_2c*255);
subplot(313); imagesc(im1_b2c); axis image;
%}


