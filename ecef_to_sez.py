# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
#  Converts ECEF coordinates at SEZ origin (o_x_km,o_y_km,o_z_km) and ECEF coordinates (x_km,y_km,z_km) to coordinates in SEZ (s_km,e_km,z_km)
# Parameters:
# Output:
#  Print the SEZ coordinates (s_km,e_km,z_km) in km
#
# Written by Erika Ashley
# Other contributors: None
#


# import Python modules
# e.g., import math # math module
import sys # argv
import math

# "constants"
R_E_KM = 6378.1363
E_E    = 0.081819221456
# helper functions

## calc_denom
##
def calc_denom(ecc,lat_rad):
    return math.sqrt(1.0-ecc**2.0*math.sin(lat_rad)**2.0)
## function description
# def calc_something(param1, param2):
#   pass

# initialize script arguments
o_x_km=float('nan')
o_y_km=float('nan') 
o_z_km=float('nan') 
x_km=float('nan')  
y_km=float('nan') 
z_km=float('nan') 

# parse script arguments
if len(sys.argv)==7:
    o_x_km=float(sys.argv[1])
    o_y_km=float(sys.argv[2])
    o_z_km=float(sys.argv[3])
    x_km=float(sys.argv[4])
    y_km=float(sys.argv[5])
    z_km=float(sys.argv[6])
else:
   print(\
   'Usage: '\
   'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'\
  )
   exit()

# calculate longitude
lon_rad = math.atan2(o_y_km,o_x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(o_z_km/math.sqrt(o_x_km**2+o_y_km**2+o_z_km**2))
r_lon_km = math.sqrt(o_x_km**2+o_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((o_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1
lat_deg=lat_rad*180.0/math.pi
# calculate hae
hae_km = r_lon_km/math.cos(lat_rad)-c_E

# write script below this line
denom=calc_denom(E_E,lat_rad)
c_E=R_E_KM/denom
s_E=R_E_KM*(1.0-E_E*E_E)/denom
r_x_km=(c_E+hae_km)*math.cos(lat_rad)*math.cos(lon_rad)
r_y_km=(c_E+hae_km)*math.cos(lat_rad)*math.sin(lon_rad)
r_z_km=(s_E+hae_km)*math.sin(lat_rad)
recef_vect=[r_x_km,r_y_km,r_z_km]

ecef_llh=[lat_deg,lon_deg,hae_km]
o_ecef=[o_x_km, o_y_km, o_z_km]
ecef=[x_km, y_km, z_km]
ecef_vect=[]

for i,j in zip(o_ecef,ecef):
    ecef_vect.append(j - i)
print(ecef_vect)
print(ecef_llh)
rotation_1=[[math.sin(lat_rad), 0, -math.cos(lat_rad)],[0, 1, 0],[math.cos(lat_rad),0,math.sin(lat_rad)]]
rotation_2=[[math.cos(lon_rad),math.sin(lon_rad),0],[-math.sin(lon_rad),math.cos(lon_rad),0],[0,0,1]]

rotationcalc_1=[0,0,0]
rotationcalc_2=[0,0,0]

for i in range(3):
    for j in range(3):
         rotationcalc_1[i]+=rotation_2[i][j]*ecef_vect[j]

for i in range(3):
    for j in range(3):
        rotationcalc_2[i]+=rotation_1[i][j]*rotationcalc_1[j]

ecef_x_km=rotationcalc_2[0]
ecef_y_km=rotationcalc_2[1]
ecef_z_km=rotationcalc_2[2]
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)
