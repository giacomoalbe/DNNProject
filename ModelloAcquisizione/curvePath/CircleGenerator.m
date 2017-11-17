% Centro
x  = 3000;
y  = 3000;
% Raggio
r = 2000;


th = 0:pi/180:2*pi-pi/180;
xunit = r * cos(th) + x;
yunit = r * sin(th) + y;
theta = th.*180/pi;
datapath = [xunit;yunit;theta];
size(datapath)

fileID = fopen('D:\AmbienteLinux\AmbientePython\SOG-Cam_Project\ModelloAcquisizione\curvePath\CircleData.txt','w');
fprintf(fileID,'%s\t%s\t%s\r\n','X','Y','Theta');
fprintf(fileID,'%0.2f\t%0.2f\t%0.2f\r\n',datapath);
type CircleData.txt