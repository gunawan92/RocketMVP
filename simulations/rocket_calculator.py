import math

g0 = 9.81

isp = float(input("ISP (s): "))
wet_mass = float(input("Wet Mass (kg): "))
dry_mass = float(input("Dry Mass (kg): "))

delta_v = isp * g0 * math.log(wet_mass / dry_mass)

print()
print(f"Delta-V : {delta_v:.2f} m/s")
