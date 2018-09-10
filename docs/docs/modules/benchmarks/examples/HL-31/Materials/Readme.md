Repository for Materials properties in mm

To check files:
for file in $(ls -1 *.json); do echo -n "$file: "; jsonlint-php $file; done

Example of a material file:
Note: All variables needs to be expressed using millimeters as length dimension, except for the Siemens used for the electrical conductivity.
{
    "name":"Material_name_composition",
    "alpha":"3.75e-3", #temperature coefficient, K-1
    "T0":"293", #reference temperature of alpha and k0, K
    "sigma0":"56.e+3", #electrical conductivity, S.mm-1
    "k0":"0.4", #thermal conductivity, W.mm-1.K-1
    "sigma":"sigma0/(1+alpha*(T-T0)):sigma0:alpha:T:T0",
    "k":"k0*T/((1+alpha*(T-T0))*T0):k0:T:alpha:T0",
    "E":"69e+9", #young modulus, Pa = 10^3 kg.mm-1.s-2
    "nu":"0.33", #poisson ratio, dimensionless
    "alphaT":"18e-6", #temperature coefficient, K-1
    "rho":"10.e-6", #density, kg.mm-3
    "Re":"450", #yield strength, MPa = 10^9 kg.mm-1.s-2
    "mu":"1" #dimensionless
}

