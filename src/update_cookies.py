import json

# Load Cookie-Editor export
with open("lidl_cookies.json", "r") as f:
    cookies_list = json.load(f)

cookies = {c["name"]: c["value"] for c in cookies_list}

# Manually add XSRF-TOKEN from DevTools
xsrf = input("Paste XSRF-TOKEN value: ").strip()
cookies["XSRF-TOKEN"] = xsrf

# Save as simple dict for easy reuse
with open("session.json", "w") as f:
    json.dump(cookies, f, indent=2)

print("Saved to session.json")
print("Keys:", list(cookies.keys()))
