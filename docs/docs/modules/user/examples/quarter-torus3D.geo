// -*- vim:filetype=gmsh
Mesh.OptimizeNetgen=0; // otherwise it crashes when IsFull=1

IsFull=0;
Unit=1.e-3;
h = 1;
h_inf = 10*h;
h_ext = 10*h;

r1=61.2*0.5;
r2=106.4*0.5;
L=4.61/2.;

r_inf=300;
r_ext=200;

// Define torus section
P0= newp; Point(P0) = {0,0,0, h};
P1= newp; Point(P1) = {r1,0,-L, h};
P2= newp; Point(P2) = {r2,0,-L, h};
P3= newp; Point(P3) = {r2,0, L, h};
P4= newp; Point(P4) = {r1,0, L, h};

L12=newl; Line(L12) = {P1, P2};
L23=newl; Line(L23) = {P2, P3};
L34=newl; Line(L34) = {P3, P4};
L41=newl; Line(L41) = {P4, P1};

L0=newl; Line Loop(L0) = {L12, L23, L34, L41};
S=newreg; Plane Surface(S) = {L0};

// Define ext section
P5=newp; Point(P5) = {0,0, -r_ext, h_ext};
P6=newp; Point(P6) = {r_ext, 0, 0, h_ext};
P7=newp; Point(P7) = {0, 0, r_ext, h_ext};

L05=newl; Line(L05) = {P0, P5};
C56=newl; Circle(C56) = {P5, P0, P6};
C67=newl; Circle(C67) = {P6, P0, P7};
L70=newl; Line(L70) = {P7, P0};

L_ext=newl; Line Loop(L_ext) = {L05, C56, C67, L70};
S_ext=newreg; Plane Surface(S_ext) = {L_ext, -L0};

// Define inf section
P8=newp; Point(P8) = {0,     0, -r_inf, h_inf};
P9=newp; Point(P9) = {r_inf, 0, 0, h_inf};
P10=newp; Point(P10) = {0,   0, r_inf, h_inf};

L58=newl; Line(L58) = {P5, P8};
C89=newl; Circle(C89) = {P8, P0, P9};
C910=newl; Circle(C910) = {P9, P0, P10};
L107=newl; Line(L107) = {P10, P7};

L_inf=newl; Line Loop(L_inf) = {L58, C89, C910, L107, -C67, -C56};
S_inf=newreg; Plane Surface(S_inf) = {L_inf};

// Build 3D geom
Extrude { {0,0,1} , {0,0,0} , Pi/2. } { 
  Surface{S, S_ext, S_inf}; //Layers{N_Layers}; //Recombine; 
}

If ( IsFull != 0) 
Extrude { {0,0,1} , {0,0,0} , Pi/2 } { 
  Surface{40, 74, 96}; //Layers{N_Layers/2}; //Recombine; 
}

Extrude { {0,0,1} , {0,0,0} , Pi/2 } { 
  Surface{118, 152, 174}; //Layers{N_Layers/2}; //Recombine; 
}

Extrude { {0,0,1} , {0,0,0} , Pi/2 } { 
  Surface{196, 230, 252}; //Layers{N_Layers/2}; //Recombine; 
}
EndIf

//  Define Physical

If ( IsFull != 0 )
  Physical Volume("coil") = {1, 4, 7, 10}; // Tore
  Physical Volume("air") = {2, 5, 8, 11, 3, 6, 9, 12}; // Infini

  Physical Surface("Border") = {85, 88, 163, 166, 222, 225, 241, 244, 300, 303 };  // Inf
EndIf
If ( IsFull == 0 )
  Physical Volume("coil") = {1}; // Tore
  Physical Volume("air") = {2, 3}; // Infini

  Physical Surface("Border") = {85, 88};  // Inf
  Physical Surface("V0") = {6};   // V0
  Physical Surface("V1") = {40};  // V1
  Physical Surface("Rext") = {31};   
  Physical Surface("Rint") = {39};  
  Physical Surface("HP") = {27};   
  Physical Surface("BP") = {35};  

  Physical Surface("OXOZ") = {12, 18};  // Sym
  Physical Surface("OYOZ") = {74, 96};  // Sym
EndIf

