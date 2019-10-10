clc;
cla;
clear all;

%Function Definition
cast_ray = @ray;

% Define Boundary
x = -100:100;
y = x.*0;

% Plot Boundary
plot(x, y+max(x), 'b', x, y+min(x), 'b', y+max(x), x, 'b', y+min(x), x, 'b');
grid on;
axis image;
hold on;

% Plot Robot
scatter(0,0,200,'filled','r','s')

r = rand()*360;
for i = 0+r:5:180+r
    cast_ray(i);
end
[rx, ry] = cast_ray(90+r);
scatter(rx, ry,100,'filled','r');
title(r-(360*floor(r/360)))






function [retX, retY] = ray(direction) %degrees clockwise from +x
    
    %Calculate Ray
    %direction = rand()*360; %degrees clockwise from +x
    direction = direction-(360*floor(direction/360));
    if (direction == 90 || direction == 270)
        direction = direction + 0.00000001;
    end

    % Define Ray
    m = -sind(direction)/cosd(direction);

    if (direction<45 || direction>=315) %East Wall
%         disp("East -> " + direction + " -> " + m);
        x = 0:100;
        plot(x,x*m,'c');
        scatter(100,100*m,50,'filled','g')
        retX = 100; retY = 100*m;
        
    elseif (direction<135) %South Wall
%         disp("South -> " + direction + " -> " + m);
        y = -100:0;
        plot(y/m,y,'c');
        scatter(-100/m,-100,50,'filled','g')
        retX = -100/m; retY = -100;
        
    elseif (direction<225) %West Wall
%         disp("West -> " + direction + " -> " + m);
        x = -100:0;
        plot(x,x*m,'c');
        scatter(-100,-100*m,50,'filled','g')
        retX = -100; retY = -100*m;
        
    elseif (direction<315) %North Wall
%         disp("North -> " + direction + " -> " + m);
        y = 0:100;
        plot(y/m,y,'c');
        scatter(100/m,100,50,'filled','g')
        retX = 100/m; retY = 100;
    end

end






