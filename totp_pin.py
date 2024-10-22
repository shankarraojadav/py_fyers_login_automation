import pyotp as tp

totp_key = "NLEOUKY2E2SUGSPSVN7A2B5L4BE366SB"
k=tp.TOTP(totp_key).now()
print(k)