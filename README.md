# foodorderingapp
Comp3122 project


# How to test
cd foodorderingapp_a
# build all containers
docker-compose up

# new terminal
cd tests
# install pytest
pip install pytest 
# install requests
pip install requests
# test
pytest -v unit.py