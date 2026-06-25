from rocketpy import Environment

env = Environment(
    latitude=-6.9175,
    longitude=107.6191,
    elevation=768
)

print("RocketPy OK")
print(f"Latitude  : {env.latitude}")
print(f"Longitude : {env.longitude}")
print(f"Elevation : {env.elevation}")
