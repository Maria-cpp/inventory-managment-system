# inventory-managment-system
Product inventory managment system
# create a docker image by writing following command in terminal
 
 docker build . -t image_name

# create a container for image using following command 
# port is also mapped to run the streamlit app on localhost

docker run --name container_name -p 8501:8501 -d -v $(pwd):/code image_name

# check the app in browser by writing following

http://localhost:8501