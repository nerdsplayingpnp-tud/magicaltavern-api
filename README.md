<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">magicaltavern api</h3>

  <p align="center">
    This repository provides an SQLite database, a RESTful API for use with magicaltavern-bot or your own implementations of a magicaltavern-web-client, and last but not least a website for the magicaltavern service, with which users can enroll into Pen and Paper campaigns.
    <br />
    <a href="https://github.com/bitfl0wer/magicaltavern-web/wiki"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/bitfl0wer/magicaltavern-web/issues">Report Bug</a>
    ·
    <a href="https://github.com/bitfl0wer/magicaltavern-web/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<!--[![Product Name Screen Shot][product-screenshot]](https://example.com)-->

This repository provides a JSON-based database handler, a RESTful API for use with magicaltavern-bot, your own implementations of a magicaltavern-web-endpoint, and last but not least a website for the magicaltavern service, with which users can enroll into Pen and Paper campaigns.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* Python 3.9
* Flask
* SQLAlchemy
* SQLite
* SQLAlchemy-serializer

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local development environment up and running, follow these steps.

### Prerequisites

* **On Windows**: Install Windows Subsystem for Linux. Use the WSL Terminal for this Project.
* [python 3.9](https://www.python.org/downloads/)
* pip

  ```sh
  python -m ensurepip --upgrade
  ```

* venv

### Installation

1. Clone the repo and cd into it.

   ```sh
   git clone https://github.com/bitfl0wer/magicaltavern-web.git
   cd ./magicaltavern-web
   ```

2. Create a venv and activate it.

   ```sh
   python3 -m venv ./venv venv
   source ./venv/bin/activate
   ```

3. Install requirements. Either:

   ```sh
   pip install -r requirements.txt
   ```

   or

   ```sh
   python -m pip install -r requirements.txt
   ```

4. Add an API key to the database. See [the API documentation](./docs/api_v2.md).
5. Create the file `${PROJECTDIR}/app_configurator.py` using the following template:

    ```py
    from flask import Flask


    def configure(app: Flask) -> Flask:
        app.config[
            "SECRET_KEY"
        ] = ""
        app.config["DISCORD_CLIENT_ID"] = 
        app.config["DISCORD_CLIENT_SECRET"] = ""
        app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:7777/callback"
        return app
    ```  

    Fill in the value `SECRET_KEY` and add the ID and Client Secret of a Discord Application that you plan to use for the project.

6. Start the development environment with

   ```sh
   python main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

WIP!

_For more examples, please refer to the [Documentation](https://github.com/bitfl0wer/magicaltavern-web/wiki)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

* [ ] Website!
  * [ ] Campaign Enroll Feature
  * [ ] Discord OAuth Login
  * [ ] E-Mail and Password Login
* [ ] 1-Factor Email Authentication

See the [open issues](https://github.com/bitfl0wer/magicaltavern-web/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the AGPL v3.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Nerds Playing PnP - nerdsplayingpnp@gmail.com.com

Project Link: [https://github.com/bitfl0wer/magicaltavern-web](https://github.com/bitfl0wer/magicaltavern-web)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Fugi](https://github.com/FugiMuffi)
  * Added Dockerfile and corresponding configuration for easy Docker Deploy functionality! Also reviewed my code on the big rewrite :)
* [SaltyOne](https://github.com/Juhi838b)
  * Is currently working on all website related issues, and is a second project maintainer. ❤️
* [Casey](https://github.com/KreerC)
  * Reviewed my pull request and suggested changes! Thanks, casey! :>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/bitfl0wer/magicaltavern-web.svg?style=for-the-badge
[contributors-url]: https://github.com/bitfl0wer/magicaltavern-web/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bitfl0wer/magicaltavern-web.svg?style=for-the-badge
[forks-url]: https://github.com/bitfl0wer/magicaltavern-web/network/members
[stars-shield]: https://img.shields.io/github/stars/bitfl0wer/magicaltavern-web.svg?style=for-the-badge
[stars-url]: https://github.com/bitfl0wer/magicaltavern-web/stargazers
[issues-shield]: https://img.shields.io/github/issues/bitfl0wer/magicaltavern-web.svg?style=for-the-badge
[issues-url]: https://github.com/bitfl0wer/magicaltavern-web/issues
[license-shield]: https://img.shields.io/github/license/bitfl0wer/magicaltavern-web.svg?style=for-the-badge
[license-url]: https://github.com/bitfl0wer/magicaltavern-web/blob/master/LICENSE.txt
