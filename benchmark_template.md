## Description of the example

In this example, we will estimate the rise in temperature due to Joules losses in  a stranded conductor. An electrical potential $V_0$ is applied to the entry/exit of the conductor which is also cooled by a force flow.
The geometry of the conductor is choosen as to have an analytical expression for the temperature.

## Geometry

- The conductor consists in a rectangular cross section torus which is somehow "cut" to allow for applying electrical potential. The conductor is cooled with a force flow along its cylindrical faces.
- /images/learning/thermoelectric/quarter-turn3D.png
- _upload CAD file if available_

| Name     | Description                      | Value                            | Unit               |
| -------- | -------------------------------- | -------------------------------- | ------------------ |
| $r_1$    | internal radius                  | $1.10^{-3}$                      | m                  |
| $r_2$    | external radius                  | $2.10^{-3}$                      | m                  |
| dz~      | height                           | $2.10^{-3}$                      | m                  |


## Input parameters

| Name     | Description                      | Value                            | Unit               |
| -------- | -------------------------------- | -------------------------------- | ------------------ |
| $Tw_1$   | coolant temperature on r~1~      | 293                              | K                  |
| $Tw_2$   | coolant temperature on r~2~      | 293                              | K                  |

| $h_1$    | heat transfer coefficient on r~1 | $h_{1}=h_{2}\frac{r_{2}}{r_{1}}$ | $W.m^{-2} .K^{-1}$ |
| $h_2$    | heat transfer coefficient on r~1 | 80000                            | $W.m^{-2} .K^{-1}$ |

| $V_0$    | electrical potential             | 0.3                              | V                  |


## Model & Toolbox

- This problem is fully described by a ThermoElectricModel, namely a poisson equation for the electrical potential $V$ and a standard heat equation for the temperature field $T$ with Joules losses as a source term.
Assuming that the physical properties of the materials forming the conductor are not dependent on $T$, we can show that $(V,T)$ are solutions of:
\[
\rho C_{p}\frac{\partial T}{\partial t} - \nabla.(k \nabla T)=\sigma(\frac{U}{2\pi r})^{2}
\]

In our geometry and owing to the considered thermal boundary conditions, $T$ only depends on the radius $r$.
We can show that the $T$ static solution is of the form:
\[
T=-a \log(\frac{r}{r_{0}})^{2} + T_{max}
\]
with:
- $a=sigma0/(2*k)*(V0/(2*pi))**2$
- $b=k*(1/(h1*r1)+1/(h2*r2))+log(r2/r1)$
- $c=log(r2/r1)*log(r2*r1)+2*k*(log(r1)/(h1*r1)+log(r2)/(h2*r2))$
- $r0=exp( ((Tw2-Tw1)/b+a*c/b)/(2*a) )$
- \[Tm = 2*a*k/(h1*r1+h2*r2)*log(r2/r1)
        + (h1*r1*Tw1+h2*r2*Tw2)/(h1*r1+h2*r2)
        + a*(h1*r1*log(r1/r0)**2+h2*r2*log(r2/r0)**2)/(h1*r1+h2*r2)
  \]

- **toolbox**:  thermoelectric

### Materials

| Name     | Description                      | Value                            | Unit               |
| -------- | -------------------------------- | -------------------------------- | ------------------ |
| $\sigma$ | electrical conductivity          | $58.10^{6}$                      | $S.m^{-1}$         |
| k        | thermal conductivity             | 380                              | $W.m^{-1} .K^{-1}$ |

### Boundary conditions

The boundary conditions for the electrical probleme are introduced as simple Dirichlet boundary conditions for the electric potential on the entry/exit of the conductor. For the remaining faces, as no current is flowing througth these faces, we add Homogeneous Neumann conditions.

As for the heat equation, the forced water cooling is modeled by robin boundary condition with $Tw$ the temperature of the coolant and $h$ an heat exchange coefficient.

| Name     | Description                      | Value                            | Unit               |
| -------- | -------------------------------- | -------------------------------- | ------------------ |
| $Tw_1$   | coolant temperature on r~1~      | 293                              | K                  |
| $Tw_2$   | coolant temperature on r~2~      | 293                              | K                  |

| $h_1$    | heat transfer coefficient on r~1 | $h_{1}=h_{2}\frac{r_{2}}{r_{1}}$ | $W.m^{-2} .K^{-1}$ |
| $h_2$    | heat transfer coefficient on r~1 | 80000                            | $W.m^{-2} .K^{-1}$ |


## Outputs

The output is describe the output set of the example

### Fields

add scalar vectorial and matricial fields to be visualized

### Measures

add measures, scalar quantities, mean values, performance metrics

## Benchmark

Describe Benchmark type:
[X] Verification
[] Validation
[] Performance

The computed values of the temperature are compared with the analytical expression given above for several mesh sizes.

## References (articles, papers, reports...)

- add any article in pdf or html links related to the example
- [REF001] authors..., title, ... journal,... year...
