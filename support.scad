





module support(x,y,z,sphereSize,height){difference(x,y,z,sphereSize,height){difference(x,y,z,sphereSize,height){translate([x,y,z])sphere(sphereSize*1.1);cubeSize = 2*(sphereSize*1.1);translate([x,y,z+sphereSize*0.7])cube([cubeSize,cubeSize,cubeSize],true);}translate([x,y,z])sphere(sphereSize);}supportHeight=(z-sphereSize)+height;translate([x,y,z+(-((supportHeight*0.5)+sphereSize))])cylinder(supportHeight,sphereSize*0.3,sphereSize*0.3,true);}



support(0,0,0,40,200);
support(100,20,2000,40,200);