# Ibovespa, Selic, IPCA Analysis 

## About The Project

This project focuses on providing an analysis of the main Brazilian indicators, namely IBOVESPA, SELIC, and IPCA. 
The technologies used for this purpose include Python, Apache Spark, Pyspark, Pandas, Docker, and Apache Superset. 

The data was extracted using the bcb library. For more information, visit: https://pypi.org/project/python-bcb/

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![APACHE_SPARK][APACHE_SPARK]][APACHE_SPARK_URL]
[![APACHE_SUPERSET][APACHE_SUPERSET]][APACHE_SUPERSET_URL]
[![PYTHON][PYTHON]][PYTHON_URL]
[![PANDAS][PANDAS]][PANDAS_URL]
[![DOCKER][DOCKER]][DOCKER_URL]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

To use this project, the softwares that needs to be installed are Docker Engine and Docker Desktop. 

For installation, follow the instructions at: 
- https://docs.docker.com/engine/install/
- https://docs.docker.com/desktop/install/linux-install/

Please note that this application was developed in a Linux environment.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/LeandroChinelli/brazilian_indexes_analysis.git
   ```
2. Set up the Spark Cluster with 3 worker nodes
   ```sh
   docker-compose up -d --scale spark-worker=3
   ```
3. Execute the app
   ```js
   docker exec spark-master spark-submit --master spark://spark-master:7077 ./apps/main.py;
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

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

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

<div align="left">
    <a href="https://www.linkedin.com/in/leandrochinelli-datadriven" target="_blank"> 
        <img  alt="linkedin" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg">
    <a href="https://github.com/LeandroChinelli" target="_blank"> 
        <img  alt="linkedin" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg">
</div>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- IMAGES -->
[APACHE_SPARK]: https://img.shields.io/badge/-Apache%20Spark-%23E25A1C?style=for-the-badge&logo=ApacheSpark&logoColor=white
[APACHE_SUPERSET]:https://img.shields.io/badge/Apache_Superset-03BB85?style=for-the-badge&logo=Apache
[PYTHON]:https://img.shields.io/badge/%20-Python-%233776AB?style=for-the-badge&logo=Python&logoColor=white
[PANDAS]:https://img.shields.io/badge/-Pandas-%23150458?style=for-the-badge&logo=Pandas&logoColor=white
[DOCKER]:https://img.shields.io/badge/%20-docker-0db7ed?style=for-the-badge&logo=Docker&logoColor=white       

<!-- LINKS -->
[APACHE_SPARK_URL]:https://spark.apache.org/
[APACHE_SUPERSET_URL]:https://superset.apache.org/
[PYTHON_URL]:https://www.python.org/
[PANDAS_URL]:https://pandas.pydata.org/
[DOCKER_URL]:https://www.docker.com/
[LINKEDIN_URL]:https://www.linkedin.com/in/leandrochinelli-datadriven
[GITHUB_URL]:https://github.com/LeandroChinelli
