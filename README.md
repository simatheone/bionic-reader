<div align="center">
    <h1>
        Bionic Reader Backend
    </h1>
</div>

<a name="top"></a>
<details>
    <summary>Table of Contents</summary>
    <ul>
        <li>
            <a href="#about-the-project">About The Project</a>
            <ul>
                <li><a href="#disclaimer">Disclaimer</a></li>
            </ul>
            <ul>
                <li><a href="#built-with">Built With</a></li>
            </ul>
        </li>
        <li>
            <a href="#getting-started">Getting Started</a>
            <ul>
                <li><a href="#installation">Installation</a></li>
            </ul>
        </li>
        <!-- <li><a href="#usage">Usage</a></li>
            <ul>
                <li><a></a></li>
                <li><a></a></li>
                <li><a></a></li>
                <li><a></a></li>
                <li><a></a></li>
            </ul> -->
        <li><a href="#contributing">Contributing</a></li>
        <li><a href="#license">License</a></li>
        <li><a href="#contacts">Contacts</a></li>
    </ul>
</details>

#
# About the Project
### Disclaimer
The **Bionic Reading method is not our invention!**</br>
The developed service was created as a hobby project and is absolutely free of charge.
It is not used for commercial purposes. Anyone can register and use the service absolutely for free!
</br>

#
Bionic Reading is a technique that allows you to highlight a certain number of letters in the text. While reading your brain is focusing on the highlighted letters and complete the words (non highlighted letters). It increases your reading speed and deep understanding of content.
</br>

[Experience it now!][bionic-reader-site]

## Features
- transform your text even if you are not logged in;
- save every transformed text in a document and download it as PDF file (have to login first);
- English and Russian languages are supported;
- up to 59 documents per page;
- scroll down/swipe up to load more documents;
- email with the unique link if you forgot your password;
- the service is adapted for mobile and tabletes.

<p align="right"><a href="#top">Back to Contents</a></p>

## Built With
### Backend

![](https://img.shields.io/badge/Deployed_at-Railway.app-9cf)
![](https://img.shields.io/badge/python-3.8.10-9cf)
![](https://img.shields.io/badge/FastAPI-0.92.0-9cf)
![](https://img.shields.io/badge/Uvicorn-0.18.3-9cf)
![](https://img.shields.io/badge/pydantic-1.10.2-9cf)
![](https://img.shields.io/badge/FastAPI_Users-10.1.5-9cf)
![](https://img.shields.io/badge/PostgreSQL-13-9cf)
![](https://img.shields.io/badge/SQLAlchemy-1.4.41-9cf)
![](https://img.shields.io/badge/Alembic-1.8.1-9cf)
![](https://img.shields.io/badge/FPDF2-2.5.7-9cf)

![](https://img.shields.io/badge/Pyright-1.1.294-yellow)
![](https://img.shields.io/badge/Flake8-5.0.4-yellow)
![](https://img.shields.io/badge/pre_commit-3.0.4-yellow)
![](https://img.shields.io/badge/isort-5.10.1-yellow)


### Frontend
Application's Frontend could be found [Here][frontend-repo] made by [Igor Shevchenko][igor-shevchenko].

# Getting Started

### Installation
1. Clone the repo:
   ```bash
   $ git clone https://github.com/simatheone/bionic-reader.git
   ```

2. Prepare virtual environment and activate it:
   ```bash
   $ cd bionic-reader/
   ```
   ```bash
   $ python3.10 -m venv venv
   ```
   ```bash
   $ source venv/bin/activate
   ```

3. Upgrade pip and install requrements:
   ```bash
   (venv) $ pip install --upgrade pip
   ```
   ```bash
   (venv) $ pip install -r requirements.txt
   ```

<p align="right"><a href="#top">Back to Contents</a></p>

<!-- # Usage -->

## API
See auto-generated documentation for API to get all information about available endpoints and methods.
- <a href="http://127.0.0.1:8000/docs/">Swagger</a>
- <a href="http://127.0.0.1:8000/redoc/">ReDoc</a>


### Contributing
Have any suggestions that could improve this project? Fork the repository and create a [Pull Request][pull-request].

1. Fork the project
2. Create your **feature** branch:
```bash
git switch -c feature/new_feature
```

3. Commit your changes in a [Commit Convention style][commit-convention]:
```bash
git commit -m "feat: new awesome feature"
```

4. Push your branch:
```bash
git push origin feature/new_feature
```

5. Open a [Pull Request][pull-request]

Found a bug? Open a [New issue][issues] and describe it there. Your help is much appreciated!

### License
Distributed under the MIT License. See [LICENSE][license-url] for more information.
### Contacts

Alexander Sviridov<br/>
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:alexandersv686@gmail.com) &nbsp;
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/simatheone) &nbsp;
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sviridov-ak-dev/)


Igor Shevchenko<br/>
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:hello.igorshevchenko@gmail.com) &nbsp;
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/heyiamigor) &nbsp;
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/igorshevchenkowork/)

<p align="right"><a href="#top">Back to Contents</a></p>


<!-- Links -->
[license-url]: https://github.com/simatheone/bionic-reader/blob/main/LICENSE
[pull-request]: https://github.com/simatheone/bionic-reader/pulls
[issues]: https://github.com/simatheone/bionic-reader/issues
[commit-convention]: https://www.conventionalcommits.org/en/v1.0.0/#summary

[frontend-repo]: https://github.com/bnzone/bionic-reader
[igor-shevchenko]: https://github.com/bnzone
[bionic-reader-site]: https://bionic-reader.up.railway.app/
