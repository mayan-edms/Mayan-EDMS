sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install git-core python-virtualenv gcc python-dev libjpeg-dev libpng-dev libtiff-dev tesseract-ocr poppler-utils unpaper redis-server libreoffice
git clone /mayan-edms-repository/ /home/vagrant/mayan-edms
cd /home/vagrant/mayan-edms
git checkout development
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install redis
./manage.py initialsetup
