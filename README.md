# Interactive COVID-19 Dashboard

Moh was here.

The dashboard is implemented as a Streamlit app within a standalone Docker image.
The image comes with the required Python version and all requirements installed.
The container starts the dashboard automatically on startup.

The dashboard is exposed on port 80.

To spin-up the Docker container and run the dashboard:  
> `docker run -p 8501:80 ds21m025/sdc_technikum-wien:covid_dashboard_v1.1`

The image is publicly available at:  
[ds21m025/sdc_technikum-wien on dockerhub](https://hub.docker.com/r/ds21m025/sdc_technikum-wien/tags)


## Continuous Deployment on Docker Hub and Azure

The source code is hosted in the GitHub repository [ds21m025/SDC-Exercise4](https://github.com/ds21m025/SDC-Exercise4)

The GitHub Action [build-and-deploy.yml](https://github.com/ds21m025/SDC-Exercise4/blob/main/.github/workflows/build-and-deploy.yml)

- builds the Docker container,
- pushes the container to the public Docker Hub repository [ds21m025/sdc_technikum-wien on dockerhub](https://hub.docker.com/r/ds21m025/sdc_technikum-wien/tags),
- deploys the Docker container as an [Azure Web App: covid_dashboard](https://wa-sdc-covid-dashboard.azurewebsites.net/).

In order to check the build process and deployment, the dashboard shows the Git commit ID as container version.
