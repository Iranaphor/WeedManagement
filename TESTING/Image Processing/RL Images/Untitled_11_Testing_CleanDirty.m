%% Setup
figure
Messy = imread('messy.png');
Clean = imread('clean.png');
Fake = imread('fake.png');
I = Messy;
I2 = rgb2hsv(I);

%% Dirt
dirtMask = imbinarize(I2(:,:,1),.55);
dirt = I.*uint8(dirtMask);

%% Weed
weed_binary = imbinarize(I2(:,:,1),.4)-dirtMask;
weed_erode = imerode(weed_binary, ones(11));
weed_filtered = imreconstruct(weed_erode, weed_binary);
weed_filled = imfill(weed_filtered, 'holes');
weedMask = imdilate(weed_filled, strel('octagon',12));
weed = I.*uint8(weedMask);

%% Carrot
carrotMask = ~(dirtMask+weedMask);
carrot = I.*uint8(carrotMask);

%% Plotting
subplot(2,2,1); imagesc(I); axis image;
subplot(2,2,2); imagesc(dirt); axis image;
subplot(2,2,3); imagesc(weed); axis image;
subplot(2,2,4); imagesc(carrot); axis image;