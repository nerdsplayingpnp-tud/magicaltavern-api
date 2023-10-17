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


<!-- PROJECT LOGO -->
<br />
<div align="center">

<img src="https://cloud.bitfl0wer.de/apps/files_sharing/publicpreview/HmLLyW3ZKXNt3oK?file=/&fileId=1003663&x=400&y=400" style="width: 100px"/>

<br />

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<h2 align="center">magicaltavern-api</h3>

  <p align="center">
    A server for magicaltavern, an enrollment/campaign management tool for Pen and Paper Gamemasters and Players alike.
    <br />
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

<!--[![Product Name Screen Shot][product-screenshot]](https://example.com)-->

This repository provides a a REST API for use with magicaltavern-compatible clients.


### Built With

* Python 3.9
* Flask
* SQLAlchemy
* SQLite
* SQLAlchemy-serializer


<!-- GETTING STARTED -->
## Getting Started

To get a local development environment up and running, follow these steps.

### Prerequisites

* cargo and rustc, version 1.73 and up.

### Installation

1. Clone the repo and cd into it.

   ```sh
   git clone https://github.com/bitfl0wer/magicaltavern-web.git
   cd ./magicaltavern-web
   ```

2. Build and run
   ```sh
   cargo run
   ```
3. If you'd like to change the database model, you'll have to do database migrations. To be able to do so, install `sea-orm-cli`
    ```
    cargo install sea-orm-cli
    ```

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


<!-- LICENSE -->
## License

Distributed under the AGPL-v3.0 License. See `LICENSE.txt` for more information.


<!-- CONTACT -->
## Contact

Nerds Playing PnP - nerdsplayingpnp@gmail.com.com

Project Link: [https://github.com/bitfl0wer/magicaltavern-web](https://github.com/bitfl0wer/magicaltavern-web)


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Fugi](https://github.com/FugiMuffi)
  * Added Dockerfile and corresponding configuration for easy Docker Deploy functionality! Also reviewed my code on the big rewrite :)
* [SaltyOne](https://github.com/Juhi838b)
  * Is currently working on all website related issues, and is a second project maintainer. ❤️
* [Casey](https://github.com/KreerC)
  * Reviewed my pull request and suggested changes! Thanks, casey! :>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/bitfl0wer/magicaltavern-web.svg
[contributors-url]: https://github.com/bitfl0wer/magicaltavern-web/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bitfl0wer/magicaltavern-web.svg
[forks-url]: https://github.com/bitfl0wer/magicaltavern-web/network/members
[stars-shield]: https://img.shields.io/github/stars/bitfl0wer/magicaltavern-web.svg
[stars-url]: https://github.com/bitfl0wer/magicaltavern-web/stargazers
[issues-shield]: https://img.shields.io/github/issues/bitfl0wer/magicaltavern-web.svg
[issues-url]: https://github.com/bitfl0wer/magicaltavern-web/issues
[license-shield]: https://img.shields.io/github/license/bitfl0wer/magicaltavern-web.svg
[license-url]: https://github.com/bitfl0wer/magicaltavern-web/blob/master/LICENSE.txt
