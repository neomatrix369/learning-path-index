- Setup Selenium (Chrome Driver, Chrome install)
Grab the Chrome installer and driver from https://googlechromelabs.github.io/chrome-for-testing/

```bash
wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chromedriver-linux64.zip
```

Selenium and Chrome in WSL
```bash
https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/
```

- Setup environment variables
.env.example is a template to become .env


- Works by signing in to the site using Selenium (sign-in involves multiple APIs and services, and so would be difficult to achieve with vanilla web scrapping)

- Uses the tokens retrieved to query Qooper API

