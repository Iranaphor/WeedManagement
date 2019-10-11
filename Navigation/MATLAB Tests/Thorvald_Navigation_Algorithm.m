clc;
cla;
clear all;

%Function Definition
cast_ray = @ray;

% Define Boundary
xB = -100:100;
yB = xB.*0;

%% Plot Boundary
subplot(4,1,1:3); cla
plot(xB, yB+max(xB), 'b', xB, yB+min(xB), 'b', yB+max(xB), xB, 'b', yB+min(xB), xB, 'b');
grid on;
axis image;
hold on;

%% Plot Robot
startX = (rand()-0.5)*200;
startY = (rand()-0.5)*200;

scatter(startX, startY, 200, 'filled', 'r', 's')
  

%% Perform Laser Scan
r = rand()*360;
total_degrees = 180;
increments = 2;


FOV = floor(total_degrees/2);
endpoints = zeros(2,total_degrees/increments);
j=1;
for i = -FOV:increments:FOV
    [rx, ry] = cast_ray(i+r, startX, startY, -100, 100, -100, 100);
    endpoints(:,j) = [rx, ry];
    j=j+1;
end


%% Plot Focal Point
[rx, ry] = cast_ray(r, startX, startY, -100, 100, -100, 100);
scatter(rx, ry,100,'filled','r');
title("Robot @ [" + startX + ", " + startY + "] w/ direction: " + (r-(360*floor(r/360))) + "°")


scatter(startX, startY, 200, 'filled', 'r', 's')
%% Convert laserscan coordinates to distances
distances = sqrt((endpoints(1,:)-startX).^2 + (endpoints(2,:)-startY).^2);
subplot(4,1,4), cla, plot(distances);


%% Cast ray and find where hit
function [retX, retY] = ray(direction, oX, oY, xMin, xMax, yMin, yMax) %degrees clockwise from +x
    %% Define Corners
    o = oY-yMin; a = xMax-oX;    ang1 = atand(o/a)+(0);
    a = oY-yMin; o = oX-xMin;    ang2 = atand(o/a)+(90);
    o = yMax-oY; a = oX-xMin;    ang3 = atand(o/a)+(180);
    a = yMax-oY; o = xMax-oX;    ang4 = atand(o/a)+(270);
    
    %% Calculate Ray
    direction = direction-(360*floor(direction/360));
    if (direction == 90 || direction == 270)
        direction = direction + 0.00000001;
    end

    %% Define Ray
    m = -sind(direction)/cosd(direction);
    c = oY-(m*oX);
    
    
    %% Determine Which wall is hit
    if (direction<ang1 || direction>=ang4) %East Wall
        disp("East -> " + direction + " -> " + m);
        x = oX:xMax;
        plot(x,(x*m)+c,'c');
        retX = xMax; retY = (xMax*m)+c;
        
    elseif (direction<ang2) %South Wall
        disp("South -> " + direction + " -> " + m);
        y = yMin:oY;
        plot((y-c)/m,y,'c');
        retX = (yMin-c)/m; retY = yMin;
        
    elseif (direction<ang3) %West Wall
        disp("West -> " + direction + " -> " + m);
        x = xMin:oX;
        plot(x,(x*m)+c,'c');
        retX = xMin; retY = (xMin*m)+c;
        
    elseif (direction<ang4) %North Wall
        disp("North -> " + direction + " -> " + m);
        y = oY:yMax;
        plot((y-c)/m,y,'c');
        retX = (yMax-c)/m; retY = yMax;
    end
    
    scatter(retX, retY,20,'filled','g')

end






