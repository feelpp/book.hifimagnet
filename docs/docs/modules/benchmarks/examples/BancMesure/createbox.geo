// hs=1;
// rbox = 29;
// zbox0 = 91;
// zbox1 = 92;
// //zbox=5;

np_zaxis=50;
np_ext=50;

Point(5000) = {rbox, 0, zbox1, hs};
Point(6000) = {-rbox, 0, zbox1, hs};
Point(7000) = {0, rbox, zbox1, hs};
Point(8000) = {0, -rbox, zbox1, hs};
Point(10000) = {0, 0, zbox1, hs};


Circle(5001) = {7000, 10000, 5000};
Circle(6001) = {5000, 10000, 8000};
Circle(7001) = {8000, 10000, 6000};
Circle(8001) = {6000, 10000, 7000};

Line Loop(64000) = {7001, 8001, 5001, 6001};
Plane Surface(65000) = {64000};


Point(11000) = {rbox, 0, zbox0, hs};
Point(12000) = {-rbox, 0, zbox0, hs};
Point(13000) = {0, rbox, zbox0, hs};
Point(14000) = {0, -rbox, zbox0, hs};
Point(15000) = {0, 0, zbox0, hs};


Circle(9001) = {13000, 15000, 11000};
Circle(10001) = {11000, 15000, 14000};
Circle(11001) = {14000, 15000, 12000};
Circle(12001) = {12000, 15000, 13000};

Line Loop(64001) = {11001, 12001, 9001, 10001};
Plane Surface(65001) = {64001};

Line(65016) = {10000, 15000};
//Transfinite Line{65016} = np_zaxis;

// create box
Line(65002) = {8000, 14000};
Line(65003) = {5000, 11000};
Line(65004) = {7000, 13000};
Line(65005) = {6000, 12000};
//Transfinite Line{65002,65003,65004,65005} = np_ext;


Line Loop(65006) = {6001, 65002, -10001, -65003};
Ruled Surface(65007) = {65006};
Line Loop(65008) = {5001, 65003, -9001, -65004};
Ruled Surface(65009) = {65008};
Line Loop(65010) = {65004, -12001, -65005, 8001};
Ruled Surface(65011) = {65010};
Line Loop(65012) = {65002, 11001, -65005, -7001};
Ruled Surface(65013) = {65012};
Surface Loop(65014) = {65000, 65013, 65007, 65001, 65011, 65009};
Volume(65015) = {65014};

Physical Volume("Box") = {65015};
