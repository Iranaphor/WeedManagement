clc;
cla;
clear;

%Function Definition
cast_ray = @ray;

%% Define Boundary
xB = -100:100;
yB = xB.*0;
Corners = [-100, 100, -100, 100];

% Plot Boundary
subplot(4,1,1:3); cla
plot(xB, yB+max(xB), 'b', xB, yB+min(xB), 'b', yB+max(xB), xB, 'b', yB+min(xB), xB, 'b');
grid on;
axis image;
hold on;

%% Plot Robot
startX = (rand()-0.5)*200;
startY = (rand()-0.5)*200;
r = rand()*360;
title("Robot @ [" + startX + ", " + startY + "] w/ direction: " + (r-(360*floor(r/360))) + "°")

scatter(startX, startY, 200, 'filled', 'r', 's');
  

% Perform Laser Scan
distances = rayScan(startX, startY, r, Corners);
subplot(4,1,4), cla, plot(distances);
findpeaks(distances);
[pks,locs] = findpeaks(distances);
subplot(4,1,1:3)


% Plot Focal Point
[rx, ry] = cast_ray(r, startX, startY, Corners, ...
                    'Ray_Show', true, ...
                    'Ray_Size', 5, ...
                    'Collision_Color', 'r', ...
                    'Collision_Size', 75);

%% Plot Corner Radius'
corners = [100,-100;-100,-100;-100,100;100,100];
plot_corner_radi(corners, pks);






%%
%{
if (size(pks,2) == 2)
    
    sctr2 = find_intersections(corners, pks(1), pks(2));
    scatter(sctr2(1,:), sctr2(2,:), 400, 'k');
    
elseif (size(pks,2) == 3)
    sctr_a = find_intersections(corners, pks(1), pks(2));
    sctr_b = find_intersections(corners, pks(1), pks(3));
    sctr_c = find_intersections(corners, pks(2), pks(3));
    
    scatter(sctr_a(1,:), sctr_a(2,:), 400, 'm');
    scatter(sctr_b(1,:), sctr_b(2,:), 400, 'm', 'p');
    scatter(sctr_c(1,:), sctr_c(2,:), 400, 'm', 'd');

    %sctr_ab = sctr_a(:,logical(sum(ismember(round(sctr_a),round(sctr_b)))-1));
    %sctr_abc = sctr_ab(:,logical(sum(ismember(round(sctr_ab),round(sctr_c)))-1));    
    %scatter(sctr_abc(1,:), sctr_abc(2,:), 400, [255/255, 165/255, 0], '*');
    
end
%}

%%
%{

1-peak:
    plot potential positions
    determine which way to turn to find the second peak quickest
    turn till 2 peaks reached

2-peak:
    caculate distance from peaks
    plot potential positions

3-peak:
    plot potential positions using triangulation
    viscircles(centre, radius)

%}




scatter(startX, startY, 200, 'filled', 'r', 's')



%% Calculate Intersections between 2 radius'
function intersections = find_intersections(corners, radius_A, radius_B)

    sctr = NaN(2,1);
    
    
    for si = 1:size(corners,1) %loop(1st rings)
        for sj = 1:size(corners,1) %loop(2nd rings)
            if (si~=sj)
                [xout, yout] = circcirc(corners(si,1), corners(si,2), radius_A, ... 
                                        corners(sj,1), corners(sj,2), radius_B);
                sctr(:,size(sctr,2)+1) = [xout(1), yout(1)];
                sctr(:,size(sctr,2)+1) = [xout(2), yout(2)];
                
            end
        end
    end
    
    %Clean the data
    sctr(:,~any(~isnan(sctr)))=[]; 
    sctr(:,any(sctr>100))=[]; 
    sctr(:,any(sctr<-100))=[];
    
    intersections = sctr;
end






%% Plot the Radius' from the Corners
function [] = plot_corner_radi(corners, pks)
    colours = ['b','m','y','g'];

    for cj = 1:size(corners,1)
        for ci=1:size(pks,2)
            viscircles(corners(cj,:),pks(ci), 'Color', colours(ci));
        end
    end
    xlim([-100,100]); ylim([-100,100]);
end




%% Perform a Laserscan
function [rays] = rayScan(X, Y, D, Corners)
    total_degrees = 180;
    increments = 1;
    
    FOV = floor(total_degrees/2);
    endpoints = zeros(2,total_degrees/increments);
    
    j=1;
    for i = -FOV:increments:FOV
        [rx, ry] = ray(i+D, X, Y, Corners);
        endpoints(:,j) = [rx, ry];
        j=j+1;
    end
    
    
    % Convert laserscan coordinates to distances
    rays = sqrt((endpoints(1,:)-X).^2 + (endpoints(2,:)-Y).^2);
    
end




%% Cast ray and find where hit
function [retX, retY] = ray(direction, oX, oY, Corners, varargin) %degrees clockwise from +x

    collision_show = true;
    collision_color = 'g';
    collision_size = 20;
    ray_show = false;
    ray_color = 'c';
    ray_size = 0.5;
    
    for i =1:2:length(varargin)
        switch cell2mat(varargin(i))
            case 'Collision_Show'
                collision_show = cell2mat(varargin(i+1));
            case 'Collision_Color'
                collision_color = cell2mat(varargin(i+1));
            case 'Collision_Size'
                collision_size = cell2mat(varargin(i+1));
            case 'Ray_Show'
                ray_show = cell2mat(varargin(i+1));
            case 'Ray_Color'
                ray_color = cell2mat(varargin(i+1));
            case 'Ray_Size'
                ray_size = cell2mat(varargin(i+1));
            otherwise
                n='';
        end
    end




    %% Define Corners
    xMin = Corners(1);
    xMax = Corners(2);
    yMin = Corners(3);
    yMax = Corners(4);

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
%         disp("East -> " + direction + " -> " + m);
        x = oX:xMax;
        if (ray_show), plot(x,(x*m)+c,ray_color, 'LineWidth', ray_size); end
        retX = xMax; retY = (xMax*m)+c;
        
    elseif (direction<ang2) %South Wall
%         disp("South -> " + direction + " -> " + m);
        y = yMin:oY;
        if (ray_show), plot((y-c)/m,y,ray_color, 'LineWidth', ray_size); end
        retX = (yMin-c)/m; retY = yMin;
        
    elseif (direction<ang3) %West Wall
%         disp("West -> " + direction + " -> " + m);
        x = xMin:oX;
        if (ray_show), plot(x,(x*m)+c,ray_color, 'LineWidth', ray_size); end
        retX = xMin; retY = (xMin*m)+c;
        
    elseif (direction<ang4) %North Wall
%         disp("North -> " + direction + " -> " + m);
        y = oY:yMax;
        if (ray_show), plot((y-c)/m,y,ray_color, 'LineWidth', ray_size); end
        retX = (yMax-c)/m; retY = yMax;
    end
    
    if (collision_show), scatter(retX, retY, collision_size,'filled',collision_color); end

end






