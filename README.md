# Interactive COVID-19 Dashboard

The dashboard is implemented as a Streamlit app within a standalone Docker image.
The image comes with the required Python version and all requirements installed.
The container starts the dashboard automatically on startup.

The dashboard is exposed on port 8501.

To spin-up the Docker container and run the dashboard:  
> `docker run -p 8501:8501 ds21m025/sdc_technikum-wien:covid_dashboard_v1.1`

The image is publicly available at:  
[ds21m025/sdc_technikum-wien on dockerhub](https://hub.docker.com/r/ds21m025/sdc_technikum-wien/tags)
