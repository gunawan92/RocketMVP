import math

g0 = 9.80665

isp = 320
wet_mass = 1000
dry_mass = 200

delta_v = isp * g0 * math.log(wet_mass / dry_mass)

print(f"ISP       : {isp} s")
print(f"Wet Mass  : {wet_mass} kg")
print(f"Dry Mass  : {dry_mass} kg")
print()
print(f"Delta-V   : {delta_v:.2f} m/s")
