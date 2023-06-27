SaladPy
==========

Key Features
-------------

- Modern async API using `asyncio`.
- Allows you to access all the Salad web API endpoints
- Supports token caching

Installing
----------

To install the library, you can just run the following command:

```sh
# Linux/macOS
python3 -m pip install -U saladpy

# Windows
py -3 -m pip install -U saladpy
```

Quick Example
--------------

```py
import saladpy
import asyncio

async def main():
    client = saladpy.SaladClient()
    verify = await client.login("john.doe@example.com")

    # Verify using the OTP sent to your email
    await verify(input("Enter OTP: "))

    # Get Balance
    balance = await client.balance()
    print("Your Salad balance is", balance)

    # Safely close SaladClient (Highly Recommended)
    await client.close()

asyncio.run(main())
```

Docs
--------------
Docs are available at <https://saladpy.gitbook.io/saladpy-docs/>. 

Contact
--------------
You can contact me at `Coddo#3210` on Discord! Ensure to first send me a friend request.