import pyotp as tp

totp_key = ""
k=tp.TOTP(totp_key).now()
print(k)