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
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/bitfl0wer/magicaltavern-web">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">magicaltavern web</h3>

  <p align="center">
    This repository provides a JSON-based database handler, a RESTful API for use with magicaltavern-bot or your own implementations of a magicaltavern-web-endpoint, and last but not least a website for the magicaltavern service, with which users can enroll into Pen and Paper campaigns.
    <br />
    <a href="https://github.com/bitfl0wer/magicaltavern-web"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/bitfl0wer/magicaltavern-web">View Demo</a>
    ·
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
4. To test `POST`, `PUT` and `DELETE` API Calls, put an API Key into `data/keys.txt`. This key can be anything you want it to be.
5. Start the development environment with
   ```sh
   python main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

WIP!

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Website!
  - [ ] Campaign Enroll Feature
  - [ ] Discord OAuth Login
  - [ ] E-Mail and Password Login
- [ ] 1-Factor Email Authentication

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
  * Added Dockerfile and corresponding configuration for easy Docker Deploy functionality!
* [SaltyOne](https://github.com/Juhi838b)
  * Is currently working on all website related issues, and is a second project maintainer. ❤️

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
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/N/A
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
